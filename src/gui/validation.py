"""Validações puras para campos das Configurações.

Mantidas fora dos frames (sem dependência de CustomTkinter) para serem
testáveis sem instanciar a GUI. Cada função retorna a mensagem de erro em
PT-BR (string) ou `None` quando o valor é válido.
"""

from typing import Optional


def validate_export_dir(value: str) -> Optional[str]:
    """Valida o diretório de exportação.

    Regra mínima: não pode ser vazio/só espaços. Não exige que a pasta já
    exista — o app a cria na hora de exportar.
    """
    if not value or not value.strip():
        return "Informe um diretório de exportação."
    return None


def validate_token(value: str) -> Optional[str]:
    """Valida o token Wialon (apenas presença — formato é checado no Testar)."""
    if not value or not value.strip():
        return "Cole um token antes de continuar."
    return None
