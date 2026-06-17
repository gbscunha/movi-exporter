"""Leitura do histórico de exportações a partir das pastas em disco.

A Home usa isto para mostrar "última exportação", sugerir o próximo mês a
exportar e estatísticas do ano. NÃO há persistência (banco/JSON) — apenas
inspeção da estrutura de pastas que o DataExporter já gera:

    EXPORT_DIR/AAAA-MM/<arquivos>                  (conta única)
    EXPORT_DIR/AAAA-MM/<Conta X>/<arquivos>         (múltiplas contas)

A persistência real de histórico (com status, re-exportar etc.) é o item #24,
planejado para uma onda futura.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# Pasta de mês no formato AAAA-MM (ex: 2026-05).
_MONTH_DIR_RE = re.compile(r"^(\d{4})-(\d{2})$")

# Extensões consideradas "arquivo de exportação".
_EXPORT_EXTS = {".csv", ".xlsx"}


@dataclass
class ExportSummary:
    """Resumo de uma exportação encontrada em disco."""

    year: int
    month: int
    account: Optional[str]  # "Conta 1"/"Conta 2"/None (conta única)
    file_count: int
    last_modified: datetime
    folder: Path


def _export_files(folder: Path) -> List[Path]:
    """Arquivos de exportação (csv/xlsx) diretamente dentro de `folder`."""
    if not folder.is_dir():
        return []
    return [
        f
        for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in _EXPORT_EXTS
    ]


def _account_subdirs(month_dir: Path) -> List[Path]:
    """Subpastas de conta ("Conta 1", "Conta 2"...) dentro de uma pasta de mês."""
    return [
        d
        for d in month_dir.iterdir()
        if d.is_dir() and d.name.lower().startswith("conta")
    ]


def list_exports(
    base_dir: str | Path,
    account_label: Optional[str] = None,
) -> List[ExportSummary]:
    """Lista as exportações encontradas, mais recentes primeiro.

    Args:
        base_dir: diretório base de exportação (settings.EXPORT_DIR).
        account_label: se informado (ex: "Conta 1"), filtra para essa conta.
            Quando a estrutura é de conta única (arquivos direto na pasta do
            mês, sem subpasta "Conta X"), esses arquivos são incluídos
            independentemente do label — afinal, são a única conta.

    Returns:
        Lista de ExportSummary ordenada por last_modified desc.
    """
    base = Path(base_dir)
    if not base.is_dir():
        return []

    summaries: List[ExportSummary] = []

    for month_dir in base.iterdir():
        m = _MONTH_DIR_RE.match(month_dir.name)
        if not month_dir.is_dir() or not m:
            continue
        year, month = int(m.group(1)), int(m.group(2))

        account_dirs = _account_subdirs(month_dir)

        if account_dirs:
            # Estrutura multi-conta: cada subpasta é uma conta.
            for acc_dir in account_dirs:
                if account_label and acc_dir.name.lower() != account_label.lower():
                    continue
                files = _export_files(acc_dir)
                if files:
                    summaries.append(
                        _summary(year, month, acc_dir.name, files, acc_dir)
                    )
        else:
            # Conta única: arquivos direto na pasta do mês.
            files = _export_files(month_dir)
            if files:
                summaries.append(_summary(year, month, None, files, month_dir))

    summaries.sort(key=lambda s: s.last_modified, reverse=True)
    return summaries


def _summary(
    year: int, month: int, account: Optional[str], files: List[Path], folder: Path
) -> ExportSummary:
    last_mtime = max(f.stat().st_mtime for f in files)
    return ExportSummary(
        year=year,
        month=month,
        account=account,
        file_count=len(files),
        last_modified=datetime.fromtimestamp(last_mtime),
        folder=folder,
    )


def last_export(
    base_dir: str | Path,
    account_label: Optional[str] = None,
) -> Optional[ExportSummary]:
    """Exportação mais recente (por data de modificação), ou None se não houver."""
    exports = list_exports(base_dir, account_label)
    return exports[0] if exports else None


def has_export_for(
    base_dir: str | Path,
    year: int,
    month: int,
    account_label: Optional[str] = None,
) -> bool:
    """True se já existe exportação para o mês/ano (e conta) dados."""
    return any(
        s.year == year and s.month == month
        for s in list_exports(base_dir, account_label)
    )


def suggest_unexported_month(
    base_dir: str | Path,
    today: datetime,
    account_label: Optional[str] = None,
) -> Optional[tuple[int, int]]:
    """Sugere o mês fechado mais recente que ainda não foi exportado.

    Relatórios são tipicamente do mês anterior fechado. Retorna (ano, mês)
    do mês anterior a `today` se ele ainda não tiver exportação; caso já
    exportado, retorna None (nada a sugerir).
    """
    # Mês anterior ao de `today`.
    if today.month == 1:
        year, month = today.year - 1, 12
    else:
        year, month = today.year, today.month - 1

    if has_export_for(base_dir, year, month, account_label):
        return None
    return (year, month)


def year_stats(
    base_dir: str | Path,
    year: int,
    account_label: Optional[str] = None,
) -> tuple[int, int]:
    """Estatísticas do ano: (qtd de exportações, total de arquivos gerados)."""
    exports = [s for s in list_exports(base_dir, account_label) if s.year == year]
    export_count = len(exports)
    file_count = sum(s.file_count for s in exports)
    return (export_count, file_count)
