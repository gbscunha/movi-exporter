"""
Testes da Fase 02 — bugs rápidos da GUI (C1 e C4).

C1: UploadResult deve ter atributo `uploaded_files` (e não `uploaded_count`).
C4: VehicleService deve propagar `page_size` ao chamar `client.get_history`.
"""

from unittest.mock import MagicMock


def test_upload_result_usa_uploaded_files():
    """C1 — garante que UploadResult tem uploaded_files, não uploaded_count."""
    from src.services.uploader import UploadResult

    result = UploadResult()
    assert hasattr(result, "uploaded_files")
    assert not hasattr(result, "uploaded_count")


def test_pwr_ext_propagado_para_proximo_registro_gps():
    """pwr_ext de mensagem data-only deve aparecer no próximo registro com GPS (Fase 04)."""
    from src.services.vehicle_service import VehicleService

    mock_client = MagicMock()
    mock_client.get_vehicle_sensors.return_value = {}
    mock_client.get_history.return_value = iter(
        [
            [
                {"t": 1700000000, "pos": None, "p": {"pwr_ext": 14.2}},
                {
                    "t": 1700000001,
                    "pos": {"y": -22.87, "x": -43.29, "s": 30},
                    "p": {},
                },
            ]
        ]
    )

    svc = VehicleService(client=mock_client)
    records, _ = svc.process_vehicle_history(
        vehicle={"id": 1, "nm": "Teste"}, month=4, year=2026
    )

    assert len(records) == 1
    assert records[0]["vehicle_voltage"] == 14.2


def test_page_size_propagado_ao_get_history():
    """C4 — garante que WIALON_PAGE_SIZE chega ao client.get_history."""
    from src.core.config import settings
    from src.services.vehicle_service import VehicleService

    mock_client = MagicMock()
    mock_client.get_history.return_value = iter([[]])
    mock_client.get_vehicle_sensors.return_value = {}

    svc = VehicleService(client=mock_client)
    svc.process_vehicle_history(
        vehicle={"id": 1, "nm": "Teste"}, month=4, year=2026
    )

    call = mock_client.get_history.call_args
    assert call is not None
    # page_size deve vir como kwarg explícito, propagado do settings
    assert "page_size" in call.kwargs
    assert call.kwargs["page_size"] == (settings.WIALON_PAGE_SIZE or 1000)


def _service_with_one_vehicle(export_format, tmp_path):
    """VehicleService mockado que processa 1 veículo com 1 registro GPS."""
    from src.services.vehicle_service import VehicleService

    mock_client = MagicMock()
    mock_client.list_vehicles.return_value = [
        {"id": 1, "nm": "Teste", "_plate": "ABC1234"}
    ]
    mock_client.get_vehicle_sensors.return_value = {}
    mock_client.get_history.return_value = iter(
        [[{"t": 1775000000, "pos": {"y": -22.8, "x": -43.2, "s": 10}, "p": {}}]]
    )
    svc = VehicleService(client=mock_client, export_dir=str(tmp_path))
    return svc


def test_consolidado_sempre_csv_mesmo_com_formato_xlsx(tmp_path):
    """Consolidado deve sair em CSV mesmo quando o formato escolhido é xlsx.

    O xlsx tem limite de ~1M linhas; o consolidado da frota estoura isso.
    """
    svc = _service_with_one_vehicle("xlsx", tmp_path)
    result = svc.export_monthly_data(
        month=4, year=2026, export_format="xlsx", consolidated=True
    )
    consolidados = [f for f in result.exported_files if "Consolidado" in f]
    assert consolidados, "deveria ter gerado um consolidado"
    assert all(f.endswith(".csv") for f in consolidados), (
        f"consolidado deveria ser .csv, veio: {consolidados}"
    )
    # E NÃO deve haver consolidado .xlsx
    assert not any(
        "Consolidado" in f and f.endswith(".xlsx") for f in result.exported_files
    )


def test_on_progress_emitido_por_veiculo(tmp_path):
    """on_progress deve ser chamado uma vez por veículo, com (atual, total, nome)."""
    from src.services.vehicle_service import VehicleService

    mock_client = MagicMock()
    mock_client.list_vehicles.return_value = [
        {"id": i, "nm": f"V{i}", "_plate": f"P{i}"} for i in range(1, 4)
    ]
    mock_client.get_vehicle_sensors.return_value = {}
    mock_client.get_history.return_value = iter(
        [[{"t": 1775000000, "pos": {"y": -22, "x": -43, "s": 5}, "p": {}}]]
    )
    calls = []
    svc = VehicleService(client=mock_client, export_dir=str(tmp_path))
    svc.export_monthly_data(
        month=4, year=2026, export_format="csv", consolidated=False,
        on_progress=lambda c, t, n: calls.append((c, t, n)),
    )
    assert calls == [(1, 3, "V1"), (2, 3, "V2"), (3, 3, "V3")]


def test_export_sem_on_progress_funciona(tmp_path):
    """on_progress é opcional — ausência não deve quebrar o export."""
    svc = _service_with_one_vehicle("csv", tmp_path)
    result = svc.export_monthly_data(month=4, year=2026, consolidated=False)
    assert result.processed_vehicles == 1


def test_export_consolidated_excel_aborta_acima_do_limite(tmp_path):
    """Guard defensivo: chamar o consolidado-xlsx acima do limite retorna '' (não estoura)."""
    from src.services import exporter as exporter_mod
    from src.services.exporter import DataExporter

    exp = DataExporter(base_export_dir=str(tmp_path))
    # Monkeypatch do limite para um valor pequeno, evitando criar milhões de dicts.
    original = exporter_mod.EXCEL_MAX_ROWS
    exporter_mod.EXCEL_MAX_ROWS = 3
    try:
        history = {
            "1": [
                {
                    "vehicle_id": 1, "timestamp": f"2026-04-01T00:0{i}:00",
                    "latitude": 0, "longitude": 0, "speed": 0, "ignition": False,
                    "system_source": "wialon",
                }
                for i in range(5)  # 5 registros > limite (3)
            ]
        }
        path = exp.export_consolidated_history_to_excel(history, 4, 2026)
        assert path == "", "deveria abortar (retornar '') acima do limite"
    finally:
        exporter_mod.EXCEL_MAX_ROWS = original
