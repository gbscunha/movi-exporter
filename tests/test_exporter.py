"""Testes do DataExporter — estrutura de pastas, colunas e formatos."""

from pathlib import Path

import pandas as pd
import pytest

from src.services.exporter import DataExporter


def _record(**overrides):
    base = {
        "vehicle_id": 1,
        "vehicle_name": "Teste",
        "plate": "TST-0001",
        "timestamp": "2026-04-01T10:00:00",
        "latitude": -22.87,
        "longitude": -43.29,
        "speed": 30,
        "ignition": True,
        "odometer": 1234.5,
        "fuel_level": 70.0,
        "rpm": 1500,
        "vehicle_voltage": 12.6,
        "internal_battery_voltage": 4.1,
        "engine_hours": 100,
        "driver": "João",
        "address": "Av. Brasil",
        "system_source": "wialon",
    }
    base.update(overrides)
    return base


@pytest.fixture
def exporter(tmp_path):
    return DataExporter(base_export_dir=str(tmp_path))


# ---------- Estrutura de pastas ----------


def test_cria_subpasta_mensal(exporter, tmp_path):
    exporter.export_history_to_csv(
        [_record()], "1", 4, 2026, vehicle_plate="TST-0001"
    )
    assert (tmp_path / "2026-04").is_dir()


def test_subpasta_por_conta_quando_account_name(exporter, tmp_path):
    exporter.export_history_to_csv(
        [_record()],
        "1",
        4,
        2026,
        vehicle_plate="TST-0001",
        account_name="Conta 2",
    )
    assert (tmp_path / "2026-04" / "Conta 2").is_dir()


def test_sem_account_name_arquivo_fica_direto_no_mes(exporter, tmp_path):
    path = exporter.export_history_to_csv(
        [_record()], "1", 4, 2026, vehicle_plate="TST-0001"
    )
    assert Path(path).parent == tmp_path / "2026-04"


# ---------- Colunas / cabeçalhos PT-BR ----------


def test_csv_contem_colunas_em_portugues(exporter):
    path = exporter.export_history_to_csv(
        [_record()], "1", 4, 2026, vehicle_plate="TST-0001"
    )
    df = pd.read_csv(path)

    for col in [
        "Data/Hora",
        "Latitude",
        "Longitude",
        "Velocidade (km/h)",
        "Odômetro (km)",
        "Ignição",
        "Localização",
        "Nível de Combustível (%)",
        "RPM",
        "Tensão do Veículo (V)",
        "Bateria Interna (V)",
        "Horas de Motor",
        "Motorista",
    ]:
        assert col in df.columns, f"coluna esperada ausente: {col}"


def test_csv_metadados_export_date_e_system_source(exporter):
    path = exporter.export_history_to_csv(
        [_record()], "1", 4, 2026, vehicle_plate="TST-0001"
    )
    df = pd.read_csv(path)
    assert "Data de Exportação" in df.columns
    assert "Sistema de Origem" in df.columns
    assert df["Sistema de Origem"].iloc[0] == "wialon"


def test_ignicao_traduzida_para_ligado_desligado(exporter):
    path = exporter.export_history_to_csv(
        [_record(ignition=True), _record(ignition=False)],
        "1",
        4,
        2026,
        vehicle_plate="TST-0001",
    )
    df = pd.read_csv(path)
    assert df["Ignição"].iloc[0] == "Ligado"
    assert df["Ignição"].iloc[1] == "Desligado"


# ---------- Excel ----------


def test_export_excel_gera_arquivo_xlsx(exporter, tmp_path):
    path = exporter.export_history_to_excel(
        [_record()], "1", 4, 2026, vehicle_plate="TST-0001"
    )
    assert path.endswith(".xlsx")
    assert Path(path).is_file()
    df = pd.read_excel(path)
    assert "Latitude" in df.columns


# ---------- Consolidado ----------


def test_consolidado_csv_inclui_multiplos_veiculos(exporter):
    history = {
        "1": [_record(vehicle_id=1, plate="A")],
        "2": [_record(vehicle_id=2, plate="B")],
    }
    info = {
        "1": {"name": "V1", "plate": "A"},
        "2": {"name": "V2", "plate": "B"},
    }
    path = exporter.export_consolidated_history_to_csv(history, 4, 2026, vehicles_info=info)

    df = pd.read_csv(path)
    assert len(df) == 2
    assert set(df["Placa"].tolist()) == {"A", "B"}


# ---------- Listagem de veículos ----------


def test_export_vehicles_to_csv_grava_colunas_basicas(exporter):
    vehicles = [
        {"id": 1, "name": "V1", "plate": "A", "system_source": "wialon"},
        {"id": 2, "name": "V2", "plate": "B", "system_source": "wialon"},
    ]
    path = exporter.export_vehicles_to_csv(vehicles, month=4, year=2026)
    df = pd.read_csv(path)
    assert "ID do Veículo" in df.columns
    assert "Nome do Veículo" in df.columns
    assert "Placa" in df.columns
    assert len(df) == 2


# ---------- Estatísticas ----------


def test_get_export_stats_diretorio_inexistente(exporter):
    stats = exporter.get_export_stats(month=12, year=2099)
    assert stats["exists"] is False
    assert stats["total_files"] == 0


def test_get_export_stats_apos_export(exporter):
    exporter.export_history_to_csv(
        [_record()], "1", 4, 2026, vehicle_plate="TST-0001"
    )
    stats = exporter.get_export_stats(month=4, year=2026)
    assert stats["exists"] is True
    assert stats["csv_files"] >= 1
