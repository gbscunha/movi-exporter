"""
Testes do WialonTransformer.

Fase 03 — odômetro deve ser lido dos params brutos e convertido de metros para km.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Garante que `src` é importável quando rodando direto via pytest.
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.wialon_transformer import WialonTransformer


def _make_transformer() -> WialonTransformer:
    client = MagicMock()
    # Sem fórmula aplicada, retorna None — não interfere nos testes de odômetro.
    client.apply_sensor_formula.return_value = None
    return WialonTransformer(client=client)


def test_odometro_converte_metros_para_km():
    """Odômetro vem em metros da API — deve sair em km."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"odometer": 8661339},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["odometer"] == 8661.34


def test_odometro_nulo_quando_param_ausente():
    transformer = _make_transformer()
    msg = {"t": 1700000000, "pos": {"y": -22.87, "x": -43.29, "s": 0}, "p": {}}
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["odometer"] is None


def test_odometro_fallback_para_new_mileage():
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"new_mileage": 5000000},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["odometer"] == 5000.0


def test_transformer_retorna_none_para_mensagem_sem_pos():
    """Mensagens sem GPS não devem virar linha no export (Fase 04)."""
    transformer = _make_transformer()
    msg = {"t": 1700000000, "pos": None, "p": {"pwr_ext": 14.2}}
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record is None


def test_battery_voltage_nao_usa_voltage_interno():
    """'voltage' é bateria interna do tracker — não deve preencher battery_voltage (Fase 05)."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"voltage": 4157},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["battery_voltage"] is None


def test_battery_voltage_usa_pwr_ext():
    """pwr_ext é a tensão real do veículo (Fase 05)."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"pwr_ext": 12.6},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["battery_voltage"] == 12.6
