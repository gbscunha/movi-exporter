"""Fixtures compartilhadas dos testes."""

import pytest


@pytest.fixture
def ctk_root():
    """Janela CTk oculta para testes que criam widgets/imagens.

    CTkImage usa PIL.ImageTk.PhotoImage, que exige um root Tk inicializado.
    Pula o teste automaticamente em ambientes sem display (CI headless).
    """
    import customtkinter as ctk

    try:
        root = ctk.CTk()
    except Exception as exc:  # noqa: BLE001 — sem display disponível
        pytest.skip(f"Tk indisponível neste ambiente: {exc}")

    root.withdraw()
    yield root
    root.destroy()
