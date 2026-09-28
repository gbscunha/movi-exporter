"""Testes da tela de Configurações — persistência dos campos do rodapé."""

import pytest

from src.gui.frames import settings as settings_module
from src.gui.frames.settings import SettingsFrame


@pytest.fixture
def frame_sem_efeitos(ctk_root, monkeypatch):
    """SettingsFrame com escrita no .env e toasts interceptados."""
    gravados: dict[str, str] = {}

    monkeypatch.setattr(
        settings_module,
        "set_env_value",
        lambda key, value: gravados.__setitem__(key, value),
    )
    monkeypatch.setattr(settings_module.settings, "reload", lambda: None)
    monkeypatch.setattr(settings_module.toast, "show", lambda *a, **k: None)

    frame = SettingsFrame(ctk_root)
    return frame, gravados


def test_alterar_id_da_pasta_habilita_salvar(frame_sem_efeitos):
    """Digitar um ID novo marca alterações pendentes no rodapé."""
    frame, _ = frame_sem_efeitos

    frame.folder_entry.delete(0, "end")
    frame.folder_entry.insert(0, "1AbCdEfGhIjK")
    frame._recompute_dirty()

    assert frame.save_changes_btn.cget("state") == "normal"


def test_salvar_persiste_id_da_pasta_do_drive(frame_sem_efeitos):
    """'Salvar alterações' grava o ID da pasta no .env."""
    frame, gravados = frame_sem_efeitos

    frame.folder_entry.delete(0, "end")
    frame.folder_entry.insert(0, "1AbCdEfGhIjK")
    frame._recompute_dirty()
    frame._save_changes()

    assert gravados.get("GOOGLE_DRIVE_FOLDER_ID") == "1AbCdEfGhIjK"


def test_apos_salvar_nao_ha_alteracao_pendente(frame_sem_efeitos):
    """Salvo o ID, o rodapé volta ao estado limpo (sem pendência)."""
    frame, _ = frame_sem_efeitos

    frame.folder_entry.delete(0, "end")
    frame.folder_entry.insert(0, "1AbCdEfGhIjK")
    frame._recompute_dirty()
    frame._save_changes()

    assert frame.save_changes_btn.cget("state") == "disabled"
    assert frame.unsaved_label.cget("text") == ""


def test_testar_token_com_sucesso_guarda_o_nome_do_usuario(ctk_root, monkeypatch):
    """O nome de quem autenticou alimenta o seletor de conta e o cache do .env."""
    from src.gui import account_state as account_state_module
    from src.gui.account_state import AccountState

    gravados: dict[str, str] = {}
    monkeypatch.setattr(
        account_state_module,
        "set_env_value",
        lambda key, value: gravados.__setitem__(key, value),
    )
    monkeypatch.setattr(settings_module, "set_env_value", lambda key, value: None)
    monkeypatch.setattr(settings_module.settings, "reload", lambda: None)
    monkeypatch.setattr(settings_module.toast, "show", lambda *a, **k: None)

    monkeypatch.setattr(settings_module.settings, "WIALON_TOKEN_2", "token-salvo")

    state = AccountState()
    frame = SettingsFrame(ctk_root, account_state=state)
    frame._on_token_test_ok(2, "lcmovi_adm")

    assert state.username(2) == "lcmovi_adm"
    assert gravados == {"WIALON_USER_2": "lcmovi_adm"}


def test_testar_token_ainda_nao_salvo_nao_guarda_o_nome(ctk_root, monkeypatch):
    """Testar um token colado mas não salvo mostraria no seletor outro usuário."""
    from src.gui import account_state as account_state_module
    from src.gui.account_state import AccountState

    gravados: dict[str, str] = {}
    monkeypatch.setattr(
        account_state_module,
        "set_env_value",
        lambda key, value: gravados.__setitem__(key, value),
    )
    monkeypatch.setattr(settings_module, "set_env_value", lambda key, value: None)
    monkeypatch.setattr(settings_module.settings, "reload", lambda: None)
    monkeypatch.setattr(settings_module.toast, "show", lambda *a, **k: None)
    monkeypatch.setattr(settings_module.settings, "WIALON_TOKEN_2", "token-salvo")

    state = AccountState()
    frame = SettingsFrame(ctk_root, account_state=state)
    frame._token_widgets[2]["entry"].delete(0, "end")
    frame._token_widgets[2]["entry"].insert(0, "token-novo-ainda-nao-salvo")
    frame._on_token_test_ok(2, "outro_usuario")

    assert state.username(2) == ""
    assert gravados == {}


def test_testar_token_sem_nome_nao_quebra(frame_sem_efeitos):
    """Autenticação que não devolveu nome só mostra 'Conectado'."""
    frame, _ = frame_sem_efeitos

    frame._on_token_test_ok(1, "")

    assert frame._token_widgets[1]["status_label"].cget("text") == "Status: Conectado"
