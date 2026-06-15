"""Fixtures compartilhadas dos testes."""

import pytest


@pytest.fixture
def ctk_root():
    """Janela CTk oculta para testes que criam widgets/imagens.

    CTkImage usa PIL.ImageTk.PhotoImage, que exige um root Tk inicializado.
    Pula o teste automaticamente em ambientes sem display (CI headless).
    """
    import customtkinter as ctk

    from src.gui import icons

    try:
        root = ctk.CTk()
    except Exception as exc:  # noqa: BLE001 — sem display disponível
        pytest.skip(f"Tk indisponível neste ambiente: {exc}")

    # O cache de imagens do icons guarda CTkImage ligados a um root Tk.
    # Entre testes o root é destruído, então limpamos o cache para não
    # reutilizar imagens órfãs (no app real há um único root vitalício).
    icons._image_cache.clear()

    root.withdraw()
    yield root
    icons._image_cache.clear()
    root.destroy()
