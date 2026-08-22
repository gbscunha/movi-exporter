"""Testes do helper de ícones FontAwesome (Onda 3 Fase 01)."""

import customtkinter as ctk

from src.gui import icons


def test_fonte_disponivel():
    """O TTF do FontAwesome deve estar vendorizado no bundle."""
    assert icons.is_available(), "fontawesome-solid.ttf não encontrado em assets"


def test_constantes_sao_glifos_de_um_caractere():
    """Cada constante de ícone é um único caractere no range FontAwesome."""
    nomes = [
        "PLUG",
        "EYE",
        "EYE_SLASH",
        "SAVE",
        "SEARCH",
        "FOLDER_OPEN",
        "FOLDER",
        "PLAY",
        "REFRESH",
        "LIST",
        "GEAR",
        "HOME",
        "FILE_EXPORT",
        "UPLOAD",
        "CLOUD",
        "CIRCLE_CHECK",
        "CIRCLE_XMARK",
        "TRIANGLE_WARNING",
        "COPY",
        "LINK",
        "TRUCK",
        "CALENDAR",
    ]
    for nome in nomes:
        glifo = getattr(icons, nome)
        assert isinstance(glifo, str) and len(glifo) == 1, f"{nome} inválido"
        # FontAwesome usa a Private Use Area (a partir de U+E000).
        assert ord(glifo) >= 0xE000, f"{nome} fora da PUA: {hex(ord(glifo))}"


def test_get_retorna_ctkimage(ctk_root):
    img = icons.get(icons.SAVE)
    assert isinstance(img, ctk.CTkImage)


def test_get_cacheia_por_parametros(ctk_root):
    """Mesmos parâmetros → mesma instância (cache)."""
    a = icons.get(icons.SAVE, size=18)
    b = icons.get(icons.SAVE, size=18)
    assert a is b


def test_get_cores_distintas_geram_imagens_distintas(ctk_root):
    verde = icons.get(icons.CIRCLE_CHECK, color="#2ecc71")
    vermelho = icons.get(icons.CIRCLE_XMARK, color="#e74c3c")
    assert verde is not vermelho


def test_get_tamanhos_distintos_geram_imagens_distintas(ctk_root):
    p = icons.get(icons.SAVE, size=14)
    g = icons.get(icons.SAVE, size=24)
    assert p is not g
