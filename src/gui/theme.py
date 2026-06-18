"""Aplicação da identidade visual Movi sobre o tema do CustomTkinter.

O CTk carrega um tema base ("blue") cujo acento é azul. Aqui sobrescrevemos
as cores de acento de cada widget para o vermelho da marca Movi (#FF0E10),
preservando o resto do tema (fundos, bordas neutras, etc).

Cada valor no tema do CTk é um par [claro, escuro]. Usamos o vermelho da
marca no modo claro e um tom levemente mais escuro no modo escuro, seguindo
a convenção do próprio CTk (acento mais vivo no claro, mais sóbrio no escuro).

Chamar `apply_movi_theme()` UMA vez após `set_default_color_theme`, antes de
criar qualquer widget.
"""

import customtkinter as ctk

from src.gui.design import Colors

# Pares [claro, escuro] derivados do vermelho da marca.
_RED = [Colors.PRIMARY, Colors.PRIMARY_HOVER]  # fg principal
_RED_HOVER = [Colors.PRIMARY_HOVER, "#9E0A0B"]  # hover/pressed
_ON_RED = [Colors.ON_PRIMARY, Colors.ON_PRIMARY]  # texto sobre o vermelho


def apply_movi_theme() -> None:
    """Sobrescreve o acento azul do CTk pelo vermelho Movi em todos os widgets."""
    theme = ctk.ThemeManager.theme

    def _set(widget: str, **overrides) -> None:
        if widget in theme:
            theme[widget].update(overrides)

    _set("CTkButton", fg_color=_RED, hover_color=_RED_HOVER, text_color=_ON_RED)
    _set(
        "CTkOptionMenu",
        fg_color=_RED,
        button_color=_RED_HOVER,
        button_hover_color=_RED_HOVER,
        text_color=_ON_RED,
    )
    _set("CTkCheckBox", fg_color=_RED, hover_color=_RED_HOVER, checkmark_color=_ON_RED)
    _set("CTkRadioButton", fg_color=_RED, hover_color=_RED_HOVER)
    _set("CTkSlider", button_color=_RED, button_hover_color=_RED_HOVER)
    _set("CTkProgressBar", progress_color=_RED)
    _set(
        "CTkSegmentedButton",
        selected_color=_RED,
        selected_hover_color=_RED_HOVER,
        text_color=_ON_RED,
    )
