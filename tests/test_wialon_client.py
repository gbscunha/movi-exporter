"""Testes do WialonClient.

Fase 11 — capturar username e gis_sid da resposta de login.
"""

import json
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
    assert (
        _client()._normalize_sensor_name("Bateria do dispositivo")
        == "internal_battery_voltage"
    )


def test_normalize_sensor_bateria_do_rastreador_vai_para_interna():
    assert (
        _client()._normalize_sensor_name("Bateria do rastreador")
        == "internal_battery_voltage"
    )


def test_normalize_sensor_bateria_interna_vai_para_interna():
    assert (
        _client()._normalize_sensor_name("Bateria Interna")
        == "internal_battery_voltage"
    )


def test_normalize_sensor_bateria_dispositivo_sem_do_vai_para_interna():
    """Bug real (model 170): admin escreveu 'Bateria dispositivo' (sem 'do').

    Antes caía no genérico 'bateria' → vehicle_voltage (errado). Agora a
    palavra-chave 'dispositivo' garante internal_battery_voltage.
    """
    assert (
        _client()._normalize_sensor_name("Bateria dispositivo")
        == "internal_battery_voltage"
    )


def test_normalize_sensor_device_battery_vai_para_interna():
    assert (
        _client()._normalize_sensor_name("Device Battery") == "internal_battery_voltage"
    )


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
    assert (
        _client()._normalize_sensor_name("Acionamento de Prancha")
        == "acionamento_de_prancha"
    )


# ----- _extract_plate — fallback pro nome da unidade quando falta o profile field -----


def test_extract_plate_usa_profile_field_quando_presente():
    """Profile field `registration_plate` é a fonte oficial e tem prioridade."""
    item = {
        "id": 1,
        "nm": "FXI2D14",
        "pflds": {"1": {"n": "registration_plate", "v": "ABC1234"}},
    }
    assert _client()._extract_plate(item) == "ABC1234"


def test_extract_plate_fallback_para_nome_da_unidade():
    """Sem profile field, usa o nome da unidade (`nm`) como placa.

    Reproduz o caso real da Conta 2: veículo sem `registration_plate`
    cadastrado, mas nomeado 'FXI2D14' na Wialon — arquivo exportado caía pro
    ID em vez da placa. Na Conta 1, Nome do Veículo e Placa sempre batem
    (confirmado nos exports reais), então o nome é um fallback confiável.
    """
    item = {"id": 402367464, "nm": "FXI2D14", "pflds": {}}
    assert _client()._extract_plate(item) == "FXI2D14"


def test_extract_plate_sem_profile_field_e_sem_nome_fica_none():
    item = {"id": 4, "nm": "", "pflds": {}}
    assert _client()._extract_plate(item) is None


# ----- list_drivers — mapa código RFID → nome (Fase 01, Motorista RFID) -----


def test_list_drivers_monta_mapa_codigo_para_nome():
    """Payload com 2 resources e N motoristas → mapa {código: nome} completo."""
    payload = {
        "items": [
            {
                "nm": "Resource A",
                "drvrs": {
                    "1": {"id": 1, "c": "9310401", "n": "ALDO LOPES"},
                    "2": {"id": 2, "c": "9310402", "n": "MARIA SOUZA"},
                },
            },
            {
                "nm": "Resource B",
                "drvrs": {"5": {"id": 5, "c": "7001", "n": "JOÃO LIMA"}},
            },
        ]
    }
    client = _client()
    with patch.object(client, "_request", return_value=payload):
        drivers = client.list_drivers()

    assert drivers == {
        "9310401": "ALDO LOPES",
        "9310402": "MARIA SOUZA",
        "7001": "JOÃO LIMA",
    }


def test_list_drivers_ignora_codigo_vazio():
    """Motorista sem código (`c` vazio/ausente) não entra no mapa."""
    payload = {
        "items": [
            {
                "drvrs": {
                    "1": {"c": "", "n": "SEM CARTÃO"},
                    "2": {"n": "SEM CODIGO"},
                    "3": {"c": "555", "n": "COM CARTÃO"},
                }
            }
        ]
    }
    client = _client()
    with patch.object(client, "_request", return_value=payload):
        drivers = client.list_drivers()

    assert drivers == {"555": "COM CARTÃO"}


def test_list_drivers_resource_sem_drivers_retorna_vazio():
    """Resource sem `drvrs` (ACL ausente ou sem motoristas) não quebra."""
    payload = {"items": [{"nm": "Resource sem motoristas"}]}
    client = _client()
    with patch.object(client, "_request", return_value=payload):
        drivers = client.list_drivers()

    assert drivers == {}


