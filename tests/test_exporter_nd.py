"""Testes do tratamento N/D para colunas de sensor opcionais no export."""

import pandas as pd

from src.services.exporter import DataExporter


def _build_record(**overrides):
    base = {
        "vehicle_id": 1,
        "vehicle_name": "Teste",
        "plate": "TST-0001",
        "timestamp": "2026-04-01T10:00:00",
        "latitude": -22.87,
        "longitude": -43.29,
        "speed": 0,
        "ignition": True,
        "odometer": None,
        "fuel_level": None,
        "rpm": None,
        "vehicle_voltage": None,
        "internal_battery_voltage": None,
        "engine_hours": None,
        "driver": None,
        "address": None,
        "system_source": "wialon",
    }
    base.update(overrides)
    return base


def test_colunas_opcionais_sem_dado_exportam_nd(tmp_path):
    """Campos de sensor ausentes devem aparecer como N/D no CSV."""
    record = _build_record()
    exporter = DataExporter(base_export_dir=str(tmp_path))
    path = exporter.export_history_to_csv(
        history=[record],
        vehicle_id="1",
        month=4,
        year=2026,
        vehicle_name="Teste",
        vehicle_plate="TST-0001",
    )

    df = pd.read_csv(path)
    assert df["Odômetro (km)"].iloc[0] == "N/D"
    assert df["RPM"].iloc[0] == "N/D"
    assert df["Nível de Combustível (%)"].iloc[0] == "N/D"
    assert df["Tensão do Veículo (V)"].iloc[0] == "N/D"
    assert df["Bateria Interna (V)"].iloc[0] == "N/D"
    assert df["Horas de Motor"].iloc[0] == "N/D"
    assert df["Motorista"].iloc[0] == "N/D"
    assert df["Localização"].iloc[0] == "N/D"


def test_colunas_obrigatorias_nao_recebem_nd(tmp_path):
    """Latitude, longitude, velocidade e ignição nunca recebem N/D."""
    record = _build_record()
    exporter = DataExporter(base_export_dir=str(tmp_path))
    path = exporter.export_history_to_csv(
        history=[record],
        vehicle_id="1",
        month=4,
        year=2026,
        vehicle_name="Teste",
        vehicle_plate="TST-0001",
    )

    df = pd.read_csv(path)
    assert str(df["Latitude"].iloc[0]) != "N/D"
    assert str(df["Longitude"].iloc[0]) != "N/D"
    assert str(df["Velocidade (km/h)"].iloc[0]) != "N/D"
    assert str(df["Ignição"].iloc[0]) != "N/D"


def test_valores_presentes_nao_sao_sobrescritos(tmp_path):
    """Valores não-nulos devem ser preservados, não substituídos por N/D."""
    record = _build_record(odometer=1234.5, rpm=1500, fuel_level=80.0)
    exporter = DataExporter(base_export_dir=str(tmp_path))
    path = exporter.export_history_to_csv(
        history=[record],
        vehicle_id="1",
        month=4,
        year=2026,
        vehicle_name="Teste",
        vehicle_plate="TST-0001",
    )

    df = pd.read_csv(path)
    assert float(df["Odômetro (km)"].iloc[0]) == 1234.5
    assert int(df["RPM"].iloc[0]) == 1500
    assert float(df["Nível de Combustível (%)"].iloc[0]) == 80.0


def test_consolidado_tambem_aplica_nd(tmp_path):
    """Export consolidado também deve substituir None por N/D nas colunas opcionais."""
    record = _build_record()
    exporter = DataExporter(base_export_dir=str(tmp_path))
    path = exporter.export_consolidated_history_to_csv(
        all_history={"1": [record]},
        month=4,
        year=2026,
        vehicles_info={"1": {"name": "Teste", "plate": "TST-0001"}},
    )

    df = pd.read_csv(path)
    assert df["Odômetro (km)"].iloc[0] == "N/D"
    assert df["RPM"].iloc[0] == "N/D"
