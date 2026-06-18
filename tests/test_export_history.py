"""Testes do leitor de histórico de exportações (Onda 3 Fase 04 — #07)."""

import time
from datetime import datetime

from src.services import export_history as eh


def _touch_export(base, year, month, account=None, name="VTR01_Hist.csv"):
    """Cria um arquivo de exportação fake na estrutura de pastas esperada."""
    folder = base / f"{year}-{month:02d}"
    if account:
        folder = folder / account
    folder.mkdir(parents=True, exist_ok=True)
    f = folder / name
    f.write_text("dado")
    return f


# ---------- list_exports ----------


def test_lista_vazia_quando_base_inexistente(tmp_path):
    assert eh.list_exports(tmp_path / "nada") == []


def test_lista_conta_unica(tmp_path):
    _touch_export(tmp_path, 2026, 4)
    _touch_export(tmp_path, 2026, 4, name="VTR02_Hist.csv")
    out = eh.list_exports(tmp_path)
    assert len(out) == 1
    assert out[0].year == 2026 and out[0].month == 4
    assert out[0].account is None
    assert out[0].file_count == 2


def test_lista_multi_conta(tmp_path):
    _touch_export(tmp_path, 2026, 5, account="Conta 1")
    _touch_export(tmp_path, 2026, 5, account="Conta 2")
    _touch_export(tmp_path, 2026, 5, account="Conta 2", name="VTR09_Hist.csv")
    out = eh.list_exports(tmp_path)
    assert len(out) == 2
    contas = {s.account: s.file_count for s in out}
    assert contas == {"Conta 1": 1, "Conta 2": 2}


def test_filtro_por_conta(tmp_path):
    _touch_export(tmp_path, 2026, 5, account="Conta 1")
    _touch_export(tmp_path, 2026, 5, account="Conta 2")
    out = eh.list_exports(tmp_path, account_label="Conta 2")
    assert len(out) == 1
    assert out[0].account == "Conta 2"


def test_filtro_conta_unica_ignora_label(tmp_path):
    """Estrutura de conta única: arquivos na raiz do mês contam mesmo com label."""
    _touch_export(tmp_path, 2026, 4)
    out = eh.list_exports(tmp_path, account_label="Conta 1")
    assert len(out) == 1


def test_ignora_pastas_nao_mensais(tmp_path):
    (tmp_path / "lixo").mkdir()
    (tmp_path / "2026-13").mkdir()  # mês inválido no formato? 13 casa o regex \d{2}
    _touch_export(tmp_path, 2026, 4)
    out = eh.list_exports(tmp_path)
    # "lixo" ignorada; "2026-13" tem dir mas sem arquivos -> não entra
    anos_meses = {(s.year, s.month) for s in out}
    assert (2026, 4) in anos_meses


def test_ordenacao_mais_recente_primeiro(tmp_path):
    _touch_export(tmp_path, 2026, 1)
    time.sleep(0.01)
    _touch_export(tmp_path, 2026, 3)
    out = eh.list_exports(tmp_path)
    assert out[0].month == 3  # modificado por último


# ---------- last_export ----------


def test_last_export_none_quando_vazio(tmp_path):
    assert eh.last_export(tmp_path) is None


def test_last_export_retorna_mais_recente(tmp_path):
    _touch_export(tmp_path, 2026, 2)
    time.sleep(0.01)
    _touch_export(tmp_path, 2026, 5)
    last = eh.last_export(tmp_path)
    assert last is not None and last.month == 5


# ---------- has_export_for ----------


def test_has_export_for(tmp_path):
    _touch_export(tmp_path, 2026, 4)
    assert eh.has_export_for(tmp_path, 2026, 4) is True
    assert eh.has_export_for(tmp_path, 2026, 5) is False


# ---------- suggest_unexported_month ----------


def test_sugestao_mes_anterior_nao_exportado(tmp_path):
    hoje = datetime(2026, 6, 16)
    # Maio (mês anterior) não exportado -> sugere (2026, 5)
    assert eh.suggest_unexported_month(tmp_path, hoje) == (2026, 5)


def test_sugestao_none_quando_mes_anterior_ja_exportado(tmp_path):
    _touch_export(tmp_path, 2026, 5)
    hoje = datetime(2026, 6, 16)
    assert eh.suggest_unexported_month(tmp_path, hoje) is None


def test_sugestao_vira_o_ano_em_janeiro(tmp_path):
    hoje = datetime(2026, 1, 10)
    # Mês anterior = dezembro/2025
    assert eh.suggest_unexported_month(tmp_path, hoje) == (2025, 12)


# ---------- year_stats ----------


def test_year_stats(tmp_path):
    _touch_export(tmp_path, 2026, 3)
    _touch_export(tmp_path, 2026, 3, name="VTR02_Hist.csv")
    _touch_export(tmp_path, 2026, 4)
    _touch_export(tmp_path, 2025, 12)  # ano diferente, não conta
    exports, files = eh.year_stats(tmp_path, 2026)
    assert exports == 2  # março e abril
    assert files == 3  # 2 (março) + 1 (abril)
