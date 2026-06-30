"""Testes da fábrica de VehicleService — seleção de conta/token."""

import pytest

from src.core.service_factory import build_vehicle_service


def test_build_vehicle_service_conta_1_usa_token_padrao(monkeypatch):
    """Conta 1 deve instanciar VehicleService usando WIALON_TOKEN."""
    from src.core import config

    monkeypatch.setattr(config.settings, "WIALON_TOKEN", "fake-token-1", raising=False)
    monkeypatch.setattr(config.settings, "WIALON_TOKEN_2", "", raising=False)

    service = build_vehicle_service(account=1)
    assert service.client.token == "fake-token-1"


def test_build_vehicle_service_conta_2_usa_token_2(monkeypatch):
    """Conta 2 deve usar WIALON_TOKEN_2."""
    from src.core import config

    monkeypatch.setattr(config.settings, "WIALON_TOKEN", "fake-token-1", raising=False)
    monkeypatch.setattr(
        config.settings, "WIALON_TOKEN_2", "fake-token-2", raising=False
    )

    service = build_vehicle_service(account=2)
    assert service.client.token == "fake-token-2"


def test_build_vehicle_service_conta_2_sem_token_levanta(monkeypatch):
    """Conta 2 sem WIALON_TOKEN_2 configurado deve levantar ValueError claro."""
    from src.core import config

    monkeypatch.setattr(config.settings, "WIALON_TOKEN", "fake-token-1", raising=False)
    monkeypatch.setattr(config.settings, "WIALON_TOKEN_2", "", raising=False)

    with pytest.raises(ValueError) as excinfo:
        build_vehicle_service(account=2)
    assert "Conta 2" in str(excinfo.value)
    assert "WIALON_TOKEN_2" in str(excinfo.value)


def test_build_vehicle_service_conta_invalida_levanta(monkeypatch):
    from src.core import config

    monkeypatch.setattr(config.settings, "WIALON_TOKEN", "fake-token-1", raising=False)

    with pytest.raises(ValueError) as excinfo:
        build_vehicle_service(account=3)
    msg = str(excinfo.value).lower()
    assert "inválida" in msg or "invalida" in msg


def test_build_vehicle_service_repassa_export_dir(monkeypatch, tmp_path):
    """export_dir customizado deve ser passado para o DataExporter."""
    from src.core import config

    monkeypatch.setattr(config.settings, "WIALON_TOKEN", "fake-token-1", raising=False)

    service = build_vehicle_service(account=1, export_dir=str(tmp_path))
    assert str(tmp_path) in str(service.exporter.base_export_dir)
