"""Testes da exportação em lotes (`EXPORT_BATCH_SIZE`).

Frotas grandes (900+ veículos) acumulavam o histórico inteiro em memória até
montar o consolidado no final e travavam o app. `export_monthly_data` agora
particiona em lotes e grava o consolidado incrementalmente (append) — estes
testes usam `EXPORT_BATCH_SIZE` pequeno (via monkeypatch) pra forçar múltiplos
lotes sem precisar de uma frota fake gigante.
"""

import pandas as pd
from unittest.mock import MagicMock

import src.services.vehicle_service as vehicle_service_module
from src.services.vehicle_service import VehicleService


def _gps_page():
    """Uma página com um registro GPS simples (sensores ausentes → N/D)."""
    return [[{"t": 1775000000, "pos": {"y": -22.8, "x": -43.2, "s": 10}, "p": {}}]]


def _fleet(n):
    return [
        {"id": i, "nm": f"V{i}", "_plate": f"PLT{i:04d}"} for i in range(1, n + 1)
    ]


def test_export_em_lotes_gera_um_unico_consolidado_com_toda_a_frota(
    tmp_path, monkeypatch
):
    """5 veículos, lote de 2 → 3 lotes, mas 1 único CSV consolidado com os 5."""
    monkeypatch.setattr(vehicle_service_module, "EXPORT_BATCH_SIZE", 2)

    mock_client = MagicMock()
    mock_client.list_vehicles.return_value = _fleet(5)
    mock_client.get_vehicle_sensors.return_value = {}
    mock_client.get_history.side_effect = lambda *a, **k: iter(_gps_page())

    svc = VehicleService(client=mock_client, export_dir=str(tmp_path))
    result = svc.export_monthly_data(
        month=4, year=2026, export_format="csv", consolidated=True
    )

    assert result.processed_vehicles == 5
    consolidados = [f for f in result.exported_files if "Consolidado" in f]
    assert len(consolidados) == 1

    df = pd.read_csv(consolidados[0])
    assert len(df) == 5
    assert sorted(df["ID do Veículo"].unique().tolist()) == [1, 2, 3, 4, 5]
    # Data de Exportação uniforme mesmo vindo de lotes gravados em chamadas
    # separadas — não pode variar por lote.
    assert df["Data de Exportação"].nunique() == 1


def test_progresso_reportado_e_continuo_entre_lotes(tmp_path, monkeypatch):
    """on_progress deve continuar contando 1..total_vehicles através dos
    lotes, não reiniciar a cada lote (índice global, não local ao lote)."""
    monkeypatch.setattr(vehicle_service_module, "EXPORT_BATCH_SIZE", 2)

    mock_client = MagicMock()
    mock_client.list_vehicles.return_value = _fleet(5)
    mock_client.get_vehicle_sensors.return_value = {}
    mock_client.get_history.side_effect = lambda *a, **k: iter(_gps_page())

    seen = []
    svc = VehicleService(client=mock_client, export_dir=str(tmp_path))
    svc.export_monthly_data(
        month=4, year=2026, export_format="csv", consolidated=True,
        on_progress=lambda current, total, name: seen.append((current, total)),
    )

    assert seen == [(1, 5), (2, 5), (3, 5), (4, 5), (5, 5)]


def test_cancelamento_no_2o_lote_descarta_consolidado_do_1o_lote_tambem(
    tmp_path, monkeypatch
):
    """1º lote (2 veículos) termina e é gravado no consolidado; cancela no
    início do 2º lote. Mesmo assim, nenhum consolidado deve sobrar — nem em
    `exported_files`, nem em disco (mesmo critério tudo-ou-nada de sempre)."""
    monkeypatch.setattr(vehicle_service_module, "EXPORT_BATCH_SIZE", 2)

    mock_client = MagicMock()
    mock_client.list_vehicles.return_value = _fleet(4)  # 2 lotes de 2
    mock_client.get_vehicle_sensors.return_value = {}
    mock_client.get_history.side_effect = lambda *a, **k: iter(_gps_page())

    state = {"calls": 0}

    def should_cancel():
        state["calls"] += 1
        return state["calls"] >= 3  # cancela antes do 3º veículo (1º do 2º lote)

    svc = VehicleService(client=mock_client, export_dir=str(tmp_path))
    result = svc.export_monthly_data(
        month=4, year=2026, export_format="csv", consolidated=True,
        should_cancel=should_cancel,
    )

    assert result.cancelled is True
    assert result.processed_vehicles == 2  # só o 1º lote, completo
    assert not any("Consolidado" in f for f in result.exported_files)
    assert list(tmp_path.rglob("*Consolidado*")) == []  # nada órfão em disco


def test_frota_menor_que_o_lote_continua_funcionando_normalmente(tmp_path):
    """Frota abaixo de EXPORT_BATCH_SIZE (padrão 100) processa em 1 lote só —
    caminho mais comum, não pode regredir."""
    mock_client = MagicMock()
    mock_client.list_vehicles.return_value = _fleet(3)
    mock_client.get_vehicle_sensors.return_value = {}
    mock_client.get_history.side_effect = lambda *a, **k: iter(_gps_page())

    svc = VehicleService(client=mock_client, export_dir=str(tmp_path))
    result = svc.export_monthly_data(
        month=4, year=2026, export_format="csv", consolidated=True
    )

    assert result.processed_vehicles == 3
    consolidados = [f for f in result.exported_files if "Consolidado" in f]
    assert len(consolidados) == 1
    df = pd.read_csv(consolidados[0])
    assert len(df) == 3
