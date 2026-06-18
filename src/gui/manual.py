"""Abertura do manual do usuário (HTML embarcado) no navegador.

O manual mora em `docs/manual/manual.html` no repositório. No app empacotado
pelo PyInstaller, os dados ficam sob `sys._MEIPASS`. Este módulo resolve o
caminho nos dois cenários e abre o arquivo no navegador padrão via file://.
"""

import sys
import webbrowser
from pathlib import Path
from typing import Optional

from src.core.logger import logger


def _candidate_paths() -> list[Path]:
    """Locais possíveis do manual.html, em ordem de prioridade.

    1. Bundle PyInstaller (`sys._MEIPASS/docs/manual/manual.html`)
    2. Raiz do projeto em desenvolvimento (a partir deste arquivo)
    """
    candidates: list[Path] = []

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass) / "docs" / "manual" / "manual.html")

    # src/gui/manual.py -> sobe 2 níveis até a raiz do projeto.
    project_root = Path(__file__).resolve().parent.parent.parent
    candidates.append(project_root / "docs" / "manual" / "manual.html")

    return candidates


def manual_path() -> Optional[Path]:
    """Retorna o caminho do manual.html se existir, senão None."""
    for path in _candidate_paths():
        if path.exists():
            return path
    return None


def open_manual() -> bool:
    """Abre o manual no navegador padrão.

    Returns:
        True se conseguiu abrir; False se o arquivo não foi encontrado.
    """
    path = manual_path()
    if path is None:
        logger.warning(
            "Manual não encontrado. Procurado em: "
            + ", ".join(str(p) for p in _candidate_paths())
        )
        return False
    webbrowser.open(path.as_uri())
    return True
