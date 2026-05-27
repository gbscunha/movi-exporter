"""Testes do helper env_writer.

Fase 08 — escrever em .env preservando ordem e comentários.
"""

import sys
from pathlib import Path

# Garante que `src` é importável quando rodando direto via pytest.
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.env_writer import set_env_value


def test_cria_arquivo_env_se_nao_existe(tmp_path):
    env_file = tmp_path / ".env"
    set_env_value("WIALON_TOKEN", "abc123", env_path=str(env_file))
    assert env_file.read_text() == "WIALON_TOKEN=abc123\n"


def test_atualiza_chave_existente(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("WIALON_TOKEN=antigo\nEXPORT_DIR=./exports\n")
    set_env_value("WIALON_TOKEN", "novo", env_path=str(env_file))
    content = env_file.read_text()
    assert "WIALON_TOKEN=novo" in content
    assert "WIALON_TOKEN=antigo" not in content
    # Preservou outras linhas
    assert "EXPORT_DIR=./exports" in content


def test_insere_chave_nova_no_final(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("EXPORT_DIR=./exports\n")
    set_env_value("WIALON_TOKEN_2", "xyz789", env_path=str(env_file))
    lines = env_file.read_text().splitlines()
    assert "WIALON_TOKEN_2=xyz789" in lines
    # Não removeu o que já existia
    assert "EXPORT_DIR=./exports" in lines


def test_preserva_comentarios(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("# Wialon\nWIALON_TOKEN=antigo\n")
    set_env_value("WIALON_TOKEN", "novo", env_path=str(env_file))
    content = env_file.read_text()
    assert "# Wialon" in content
    assert "WIALON_TOKEN=novo" in content
