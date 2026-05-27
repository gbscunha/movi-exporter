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
