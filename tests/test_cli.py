"""Testes do CLI — flag --account e parser de IDs (#36)."""

import argparse

import pytest

from src.cli.main import build_service, parse_vehicle_ids


# ---------- parse_vehicle_ids ----------


def test_parse_vehicle_ids_string_simples():
    assert parse_vehicle_ids("123,456,789") == [123, 456, 789]


def test_parse_vehicle_ids_ignora_espacos():
    assert parse_vehicle_ids("  123 , 456 ,  789  ") == [123, 456, 789]


def test_parse_vehicle_ids_string_vazia():
    assert parse_vehicle_ids("") == []


def test_parse_vehicle_ids_id_invalido_levanta():
    with pytest.raises(argparse.ArgumentTypeError) as excinfo:
        parse_vehicle_ids("123,abc,456")
    assert "abc" in str(excinfo.value)


# ---------- build_service ----------


def test_build_service_account_1_usa_token_padrao(monkeypatch):
    """Conta 1 deve instanciar VehicleService sem custom client (usa WIALON_TOKEN)."""
    from src.core import config

    monkeypatch.setattr(config.settings, "WIALON_TOKEN", "fake-token-1", raising=False)
    monkeypatch.setattr(config.settings, "WIALON_TOKEN_2", "", raising=False)

    service = build_service(account=1)
    # O client foi criado com o token padrão da config
    assert service.client.token == "fake-token-1"


def test_build_service_account_2_usa_token_2(monkeypatch):
    """Conta 2 deve usar WIALON_TOKEN_2."""
    from src.core import config

    monkeypatch.setattr(config.settings, "WIALON_TOKEN", "fake-token-1", raising=False)
    monkeypatch.setattr(
        config.settings, "WIALON_TOKEN_2", "fake-token-2", raising=False
    )

    service = build_service(account=2)
    assert service.client.token == "fake-token-2"


def test_build_service_account_2_sem_token_levanta(monkeypatch):
    """Conta 2 sem WIALON_TOKEN_2 configurado deve levantar ValueError claro."""
    from src.core import config

    monkeypatch.setattr(config.settings, "WIALON_TOKEN", "fake-token-1", raising=False)
    monkeypatch.setattr(config.settings, "WIALON_TOKEN_2", "", raising=False)

    with pytest.raises(ValueError) as excinfo:
        build_service(account=2)
    assert "Conta 2" in str(excinfo.value)
    assert "WIALON_TOKEN_2" in str(excinfo.value)


def test_build_service_account_invalido_levanta(monkeypatch):
    from src.core import config

    monkeypatch.setattr(config.settings, "WIALON_TOKEN", "fake-token-1", raising=False)

    with pytest.raises(ValueError) as excinfo:
        build_service(account=3)
    assert "inválida" in str(excinfo.value).lower() or "invalida" in str(excinfo.value).lower()


def test_build_service_repassa_export_dir(monkeypatch, tmp_path):
    """export_dir customizado deve ser passado para o DataExporter."""
    from src.core import config

    monkeypatch.setattr(config.settings, "WIALON_TOKEN", "fake-token-1", raising=False)

    service = build_service(account=1, export_dir=str(tmp_path))
    assert str(tmp_path) in str(service.exporter.base_export_dir)
