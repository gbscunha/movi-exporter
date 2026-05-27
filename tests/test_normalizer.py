"""Testes do DataNormalizer (mapeamento Wialon)."""

from datetime import datetime

import pytest

from src.services.normalizer import DataNormalizer


@pytest.fixture
def normalizer():
    return DataNormalizer()


def test_sistemas_suportados_inclui_wialon(normalizer):
    assert "wialon" in normalizer.get_supported_systems()


def test_normalize_vehicle_list_preserva_campos_basicos(normalizer):
    raw = [{"vehicle_id": 1, "nm": "Caminhão A", "plate": "ABC-1234"}]
    out = normalizer.normalize_vehicle_list(raw)

    assert len(out) == 1
    v = out[0]
    assert v["id"] == 1
    assert v["name"] == "Caminhão A"
    assert v["plate"] == "ABC-1234"
    assert v["system_source"] == "wialon"
    assert v["raw_data"] == raw[0]


def test_normalize_history_preserva_campos_completos(normalizer):
    raw = [
        {
            "vehicle_id": 1,
            "timestamp": "2026-04-01T10:00:00",
            "latitude": -22.87,
            "longitude": -43.29,
            "speed": 45.5,
            "odometer": 1234.5,
            "ignition": True,
            "address": "Av. Brasil",
            "fuel_level": 80.0,
            "rpm": 1500,
            "vehicle_voltage": 12.6,
            "internal_battery_voltage": 4.1,
            "engine_hours": 1200,
            "driver": "João",
        }
    ]
    out = normalizer.normalize_history(raw)

    assert len(out) == 1
    r = out[0]
    assert r["vehicle_id"] == 1
    assert r["latitude"] == -22.87
    assert r["longitude"] == -43.29
    assert r["speed"] == 45.5
    assert r["odometer"] == 1234.5
    assert r["ignition"] is True
    assert r["fuel_level"] == 80.0
    assert r["rpm"] == 1500
    assert r["vehicle_voltage"] == 12.6
    assert r["internal_battery_voltage"] == 4.1
    assert r["engine_hours"] == 1200
    assert r["driver"] == "João"
    assert r["system_source"] == "wialon"


def test_normalize_history_sensor_ausente_vira_none(normalizer):
    """Campos opcionais sem dado devem ficar None — NUNCA defaults numéricos/string.

    Regressão Onda 1 #34: defaults 0.0/"" mascaravam ausência como zero válido,
    impedindo o exporter de substituir por N/D.
    """
    raw = [
        {
            "vehicle_id": 1,
            "timestamp": "2026-04-01T10:00:00",
            "latitude": -22.87,
            "longitude": -43.29,
            "speed": 0,
            "ignition": False,
        }
    ]
    out = normalizer.normalize_history(raw)

    r = out[0]
    assert r["odometer"] is None, "odometer ausente deve ser None, não 0.0"
    assert r["address"] is None, "address ausente deve ser None, não string vazia"
    assert r["fuel_level"] is None
    assert r["rpm"] is None
    assert r["vehicle_voltage"] is None
    assert r["internal_battery_voltage"] is None
    assert r["engine_hours"] is None
    assert r["driver"] is None


def test_normaliza_timestamp_unix_para_iso(normalizer):
    raw = [{"vehicle_id": 1, "timestamp": 1700000000}]
    out = normalizer.normalize_history(raw)

    # 1700000000 → ~2023-11-14 — depende do timezone local, mas deve produzir
    # uma string ISO válida com ano 2023.
    ts = out[0]["timestamp"]
    parsed = datetime.fromisoformat(ts)
    assert parsed.year == 2023


def test_normaliza_timestamp_iso_preservado(normalizer):
    raw = [{"vehicle_id": 1, "timestamp": "2026-04-01T10:00:00"}]
    out = normalizer.normalize_history(raw)
    assert out[0]["timestamp"] == "2026-04-01T10:00:00"


def test_sistema_desconhecido_retorna_lista_vazia(normalizer):
    """Sistema sem mapeamento deve logar erro e devolver lista vazia (sem crash)."""
    raw = [{"vehicle_id": 1}]
    out = normalizer.normalize_history(raw, system="sistema_inexistente")
    assert out == []


def test_add_system_mapping_estende_suportados(normalizer):
    normalizer.add_system_mapping("teste", {"vehicle_id": "device_id"})
    assert "teste" in normalizer.get_supported_systems()


def test_get_field_aninhado(normalizer):
    record = {"nested": {"key": "value"}}
    assert normalizer._get_field(record, "nested.key") == "value"
    assert normalizer._get_field(record, "nested.ausente", default="d") == "d"
