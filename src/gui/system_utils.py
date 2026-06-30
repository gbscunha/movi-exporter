"""Utilidades de integração com o sistema operacional para a GUI."""

import subprocess
import sys
from pathlib import Path


def open_system_folder(path: Path) -> None:
    """Abre `path` no explorador de arquivos do SO atual.

    Levanta a exceção do subprocess em caso de falha — o chamador decide como
    reportar (toast, messagebox ou apenas log).
    """
    if sys.platform == "win32":
        subprocess.Popen(["explorer", str(path)])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])
