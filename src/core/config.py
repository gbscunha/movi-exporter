"""
Configurações centralizadas do Movi Exporter App.

Carrega variáveis de ambiente do arquivo .env.
"""

import os

from dotenv import find_dotenv, load_dotenv

# usecwd=True garante que find_dotenv olhe a partir do diretório de trabalho
# atual — fundamental para testes (que rodam em tmp_path) e para o app
# instalado, onde o .env fica ao lado do executável.
load_dotenv(find_dotenv(usecwd=True))


class Settings:
    """Configurações da aplicação carregadas do ambiente.

    Os atributos são preenchidos via `reload()` em `__init__`, permitindo
    que a aplicação leia mudanças no `.env` em runtime (ex: depois do
    usuário salvar um novo token pela GUI) sem reiniciar.
    """

    # Anotações de tipo — valores são preenchidos por reload().
    WIALON_TOKEN: str
    WIALON_TOKEN_2: str
    WIALON_BASE_URL: str
    EXPORT_DIR: str
    WIALON_PAGE_SIZE: int
    GOOGLE_DRIVE_CREDENTIALS_FILE: str
    GOOGLE_DRIVE_FOLDER_ID: str

    def __init__(self) -> None:
        self.reload()

    def reload(self) -> None:
        """Recarrega todas as variáveis a partir do `.env` atual."""
        load_dotenv(find_dotenv(usecwd=True), override=True)
        self.WIALON_TOKEN = os.getenv("WIALON_TOKEN", "")
        self.WIALON_TOKEN_2 = os.getenv("WIALON_TOKEN_2", "")
        self.WIALON_BASE_URL = os.getenv(
            "WIALON_BASE_URL", "https://hst-api.wialon.com/wialon/ajax.html"
        )
        self.EXPORT_DIR = os.getenv("EXPORT_DIR", "./exports")
        self.WIALON_PAGE_SIZE = int(os.getenv("WIALON_PAGE_SIZE", "1000"))
        self.GOOGLE_DRIVE_CREDENTIALS_FILE = os.getenv(
            "GOOGLE_DRIVE_CREDENTIALS_FILE", "./client_secrets.json"
        )
        self.GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")


settings = Settings()
