"""
Sistema de Auto-Update via GitHub Releases.
"""

import os
import sys
import tempfile
import subprocess
import requests
from typing import Optional, Tuple
from packaging import version

from src.core.logger import logger
from src.gui import __version__

# Configuração do repositório GitHub
GITHUB_OWNER = "gbscunha"
GITHUB_REPO = "movi-exporter"
GITHUB_API_URL = (
    f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
)


class AutoUpdater:
    """
    Sistema de atualização automática via GitHub Releases.

    Funcionalidades:
    - Verifica nova versão no GitHub
    - Baixa o instalador/executável
    - Inicia a instalação e fecha o app atual
    """

    def __init__(self):
        self.current_version = __version__
        self.latest_version: Optional[str] = None
        self.download_url: Optional[str] = None
        self.release_notes: Optional[str] = None

    def check_for_updates(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Verifica se há atualizações disponíveis.

        Returns:
            Tuple[bool, Optional[str], Optional[str]]:
                (tem_atualização, versão_nova, url_download)
        """
        try:
            logger.info(
                f"Verificando atualizações... (versão atual: {self.current_version})"
            )

            response = requests.get(
                GITHUB_API_URL,
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=10,
            )

            if response.status_code == 404:
                logger.info("Nenhum release encontrado no GitHub")
                return False, None, None

            response.raise_for_status()
            data = response.json()

            # Extrair versão (remove 'v' se houver)
            tag_name = data.get("tag_name", "")
            self.latest_version = tag_name.lstrip("v")
            self.release_notes = data.get("body", "")

            # Encontrar asset para download (Windows .exe ou .msi)
            assets = data.get("assets", [])
            for asset in assets:
                name = asset.get("name", "").lower()
                if name.endswith((".exe", ".msi")):
                    self.download_url = asset.get("browser_download_url")
                    break

            # Comparar versões
            if self._is_newer_version(self.latest_version):
                logger.info(f"Nova versão disponível: {self.latest_version}")
                return True, self.latest_version, self.download_url

            logger.info("Nenhuma atualização disponível")
            return False, None, None

        except requests.RequestException as e:
            logger.warning(f"Erro ao verificar atualizações: {e}")
            return False, None, None
        except Exception as e:
            logger.error(f"Erro inesperado ao verificar atualizações: {e}")
            return False, None, None

    def _is_newer_version(self, new_version: str) -> bool:
        """Verifica se a nova versão é maior que a atual."""
        try:
            return version.parse(new_version) > version.parse(self.current_version)
        except Exception:
            return False

    def download_update(self, progress_callback=None) -> Optional[str]:
        """
        Baixa a atualização.

        Args:
            progress_callback: Função callback(downloaded, total) para progresso

        Returns:
            Caminho do arquivo baixado ou None se falhou
        """
        if not self.download_url:
            logger.error("URL de download não disponível")
            return None

        try:
            logger.info(f"Baixando atualização: {self.download_url}")

            response = requests.get(self.download_url, stream=True, timeout=300)
            response.raise_for_status()

            # Obter tamanho total
            total_size = int(response.headers.get("content-length", 0))

            # Criar arquivo temporário
            _, ext = os.path.splitext(self.download_url)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext or ".exe")

            downloaded = 0
            chunk_size = 8192

            with open(temp_file.name, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        if progress_callback and total_size:
                            progress_callback(downloaded, total_size)

            logger.info(f"Download concluído: {temp_file.name}")
            return temp_file.name

        except Exception as e:
            logger.error(f"Erro ao baixar atualização: {e}")
            return None

    def install_update(self, installer_path: str) -> bool:
        """
        Instala a atualização e fecha o app atual.

        Args:
            installer_path: Caminho do instalador baixado

        Returns:
            True se iniciou a instalação com sucesso
        """
        try:
            logger.info(f"Iniciando instalação: {installer_path}")

            if sys.platform == "win32":
                # Windows: executa o instalador
                os.startfile(installer_path)
            else:
                # macOS/Linux: abre o arquivo
                subprocess.Popen(["open", installer_path])

            # Fecha a aplicação atual
            logger.info("Fechando aplicação para atualização...")
            sys.exit(0)

        except Exception as e:
            logger.error(f"Erro ao instalar atualização: {e}")
            return False

        return True

    def get_release_notes(self) -> str:
        """Retorna as notas da release."""
        return self.release_notes or "Sem notas de versão disponíveis."