def test_list_drivers_aceita_drvrs_como_lista():
    """Alguns retornos trazem `drvrs` como lista em vez de dict."""
    payload = {"items": [{"drvrs": [{"c": "111", "n": "A"}, {"c": "222", "n": "B"}]}]}
    client = _client()
    with patch.object(client, "_request", return_value=payload):
        drivers = client.list_drivers()

    assert drivers == {"111": "A", "222": "B"}


def test_list_drivers_usa_cache_na_segunda_chamada():
    """Segunda chamada usa cache — não repete o request."""
    payload = {"items": [{"drvrs": {"1": {"c": "9", "n": "X"}}}]}
    client = _client()
    with patch.object(client, "_request", return_value=payload) as mock_req:
        first = client.list_drivers()
        second = client.list_drivers()

    assert first == second == {"9": "X"}
    assert mock_req.call_count == 1


# ----- get_addresses_batch — geocodificação reversa (Feature Endereço) -----


def _geo_client():
    """Client pronto para geocodificar (uid + url setados, sem autenticar)."""
    c = WialonClient(token="fake_token")
    c.uid = 999
    c.gis_geocode_url = "https://geocode-maps.wialon.us/hst-api.wialon.us/gis_geocode"
    return c


def test_get_addresses_batch_retorna_enderecos_na_ordem():
    c = _geo_client()
    coords = [{"lon": -46.6, "lat": -23.5}, {"lon": -43.3, "lat": -22.8}]
    with patch.object(
        c._session,
        "post",
        return_value=_fake_response(["Av. Paulista, SP", "Rua X, RJ"]),
    ):
        addrs = c.get_addresses_batch(coords)
    assert addrs == ["Av. Paulista, SP", "Rua X, RJ"]


def test_get_addresses_batch_string_vazia_vira_none():
    c = _geo_client()
    with patch.object(c._session, "post", return_value=_fake_response(["Rua X", ""])):
        addrs = c.get_addresses_batch([{"lon": 1, "lat": 1}, {"lon": 2, "lat": 2}])
    assert addrs == ["Rua X", None]


def test_get_addresses_batch_coords_vazio_nao_chama_api():
    c = _geo_client()
    with patch.object(c._session, "post") as mock_post:
        assert c.get_addresses_batch([]) == []
    mock_post.assert_not_called()


def test_get_addresses_batch_sem_uid_retorna_none():
    c = _geo_client()
    c.uid = None
    with patch.object(c._session, "post") as mock_post:
        addrs = c.get_addresses_batch([{"lon": 1, "lat": 1}, {"lon": 2, "lat": 2}])
    assert addrs == [None, None]
    mock_post.assert_not_called()


def test_get_addresses_batch_erro_api_retorna_none():
    c = _geo_client()
    with patch.object(c._session, "post", return_value=_fake_response({"error": 7})):
        addrs = c.get_addresses_batch([{"lon": 1, "lat": 1}])
    assert addrs == [None]


def test_get_addresses_batch_usa_post_com_uid_e_flags():
    """Confere o contrato: POST com coords/flags/uid — sem gis_sid/search_provider."""
    c = _geo_client()
    with patch.object(
        c._session, "post", return_value=_fake_response(["Rua X"])
    ) as mock_post:
        c.get_addresses_batch([{"lon": -43.3, "lat": -22.8}])
    _, kwargs = mock_post.call_args
    body = kwargs["data"]
    assert body["uid"] == 999
    assert body["flags"] == WialonClient.GEOCODE_FLAGS
    assert "gis_sid" not in body and "search_provider" not in body
    assert '"lon": -43.3' in body["coords"] or '"lon":-43.3' in body["coords"]


def test_get_addresses_batch_divide_em_lotes():
    """Mais que GEOCODE_BATCH_SIZE coords → múltiplos POSTs, ordem preservada."""
    c = _geo_client()
    n = WialonClient.GEOCODE_BATCH_SIZE + 10
    coords = [{"lon": i, "lat": i} for i in range(n)]

    def fake_post(url, data=None, timeout=None):
        enviados = json.loads(data["coords"])
        return _fake_response([f"addr{c['lon']}" for c in enviados])

    with patch.object(c._session, "post", side_effect=fake_post) as mock_post:
        addrs = c.get_addresses_batch(coords)

    assert mock_post.call_count == 2  # 1000 + 10
    assert len(addrs) == n
    assert addrs[0] == "addr0" and addrs[-1] == f"addr{n - 1}"
