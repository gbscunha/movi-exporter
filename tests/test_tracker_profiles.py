"""Testes dos perfis de tracker (Fase 17).

Cada perfil isola o dialeto de um fabricante. Testamos cada um em isolamento
e a função de detecção que escolhe qual aplicar para uma mensagem.
"""

from src.services.tracker_profiles import (
    DEFAULT_PROFILES,
    DefaultProfile,
    SuntechProfile,
    detect_profile,
)


# ---------- Detecção ----------


def test_detect_suntech_por_model_197():
    msg = {"pos": {}, "p": {"model": 197, "s_asgn1": 28.0}}
    assert isinstance(detect_profile(msg), SuntechProfile)


def test_detect_suntech_por_rep_type_stt():
    """Modelos Suntech além do 197 devem cair pelo rep_type=STT."""
    msg = {"pos": {}, "p": {"rep_type": "STT", "s_asgn1": 28.0}}
    assert isinstance(detect_profile(msg), SuntechProfile)


def test_detect_default_quando_msg_generica():
    msg = {"pos": {}, "p": {"pwr_ext": 12.6, "in": 1}}
    assert isinstance(detect_profile(msg), DefaultProfile)


def test_detect_default_quando_params_vazios():
    msg = {"pos": {}, "p": {}}
    assert isinstance(detect_profile(msg), DefaultProfile)


def test_detect_default_quando_message_sem_p():
    msg = {"pos": {}}
    assert isinstance(detect_profile(msg), DefaultProfile)


def test_ordem_dos_perfis_suntech_antes_de_default():
    """DefaultProfile sempre dá match — Suntech tem que vir antes."""
    assert DEFAULT_PROFILES[-1].__class__ is DefaultProfile
    classes_antes = [type(p) for p in DEFAULT_PROFILES[:-1]]
    assert SuntechProfile in classes_antes


# ---------- DefaultProfile ----------


def test_default_known_params_separa_voltagens():
    """pwr_ext (veículo) e pwr_int (tracker) devem ir para colunas distintas."""
    profile = DefaultProfile()
    params = profile.known_params()
    assert params["vehicle_voltage"] == ["pwr_ext"]
    assert "pwr_int" in params["internal_battery_voltage"]
    assert "pwr_int" not in params["vehicle_voltage"]


def test_default_extract_odometer_metros():
    profile = DefaultProfile()
    assert profile.extract_odometer_meters({"odometer": 1234567}) == 1234567.0


def test_default_extract_odometer_zero_e_preservado():
    """0 km é leitura legítima (veículo novo) — não deve virar None."""
    profile = DefaultProfile()
    assert profile.extract_odometer_meters({"odometer": 0}) == 0.0


def test_default_extract_odometer_fallback_new_mileage():
    profile = DefaultProfile()
    assert profile.extract_odometer_meters({"new_mileage": 5000000}) == 5000000.0


def test_default_extract_odometer_none_quando_ausente():
    profile = DefaultProfile()
    assert profile.extract_odometer_meters({}) is None


# ---------- SuntechProfile ----------


def test_suntech_matches_model_197():
    profile = SuntechProfile()
    assert profile.matches({"p": {"model": 197}}) is True


def test_suntech_matches_rep_type_stt_sem_model():
    profile = SuntechProfile()
    assert profile.matches({"p": {"rep_type": "STT"}}) is True


def test_suntech_nao_matches_msg_generica():
    profile = SuntechProfile()
    assert profile.matches({"p": {"pwr_ext": 12.0}}) is False


def test_suntech_ignicao_em_mode():
    """Suntech ST380 usa `mode` (1/0) em vez de `in`/`in1`."""
    profile = SuntechProfile()
    assert profile.known_params()["ignition"] == ["mode"]


def test_suntech_voltagens_separadas_s_asgn1_s_asgn2():
    profile = SuntechProfile()
    params = profile.known_params()
    assert params["vehicle_voltage"] == ["s_asgn1"]
    assert params["internal_battery_voltage"] == ["s_asgn2"]


def test_suntech_odometro_em_m_asgn1():
    profile = SuntechProfile()
    # m_asgn1 vem em metros (240131878 = 240131.878 km)
    assert profile.extract_odometer_meters({"m_asgn1": 240131878}) == 240131878.0


def test_suntech_odometro_zero_preservado():
    """Veículo novo Suntech: m_asgn1=0 não é dado ausente."""
    profile = SuntechProfile()
    assert profile.extract_odometer_meters({"m_asgn1": 0}) == 0.0


def test_suntech_odometro_fallback_odometer_se_admin_configurou():
    """Se admin do Wialon configurou sensor com nome `odometer`, aceitar."""
    profile = SuntechProfile()
    assert profile.extract_odometer_meters({"odometer": 5000}) == 5000.0


def test_suntech_odometro_prefere_m_asgn1_sobre_odometer():
    """Quando ambos existem, m_asgn1 é a fonte canônica do Suntech."""
    profile = SuntechProfile()
    result = profile.extract_odometer_meters({"m_asgn1": 240131878, "odometer": 5000})
    assert result == 240131878.0


def test_suntech_odometro_none_quando_ausente():
    profile = SuntechProfile()
    assert profile.extract_odometer_meters({}) is None
