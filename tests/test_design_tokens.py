"""Testes dos design tokens (Fase 04 da Onda 2)."""

import re

from src.gui.design import Border, Colors, Font, Space

_HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


def test_cores_sao_hex_validas():
    for name in ("SUCCESS", "WARNING", "ERROR", "INFO", "MUTED"):
        value = getattr(Colors, name)
        assert _HEX_RE.match(value), f"{name}={value!r} não é hex de 6 dígitos"


def test_cores_semanticas_sao_distintas():
    """Sucesso, aviso e erro precisam ser cores diferentes entre si."""
    assert len({Colors.SUCCESS, Colors.WARNING, Colors.ERROR}) == 3


def test_espacamentos_crescentes_e_positivos():
    valores = [Space.XS, Space.SM, Space.MD, Space.LG, Space.XL, Space.XXL]
    assert all(isinstance(v, int) and v > 0 for v in valores)
    assert valores == sorted(valores), "espaçamentos devem ser crescentes"


def test_tamanhos_de_fonte_crescentes():
    tamanhos = [
        Font.SIZE_SM,
        Font.SIZE_BASE,
        Font.SIZE_MD,
        Font.SIZE_LG,
        Font.SIZE_XL,
        Font.SIZE_2XL,
    ]
    assert all(isinstance(v, int) and v > 0 for v in tamanhos)
    assert tamanhos == sorted(tamanhos)


def test_pesos_de_fonte():
    assert Font.WEIGHT_NORMAL == "normal"
    assert Font.WEIGHT_BOLD == "bold"


def test_border_radius_positivos():
    for v in (Border.RADIUS_SM, Border.RADIUS_MD, Border.RADIUS_LG):
        assert isinstance(v, int) and v > 0
