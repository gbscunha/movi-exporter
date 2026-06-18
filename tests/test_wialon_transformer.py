"""
Testes do WialonTransformer.

Cobertura:
- Fase 03: odômetro convertido m→km, preserva 0 km legítimo
- Fase 04: mensagens sem GPS retornam None
- Fase 05 + Fase 16: separação vehicle_voltage (pwr_ext) × internal_battery_voltage (pwr_int)
"""

from unittest.mock import MagicMock

from src.services.wialon_transformer import WialonTransformer


def _make_transformer() -> WialonTransformer:
    client = MagicMock()
    # Sem fórmula aplicada, retorna None — não interfere nos testes de odômetro.
    client.apply_sensor_formula.return_value = None
    return WialonTransformer(client=client)


# ----- Odômetro -----


def test_odometro_converte_metros_para_km():
    """Odômetro vem em metros da API — deve sair em km."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"odometer": 8661339},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["odometer"] == 8661.34


def test_odometro_nulo_quando_param_ausente():
    transformer = _make_transformer()
    msg = {"t": 1700000000, "pos": {"y": -22.87, "x": -43.29, "s": 0}, "p": {}}
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["odometer"] is None


def test_odometro_fallback_para_new_mileage():
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"new_mileage": 5000000},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["odometer"] == 5000.0


def test_odometro_zero_e_preservado_nao_vira_none():
    """0 km é leitura legítima (veículo novo). Não deve virar None."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"odometer": 0},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["odometer"] == 0


# ----- Posição obrigatória -----


def test_transformer_retorna_none_para_mensagem_sem_pos():
    """Mensagens sem GPS não devem virar linha no export (Fase 04)."""
    transformer = _make_transformer()
    msg = {"t": 1700000000, "pos": None, "p": {"pwr_ext": 14.2}}
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record is None


# ----- Tensão do veículo (pwr_ext) × Bateria interna (pwr_int) -----


def test_vehicle_voltage_usa_pwr_ext():
    """pwr_ext é a tensão do veículo."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"pwr_ext": 12.6},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["vehicle_voltage"] == 12.6


def test_vehicle_voltage_nao_faz_fallback_para_pwr_int():
    """Sem pwr_ext, vehicle_voltage deve ser None — NUNCA cair para pwr_int."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"pwr_int": 4.1},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["vehicle_voltage"] is None


def test_internal_battery_usa_pwr_int():
    """pwr_int é a bateria interna do tracker (~4V)."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"pwr_int": 4.1},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["internal_battery_voltage"] == 4.1


def test_internal_battery_usa_voltage_e_battery_como_fallback():
    """Trackers antigos podem reportar a bateria interna como `voltage` ou `battery`."""
    transformer = _make_transformer()

    msg_voltage = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"voltage": 4.2},
    }
    record = transformer.transform_message(msg_voltage, vehicle_id=1, sensor_map={})
    assert record["internal_battery_voltage"] == 4.2

    msg_battery = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"battery": 4.0},
    }
    record = transformer.transform_message(msg_battery, vehicle_id=1, sensor_map={})
    assert record["internal_battery_voltage"] == 4.0


def test_ambos_voltagens_quando_msg_tem_pwr_ext_e_pwr_int():
    """Quando ambos estão presentes, cada um vai para sua coluna."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"pwr_ext": 14.0, "pwr_int": 4.1},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["vehicle_voltage"] == 14.0
    assert record["internal_battery_voltage"] == 4.1


# ----- Ignição por evento (Suntech alert_id) -----


def test_ignicao_por_evento_alert_33_quando_sem_mode():
    """Mensagem Suntech ALT (sem `mode`, com alert_id=33) deve sair ignição ligada."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.8, "x": -43.5, "s": 0},
        "p": {"model": 170, "rep_type": "ALT", "alert_id": 33, "s_asgn2": 13.5},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["ignition"] is True


def test_ignicao_por_evento_alert_34_desliga():
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.8, "x": -43.5, "s": 0},
        "p": {"model": 170, "rep_type": "ALT", "alert_id": 34, "s_asgn2": 13.5},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["ignition"] is False


def test_ignicao_none_quando_sem_mode_e_sem_evento():
    """Sem `mode` e sem alert de ignição → None (será herdado por carry-forward)."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.8, "x": -43.5, "s": 0},
        "p": {"model": 170, "rep_type": "STT", "s_asgn2": 13.5},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["ignition"] is None


def test_ignicao_mode_tem_prioridade_sobre_evento():
    """STT com `mode` resolve direto, sem depender do evento."""
    transformer = _make_transformer()
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.8, "x": -43.5, "s": 0},
        "p": {"model": 170, "rep_type": "STT", "mode": 1},
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["ignition"] is True
