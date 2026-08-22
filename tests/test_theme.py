"""Testes da aplicação do tema Movi (Onda 3 Fase 03 — #2)."""

import customtkinter as ctk

from src.gui.design import Colors
from src.gui.theme import apply_movi_theme


def test_apply_movi_theme_pinta_botoes_de_vermelho():
    ctk.set_default_color_theme("blue")
    apply_movi_theme()
    fg = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
    assert fg[0] == Colors.PRIMARY  # claro = vermelho da marca


def test_apply_movi_theme_optionmenu_e_checkbox():
    ctk.set_default_color_theme("blue")
    apply_movi_theme()
    theme = ctk.ThemeManager.theme
    assert theme["CTkOptionMenu"]["fg_color"][0] == Colors.PRIMARY
    assert theme["CTkCheckBox"]["fg_color"][0] == Colors.PRIMARY


def test_apply_movi_theme_progressbar():
    ctk.set_default_color_theme("blue")
    apply_movi_theme()
    assert (
        ctk.ThemeManager.theme["CTkProgressBar"]["progress_color"][0] == Colors.PRIMARY
    )


def test_primary_tokens_existem():
    assert Colors.PRIMARY == "#FF0E10"
    assert Colors.ON_PRIMARY == "#FFFFFF"
