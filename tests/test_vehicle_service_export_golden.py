"""Testes de caracterização (golden) de `export_monthly_data`.

Capturam o comportamento atual da orquestração antes da Fase 6 (quebra do
método em sub-métodos). Servem de rede de segurança: a saída agregada e os
arquivos gerados não podem mudar com o refactor.
"""

import pandas as pd
from unittest.mock import MagicMock

from src.clients.wialon_client import WialonError
from src.services.vehicle_service import VehicleService


def _gps_page():
    """Uma página com um registro GPS simples (sensores ausentes → N/D)."""
    return [[{"t": 1775000000, "pos": {"y": -22.8, "x": -43.2, "s": 10}, "p": {}}]]


def test_resultado_agregado_lote_misto(tmp_path):
    """Lote com sucesso + sem-registros + erro: confere o ExportResult agregado."""
    mock_client = MagicMock()
    mock_client.list_vehicles.return_value = [
        {"id": 1, "nm": "V1", "_plate": "AAA1111"},
        {"id": 2, "nm": "V2", "_plate": "BBB2222"},
        {"id": 3, "nm": "V3", "_plate": "CCC3333"},
    ]
    mock_client.get_vehicle_sensors.return_value = {}
    # v1: 1 registro GPS | v2: página vazia (sem registros) | v3: erro Wialon
    mock_client.get_history.side_effect = [
        iter(_gps_page()),
        iter([[]]),
        WialonError("falha simulada"),
    ]

    svc = VehicleService(client=mock_client, export_dir=str(tmp_path))
    result = svc.export_monthly_data(
        month=4, year=2026, export_format="csv", consolidated=True
    )

    assert result.total_vehicles == 3
    assert result.processed_vehicles == 2  # v1 (com arquivo) + v2 (sem registros)
    assert result.failed_vehicles == 1  # v3
    assert result.total_records == 1  # só v1

    individuais = [f for f in result.exported_files if "Consolidado" not in f]
    consolidados = [f for f in result.exported_files if "Consolidado" in f]
    assert len(individuais) == 1  # só v1 gerou arquivo individual
    assert len(consolidados) == 1
    assert consolidados[0].endswith(".csv")

    # O consolidado contém apenas o veículo processado com registros (v1).
    df = pd.read_csv(consolidados[0])
    assert set(df["ID do Veículo"].unique()) == {1}


def test_conta_sem_veiculos(tmp_path):
    """Conta sem veículos: resultado zerado e nenhum arquivo."""
    mock_client = MagicMock()
    mock_client.list_vehicles.return_value = []

    svc = VehicleService(client=mock_client, export_dir=str(tmp_path))
    result = svc.export_monthly_data(month=4, year=2026, consolidated=True)

    assert result.total_vehicles == 0
    assert result.processed_vehicles == 0
    assert result.failed_vehicles == 0
    assert result.exported_files == []


def test_formato_both_gera_csv_e_xlsx_individuais(tmp_path):
    """format='both' gera CSV + XLSX por veículo e consolidado em CSV."""
    mock_client = MagicMock()
    mock_client.list_vehicles.return_value = [
        {"id": 1, "nm": "V1", "_plate": "AAA1111"}
    ]
    mock_client.get_vehicle_sensors.return_value = {}
    mock_client.get_history.side_effect = lambda *a, **k: iter(_gps_page())

    svc = VehicleService(client=mock_client, export_dir=str(tmp_path))
    result = svc.export_monthly_data(
        month=4, year=2026, export_format="both", consolidated=True
    )

    individuais = [f for f in result.exported_files if "Consolidado" not in f]
    consolidados = [f for f in result.exported_files if "Consolidado" in f]
    assert len(individuais) == 2
    assert sum(f.endswith(".csv") for f in individuais) == 1
    assert sum(f.endswith(".xlsx") for f in individuais) == 1
    assert len(consolidados) == 1 and consolidados[0].endswith(".csv")


def test_nd_no_arquivo_individual_pipeline_completo(tmp_path):
    """N/D deve aparecer no arquivo individual quando sensores estão ausentes."""
    mock_client = MagicMock()
    mock_client.list_vehicles.return_value = [
        {"id": 1, "nm": "V1", "_plate": "AAA1111"}
    ]
    mock_client.get_vehicle_sensors.return_value = {}
    mock_client.get_history.side_effect = lambda *a, **k: iter(_gps_page())

    svc = VehicleService(client=mock_client, export_dir=str(tmp_path))
    result = svc.export_monthly_data(
        month=4, year=2026, export_format="csv", consolidated=False
    )

    individuais = [f for f in result.exported_files if "Consolidado" not in f]
    assert len(individuais) == 1
    df = pd.read_csv(individuais[0])
    # Sensores ausentes saem como "N/D" (não vazio).
    assert df["RPM"][0] == "N/D"
    assert df["Motorista"][0] == "N/D"
