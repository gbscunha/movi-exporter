"""Fábrica central de `VehicleService`.

Ponto único de criação do serviço a partir da conta selecionada. Existe para
que a GUI e o CLI não instanciem `WialonClient` diretamente — a regra de
arquitetura é que nada em `src/gui/` importe `src.clients` (ver CLAUDE.md).
"""

from typing import Optional

from src.clients.wialon_client import WialonClient, WialonError
from src.core.config import settings
from src.services.vehicle_service import VehicleService

__all__ = ["build_vehicle_service", "authenticate_token", "WialonError"]


def build_vehicle_service(
    account: int = 1,
    export_dir: Optional[str] = None,
) -> VehicleService:
    """Cria um `VehicleService` usando o token da conta selecionada.

    Conta 1 usa `settings.WIALON_TOKEN`; conta 2 usa `settings.WIALON_TOKEN_2`.
    Se a Conta 2 for solicitada mas não estiver configurada, levanta ValueError.
    """
    if account == 1:
        return VehicleService(export_dir=export_dir)

    if account == 2:
        if not settings.WIALON_TOKEN_2:
            raise ValueError(
                "Conta 2 não configurada — defina WIALON_TOKEN_2 no .env "
                "ou na tela Configurações."
            )
        client = WialonClient(token=settings.WIALON_TOKEN_2)
        return VehicleService(client=client, export_dir=export_dir)

    raise ValueError(f"Conta inválida: {account!r}. Use 1 ou 2.")


def authenticate_token(token: str) -> str:
    """Autentica um token avulso e retorna o username.

    Usado pela tela de Configurações para validar um token digitado antes de
    salvá-lo. Levanta `WialonError` se a autenticação falhar.
    """
    client = WialonClient(token=token)
    try:
        client.authenticate()
        return getattr(client, "username", "") or ""
    finally:
        client.logout()
