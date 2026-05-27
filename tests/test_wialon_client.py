"""Testes do WialonClient.

Fase 11 — capturar username e gis_sid da resposta de login.
"""

from unittest.mock import MagicMock, patch

from src.clients.wialon_client import WialonClient


def _fake_response(json_payload):
    """Constrói um mock de response do requests com o JSON dado."""
    response = MagicMock()
    response.json.return_value = json_payload
    response.raise_for_status.return_value = None
    return response


def test_authenticate_salva_username():
    """Username da conta deve ser salvo após autenticação."""
    payload = {
        "eid": "abc123",
        "au": {"nm": "movi"},
        "gis_sid": "xyz",
        "base_url": "https://hst-api.wialon.com",
    }

    client = WialonClient(token="fake_token")
    with patch.object(client._session, "get", return_value=_fake_response(payload)):
        client.authenticate()

    assert client.username == "movi"


def test_authenticate_salva_gis_sid():
    """gis_sid retornado no login deve ser salvo."""
    payload = {
        "eid": "abc",
        "au": "movi",
        "gis_sid": "gis_abc",
        "base_url": "https://hst-api.wialon.com",
    }

    client = WialonClient(token="fake_token")
    with patch.object(client._session, "get", return_value=_fake_response(payload)):
        client.authenticate()

    assert client.gis_sid == "gis_abc"


def test_authenticate_aceita_au_como_string():
    """Algumas contas retornam 'au' direto como string em vez de dict."""
    payload = {
        "eid": "abc",
        "au": "movi",
        "base_url": "https://hst-api.wialon.com",
    }

    client = WialonClient(token="fake_token")
    with patch.object(client._session, "get", return_value=_fake_response(payload)):
        client.authenticate()

    assert client.username == "movi"


def test_authenticate_username_vazio_se_au_ausente():
    """Sem 'au' na resposta, username deve ficar vazio (sem crash)."""
    payload = {
        "eid": "abc",
        "base_url": "https://hst-api.wialon.com",
    }

    client = WialonClient(token="fake_token")
    with patch.object(client._session, "get", return_value=_fake_response(payload)):
        client.authenticate()

    assert client.username == ""
