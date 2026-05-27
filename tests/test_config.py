"""Testes do Settings.reload() e suporte a WIALON_TOKEN_2.

Fase 09 — recarregamento em memória do .env e segunda conta Wialon.
"""

import sys
from pathlib import Path

# Garante que `src` é importável quando rodando direto via pytest.
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_reload_carrega_novo_token(tmp_path, monkeypatch):
    """settings.reload() deve refletir mudança no .env sem reiniciar."""
    env_file = tmp_path / ".env"
    env_file.write_text("WIALON_TOKEN=antigo\n")
    monkeypatch.chdir(tmp_path)

    # Garante que o ambiente do processo não está poluído com WIALON_TOKEN
    monkeypatch.delenv("WIALON_TOKEN", raising=False)

    from src.core.config import Settings

    s = Settings()
    assert s.WIALON_TOKEN == "antigo"

    env_file.write_text("WIALON_TOKEN=novo\n")
    s.reload()
    assert s.WIALON_TOKEN == "novo"


def test_wialon_token_2_existe_como_string():
    """WIALON_TOKEN_2 deve existir e ser sempre string (vazia se não setado)."""
    from src.core.config import settings

    assert hasattr(settings, "WIALON_TOKEN_2")
    assert isinstance(settings.WIALON_TOKEN_2, str)


def test_reload_carrega_wialon_token_2(tmp_path, monkeypatch):
    """reload() deve atualizar WIALON_TOKEN_2 também."""
    env_file = tmp_path / ".env"
    env_file.write_text("WIALON_TOKEN_2=segundoabc\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("WIALON_TOKEN_2", raising=False)

    from src.core.config import Settings

    s = Settings()
    assert s.WIALON_TOKEN_2 == "segundoabc"
