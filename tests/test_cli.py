"""Testes do CLI — parser de IDs (#36).

A seleção de conta/token vive agora em `src.core.service_factory`; ver
`tests/test_service_factory.py`.
"""

import argparse

import pytest

from src.cli.main import parse_vehicle_ids


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
