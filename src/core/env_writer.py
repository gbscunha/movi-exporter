"""Helper para escrita segura no arquivo .env.

Atualiza ou insere uma chave KEY=value preservando a ordem das linhas
e quaisquer comentários presentes no arquivo original.
"""

import re
from pathlib import Path


def set_env_value(key: str, value: str, env_path: str = ".env") -> None:
    """Atualiza KEY=value no .env. Cria o arquivo se não existir.

    Se a chave já existe, substitui a linha in-place (preservando ordem).
    Se não existe, anexa ao final. Comentários e outras linhas são preservados.
    """
    path = Path(env_path)
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []

    pattern = re.compile(rf"^{re.escape(key)}\s*=")
    new_line = f"{key}={value}"
    updated = False

    for i, line in enumerate(lines):
        if pattern.match(line):
            lines[i] = new_line
            updated = True
            break

    if not updated:
        lines.append(new_line)

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
