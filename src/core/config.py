"""
Configurações centralizadas do Movi Exporter App.

Carrega variáveis de ambiente do arquivo .env.
"""

from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    """Configurações da aplicação carregadas do ambiente."""

    # Wialon (sistema principal)
    WIALON_TOKEN: str = os.getenv("WIALON_TOKEN", "")
    WIALON_BASE_URL: str = os.getenv(
        "WIALON_BASE_URL", "https://hst-api.wialon.com/wialon/ajax.html"
    )

    # Configurações de exportação
    EXPORT_DIR: str = os.getenv("EXPORT_DIR", "./exports")

    # Configurações de paginação
    WIALON_PAGE_SIZE: int = int(os.getenv("WIALON_PAGE_SIZE", "1000"))

    # Google Drive (OAuth2)
    GOOGLE_DRIVE_CREDENTIALS_FILE: str = os.getenv(
        "GOOGLE_DRIVE_CREDENTIALS_FILE", "./client_secrets.json"
    )
    GOOGLE_DRIVE_FOLDER_ID: str = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")


settings = Settings()
