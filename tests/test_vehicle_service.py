"""
Testes da Fase 02 — bugs rápidos da GUI (C1 e C4).

C1: UploadResult deve ter atributo `uploaded_files` (e não `uploaded_count`).
C4: VehicleService deve propagar `page_size` ao chamar `client.get_history`.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Garante que `src` é importável quando rodando direto via pytest.
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_upload_result_usa_uploaded_files():
    """C1 — garante que UploadResult tem uploaded_files, não uploaded_count."""
    from src.services.uploader import UploadResult

    result = UploadResult()
    assert hasattr(result, "uploaded_files")
    assert not hasattr(result, "uploaded_count")


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
