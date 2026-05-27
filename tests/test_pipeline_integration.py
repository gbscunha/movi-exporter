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
