"""
Clients module for external API integrations.

Módulos:
- base_client: Classes base para clientes HTTP
- wialon_client: Cliente para API Wialon Hosting
- system_a_client: Cliente legado para System A
"""

from .base_client import BaseClient, StatefulClient
from .wialon_client import WialonClient, WialonError, WialonAuthError, WialonValidationError

__all__ = [
    "BaseClient",
    "StatefulClient",
    "WialonClient",
    "WialonError",
    "WialonAuthError",
    "WialonValidationError",
]
