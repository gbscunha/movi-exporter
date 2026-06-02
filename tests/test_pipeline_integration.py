"""
Testes de integração: transformer → normalizer → exporter.

Esses testes existem porque a Onda 1 teve regressões reais que passaram
pelos testes unitários de cada camada, mas quebraram no end-to-end:

- Fase 03 (odômetro None) era anulada pelo default=0.0 do normalizer
- Fase 05 (battery sem fallback interno) tinha furo (pwr_int ficou)
- Fase 07 (N/D) só pegava None, não 0.0/string vazia

Esses testes simulam o caminho completo de uma mensagem Wialon real até
o CSV final.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest

from src.services.exporter import DataExporter
from src.services.normalizer import DataNormalizer
from src.services.wialon_transformer import WialonTransformer


@pytest.fixture
def pipeline(tmp_path):
    """Fabrica os 3 componentes acoplados como a app os usa em produção."""
    client = MagicMock()
    client.apply_sensor_formula.return_value = None
    return {
        "transformer": WialonTransformer(client=client),
        "normalizer": DataNormalizer(),
        "exporter": DataExporter(base_export_dir=str(tmp_path)),
    }


def _run_pipeline(pipeline, wialon_messages):
    """Roda os 3 estágios e exporta CSV. Retorna o DataFrame."""
    transformer = pipeline["transformer"]
    normalizer = pipeline["normalizer"]
    exporter = pipeline["exporter"]

    transformed = []
    for msg in wialon_messages:
        record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
        if record is not None:
            transformed.append(record)

    normalized = normalizer.normalize_history(transformed, system="wialon")
    path = exporter.export_history_to_csv(
        normalized, "1", 4, 2026, vehicle_plate="TST-0001"
    )
    return pd.read_csv(path)


def test_pipeline_veiculo_parado_sem_pwr_ext_battery_externa_fica_nd(pipeline):
    """Bug VTR05: veículo parado nunca envia pwr_ext.

    A coluna 'Tensão do Veículo (V)' deve ser N/D, NÃO 4.1V (que era o
    pwr_int do tracker vazando pelo fallback antigo).
    """
    msgs = [
        {
            "t": 1700000000,
            "pos": {"y": -22.87, "x": -43.29, "s": 0},
            "p": {"pwr_int": 4.1},  # só interna, sem pwr_ext
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    assert df["Tensão do Veículo (V)"].iloc[0] == "N/D"
    assert float(df["Bateria Interna (V)"].iloc[0]) == 4.1


def test_pipeline_odometro_ausente_vira_nd_nao_zero(pipeline):
    """Bug regressão Onda 1: odômetro ausente virava 0 no CSV (não N/D)."""
    msgs = [
        {
            "t": 1700000000,
            "pos": {"y": -22.87, "x": -43.29, "s": 0},
            "p": {},  # sem odometer
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    assert df["Odômetro (km)"].iloc[0] == "N/D"


def test_pipeline_odometro_zero_e_preservado(pipeline):
    """0 km é leitura legítima (veículo novo) e deve ir para o CSV como 0, não N/D."""
    msgs = [
        {
            "t": 1700000000,
            "pos": {"y": -22.87, "x": -43.29, "s": 0},
            "p": {"odometer": 0},
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    assert float(df["Odômetro (km)"].iloc[0]) == 0.0


def test_pipeline_address_ausente_vira_nd(pipeline):
    """Endereço sem geocodificação deve aparecer como N/D, não vazio."""
    msgs = [
        {
            "t": 1700000000,
            "pos": {"y": -22.87, "x": -43.29, "s": 0},
            "p": {"pwr_ext": 12.6},
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    assert df["Localização"].iloc[0] == "N/D"


def test_pipeline_caminho_feliz_todos_os_campos(pipeline):
    """Cenário ideal: mensagem completa com todos os sensores presentes."""
    msgs = [
        {
            "t": 1700000000,
            "pos": {"y": -22.87, "x": -43.29, "s": 60},
            "p": {
                "odometer": 8661339,  # 8661.34 km
                "pwr_ext": 14.0,
                "pwr_int": 4.1,
                "ignition": 1,
                "fuel1": 75,
                "rpm": 2000,
                "engine_hours": 1234,
            },
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    row = df.iloc[0]
    assert float(row["Odômetro (km)"]) == 8661.34
    assert float(row["Tensão do Veículo (V)"]) == 14.0
    assert float(row["Bateria Interna (V)"]) == 4.1
    assert row["Ignição"] == "Ligado"
    assert float(row["Velocidade (km/h)"]) == 60.0


def test_pipeline_obrigatorios_nunca_recebem_nd(pipeline):
    """Latitude, longitude, velocidade e ignição NUNCA viram N/D, mesmo sem params."""
    msgs = [
        {
            "t": 1700000000,
            "pos": {"y": -22.87, "x": -43.29, "s": 0},
            "p": {},
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    assert df["Latitude"].iloc[0] != "N/D"
    assert df["Longitude"].iloc[0] != "N/D"
    assert df["Velocidade (km/h)"].iloc[0] != "N/D"
    assert df["Ignição"].iloc[0] != "N/D"


def test_pipeline_csv_tem_as_duas_colunas_de_tensao(pipeline, tmp_path):
    """Garante que o CSV tem EXATAMENTE 2 colunas de tensão (veículo + interna)."""
    msgs = [
        {
            "t": 1700000000,
            "pos": {"y": -22.87, "x": -43.29, "s": 0},
            "p": {"pwr_ext": 14.0, "pwr_int": 4.1},
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    assert "Tensão do Veículo (V)" in df.columns
    assert "Bateria Interna (V)" in df.columns
    # E NÃO deve mais existir a coluna ambígua antiga
    assert "Tensão da Bateria (V)" not in df.columns


# ----- Cenários Suntech ST380 (frota Movi em produção) -----
#
# Mensagens reais capturadas via API no QA do VTR05 (Conta 1, Abril/2026).
# Suntech ST380 usa `model=197`, `rep_type='STT'` e nomes próprios para
# params críticos: `mode` (ignição), `s_asgn1`/`s_asgn2` (voltagens),
# `m_asgn1` (odômetro em metros).


def test_pipeline_suntech_andando_ignicao_ligada(pipeline):
    """Msg Suntech com velocidade > 0 e mode=1 → Ignição='Ligado'.

    Pré-Fase 17: Ignição vinha 'Desligado' mesmo com vel=20km/h porque o
    transformer procurava 'in'/'in1'/'din1' que não existem no Suntech.
    """
    msgs = [
        {
            "t": 1775136988,
            "pos": {"y": -22.88428, "x": -43.406108, "s": 20},
            "p": {
                "rep_type": "STT",
                "model": 197,
                "mode": 1,
                "s_asgn1": 28.67,
                "s_asgn2": 4.1,
                "m_asgn1": 240141149,
            },
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    row = df.iloc[0]
    assert row["Ignição"] == "Ligado"
    assert float(row["Tensão do Veículo (V)"]) == 28.67
    assert float(row["Bateria Interna (V)"]) == 4.1
    assert float(row["Odômetro (km)"]) == 240141.15


def test_pipeline_suntech_parado_ignicao_desligada(pipeline):
    """Msg Suntech com vel=0 e mode=0 → Ignição='Desligado'."""
    msgs = [
        {
            "t": 1775023200,
            "pos": {"y": -22.852862, "x": -43.483135, "s": 0},
            "p": {
                "rep_type": "STT",
                "model": 197,
                "mode": 0,
                "s_asgn1": 25.07,
                "s_asgn2": 4.2,
                "m_asgn1": 240099537,
            },
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    row = df.iloc[0]
    assert row["Ignição"] == "Desligado"
    # Mesmo parado, Suntech reporta tensão do veículo (s_asgn1 = bateria
    # de chumbo, lê sempre — não depende de motor ligado).
    assert float(row["Tensão do Veículo (V)"]) == 25.07
    assert float(row["Bateria Interna (V)"]) == 4.2
    assert float(row["Odômetro (km)"]) == 240099.54


def test_pipeline_suntech_perfil_detectado_por_rep_type():
    """Modelo Suntech diferente de 197 (ex: ST300) ainda usa o perfil pelo rep_type."""
    from src.services.tracker_profiles import SuntechProfile, detect_profile

    msg = {"pos": {}, "p": {"rep_type": "STT", "model": 215}}
    assert isinstance(detect_profile(msg), SuntechProfile)


def test_pipeline_msg_generica_continua_funcionando(pipeline):
    """Tracker genérico (não Suntech) deve continuar usando os nomes Wialon padrão."""
    msgs = [
        {
            "t": 1700000000,
            "pos": {"y": -22.87, "x": -43.29, "s": 60},
            "p": {
                "in": 1,
                "pwr_ext": 12.6,
                "pwr_int": 4.0,
                "odometer": 50000,
            },
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    row = df.iloc[0]
    assert row["Ignição"] == "Ligado"
    assert float(row["Tensão do Veículo (V)"]) == 12.6
    assert float(row["Bateria Interna (V)"]) == 4.0
    assert float(row["Odômetro (km)"]) == 50.0


# ----- Cenários Jimi VL03 (CVM0H79 — frota Movi Conta 2) -----
#
# Mensagens reais capturadas via API. Jimi não tem `model`/`rep_type` óbvio
# como Suntech — detecção é pela combinação `serial`+`gps_real_up`+`data_mode`.


def test_pipeline_jimi_andando_ignicao_ligada(pipeline):
    """Msg Jimi VL03 com `acc=1` → Ignição='Ligado'."""
    msgs = [
        {
            "t": 1780414000,
            "pos": {"y": -22.6799, "x": -43.4660, "s": 11},
            "p": {
                "mcc": 0,
                "mnc": 0,
                "lac": 0,
                "cell_id": 0,
                "acc": 1,
                "data_mode": 2,
                "gps_real_up": 0,
                "serial": 723,
            },
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    row = df.iloc[0]
    assert row["Ignição"] == "Ligado"
    # Sem `pwr_ext` nessa msg, sem propagação anterior — fica N/D.
    assert row["Tensão do Veículo (V)"] == "N/D"
    # `voltage` não aparece nessa msg também.
    assert row["Bateria Interna (V)"] == "N/D"
    # VL03 não reporta odômetro nessa config.
    assert row["Odômetro (km)"] == "N/D"


def test_pipeline_jimi_acc_zero_desligado(pipeline):
    """`acc=0` → Ignição='Desligado'."""
    msgs = [
        {
            "t": 1780000000,
            "pos": {"y": -22.7, "x": -43.5, "s": 0},
            "p": {"acc": 0, "data_mode": 0, "gps_real_up": 0, "serial": 1},
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    assert df.iloc[0]["Ignição"] == "Desligado"


def test_pipeline_jimi_voltage_vai_para_bateria_interna(pipeline):
    """`voltage` no Jimi é bateria interna do tracker — NÃO confundir com Suntech."""
    msgs = [
        {
            "t": 1780000000,
            "pos": {"y": -22.7, "x": -43.5, "s": 5},
            "p": {
                "acc": 1,
                "data_mode": 0,
                "gps_real_up": 0,
                "serial": 1,
                "voltage": 6,
            },
        }
    ]
    df = _run_pipeline(pipeline, msgs)
    row = df.iloc[0]
    assert float(row["Bateria Interna (V)"]) == 6.0
    # NÃO deve vazar para tensão do veículo.
    assert row["Tensão do Veículo (V)"] == "N/D"
