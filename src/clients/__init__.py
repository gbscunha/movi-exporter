"""
Clients module for external API integrations.

Módulos:
- wialon_client: Cliente para API Wialon Hosting
"""

from .wialon_client import WialonClient, WialonError, WialonAuthError, WialonValidationError

__all__ = [
    "WialonClient",
    "WialonError",
    "WialonAuthError",
    "WialonValidationError",
]
