"""Testes das validações puras das Configurações (Fase 06)."""

from src.gui.validation import validate_export_dir, validate_token


def test_diretorio_vazio_retorna_erro():
    assert validate_export_dir("") is not None
    assert validate_export_dir("   ") is not None


def test_diretorio_valido_retorna_none():
    assert validate_export_dir("./exports") is None
    assert validate_export_dir("/Users/foo/dados") is None


def test_token_vazio_retorna_erro():
    assert validate_token("") is not None
    assert validate_token("  ") is not None


def test_token_preenchido_retorna_none():
    assert validate_token("abc123") is None
