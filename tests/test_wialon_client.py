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


# ----- _normalize_sensor_name — separação tensão do veículo × bateria interna -----


def _client():
    """WialonClient com token fake (não autentica)."""
    return WialonClient(token="fake_token")


def test_normalize_sensor_bateria_do_dispositivo_vai_para_interna():
    """Cliente Movi nomeou 'Bateria do dispositivo' no Wialon — bug visto no QA.

    'bateria' sozinha vinha capturando antes de chegar em 'dispositivo'
    e o sensor s_asgn2 (4.1V, bateria interna do tracker) acabava mapeado
    para vehicle_voltage. Esse teste blinda a ordem.
    """
    assert _client()._normalize_sensor_name("Bateria do dispositivo") == "internal_battery_voltage"


def test_normalize_sensor_bateria_do_rastreador_vai_para_interna():
    assert _client()._normalize_sensor_name("Bateria do rastreador") == "internal_battery_voltage"


def test_normalize_sensor_bateria_interna_vai_para_interna():
    assert _client()._normalize_sensor_name("Bateria Interna") == "internal_battery_voltage"


def test_normalize_sensor_device_battery_vai_para_interna():
    assert _client()._normalize_sensor_name("Device Battery") == "internal_battery_voltage"


def test_normalize_sensor_bateria_do_veiculo_vai_para_vehicle():
    """Cliente Movi nomeou 'Bateria do veículo' no Wialon — caso real."""
    assert _client()._normalize_sensor_name("Bateria do veículo") == "vehicle_voltage"


def test_normalize_sensor_bateria_externa_vai_para_vehicle():
    """Cliente Movi (CVM0H79, Jimi VL03) nomeou 'Bateria Externa' no Wialon."""
    assert _client()._normalize_sensor_name("Bateria Externa") == "vehicle_voltage"


def test_normalize_sensor_tensao_do_veiculo_vai_para_vehicle():
    assert _client()._normalize_sensor_name("Tensão do veículo") == "vehicle_voltage"


def test_normalize_sensor_bateria_generica_cai_em_vehicle():
    """Quando admin nomeia apenas 'Bateria' (ambíguo), assumir tensão do veículo."""
    assert _client()._normalize_sensor_name("Bateria") == "vehicle_voltage"


def test_normalize_sensor_ignicao():
    assert _client()._normalize_sensor_name("Ignição") == "ignition"
    assert _client()._normalize_sensor_name("Ignicao") == "ignition"


def test_normalize_sensor_combustivel():
    assert _client()._normalize_sensor_name("Nível Combustível") == "fuel_level"
    assert _client()._normalize_sensor_name("Fuel Tank") == "fuel_level"


def test_normalize_sensor_nome_desconhecido_vira_snake_case():
    """Nomes sem correspondência ficam como snake_case do nome original."""
    assert _client()._normalize_sensor_name("Acionamento de Prancha") == "acionamento_de_prancha"
