"""
Serviço de upload para Google Drive.

Utiliza OAuth2 para autenticação com usuário real.
Na primeira execução, abre o navegador para login.
O token é salvo em token.json para uso futuro.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from src.core.config import settings
from src.core.logger import logger


# Escopos necessários para upload
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Arquivo para salvar o token de acesso
TOKEN_FILE = "token.json"


@dataclass
class UploadResult:
    """Resultado do upload de arquivos."""

    total_files: int = 0
    uploaded_files: int = 0
    failed_files: int = 0
    file_details: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Taxa de sucesso do upload."""
        if self.total_files == 0:
            return 0.0
        return (self.uploaded_files / self.total_files) * 100


class DriveUploader:
    """
    Serviço de upload para Google Drive.

    Usa OAuth2 para autenticação com usuário real.
    Na primeira execução, abre o navegador para autorização.
    O token é salvo para uso futuro.
    """

    # Mapeamento de extensões para MIME types
    MIME_TYPES = {
        ".csv": "text/csv",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls": "application/vnd.ms-excel",
        ".json": "application/json",
        ".txt": "text/plain",
    }

    def __init__(
        self,
        credentials_file: Optional[str] = None,
        folder_id: Optional[str] = None,
        token_file: Optional[str] = None,
    ):
        """
        Inicializa o uploader.

        Args:
            credentials_file: Caminho para client_secrets.json (OAuth2).
                             Se não fornecido, usa settings.
            folder_id: ID da pasta raiz no Drive.
                      Se não fornecido, usa settings.
            token_file: Caminho para salvar o token.
                       Se não fornecido, usa TOKEN_FILE.
        """
        self.credentials_file = (
            credentials_file or settings.GOOGLE_DRIVE_CREDENTIALS_FILE
        )
        self.root_folder_id = folder_id or settings.GOOGLE_DRIVE_FOLDER_ID
        self.token_file = token_file or TOKEN_FILE

        self._service = None
        self._folder_cache: Dict[str, str] = {}  # Cache de subpastas criadas

        logger.info("DriveUploader inicializado")

    def _get_credentials(self) -> Credentials:
        """
        Obtém credenciais OAuth2.

        Na primeira execução, abre o navegador para autorização.
        Nas próximas, usa o token salvo.

        Returns:
            Credenciais OAuth2
        """
        creds = None

        # Verifica se já existe token salvo
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
            logger.debug("Token existente carregado")

        # Se não há credenciais válidas, faz o fluxo de autorização
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Token expirado, mas pode ser renovado
                logger.info("Renovando token de acesso...")
                creds.refresh(Request())
            else:
                # Primeira vez: abre navegador para autorização
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Arquivo client_secrets.json não encontrado: {self.credentials_file}\n"
                        "Baixe o arquivo de credenciais OAuth2 do Google Cloud Console."
                    )

                logger.info("Abrindo navegador para autorização do Google Drive...")
                logger.info("Por favor, faça login e autorize o acesso.")

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
                logger.success("Autorização concedida!")

            # Salva o token para próximas execuções
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())
                logger.info(f"Token salvo em: {self.token_file}")

        return creds

    def _get_service(self):
        """
        Obtém serviço autenticado do Google Drive.

        Returns:
            Serviço da API do Google Drive

        Raises:
            FileNotFoundError: Se arquivo de credenciais não existir
            ValueError: Se credenciais inválidas
        """
        if self._service is not None:
            return self._service

        if not self.root_folder_id:
            raise ValueError(
                "GOOGLE_DRIVE_FOLDER_ID não configurado. "
                "Adicione ao .env ou passe como parâmetro."
            )

        try:
            creds = self._get_credentials()
            self._service = build("drive", "v3", credentials=creds)
            logger.debug("Serviço do Google Drive autenticado com sucesso")

            return self._service

        except Exception as e:
            raise ValueError(f"Erro ao autenticar com Google Drive: {e}")

    def _get_mime_type(self, file_path: str) -> str:
        """
        Obtém MIME type baseado na extensão do arquivo.

        Args:
            file_path: Caminho do arquivo

        Returns:
            MIME type string
        """
        ext = Path(file_path).suffix.lower()
        return self.MIME_TYPES.get(ext, "application/octet-stream")

    def _find_folder(self, folder_name: str, parent_id: str) -> Optional[str]:
        """
        Busca uma pasta pelo nome dentro de um diretório pai.

        Args:
            folder_name: Nome da pasta a buscar
            parent_id: ID da pasta pai

        Returns:
            ID da pasta se encontrada, None caso contrário
        """
        service = self._get_service()

        query = (
            f"name = '{folder_name}' and "
            f"'{parent_id}' in parents and "
            f"mimeType = 'application/vnd.google-apps.folder' and "
            f"trashed = false"
        )

        try:
            results = (
                service.files()
                .list(q=query, spaces="drive", fields="files(id, name)")
                .execute()
            )

            files = results.get("files", [])
            if files:
                return files[0]["id"]
            return None

        except HttpError as e:
            logger.error(f"Erro ao buscar pasta {folder_name}: {e}")
            return None

    def _create_folder(self, folder_name: str, parent_id: str) -> str:
        """
        Cria uma pasta no Google Drive.

        Args:
            folder_name: Nome da pasta
            parent_id: ID da pasta pai

        Returns:
            ID da pasta criada
        """
        service = self._get_service()

        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }

        try:
            folder = service.files().create(body=file_metadata, fields="id").execute()

            folder_id = folder.get("id")
            logger.info(f"Pasta criada no Drive: {folder_name} (ID: {folder_id})")

            return folder_id

        except HttpError as e:
            raise RuntimeError(f"Erro ao criar pasta {folder_name}: {e}")

    def _get_or_create_folder(self, folder_name: str, parent_id: str) -> str:
        """
        Obtém ID de uma pasta, criando-a se não existir.

        Args:
            folder_name: Nome da pasta
            parent_id: ID da pasta pai

        Returns:
            ID da pasta
        """
        # Verifica cache primeiro
        cache_key = f"{parent_id}/{folder_name}"
        if cache_key in self._folder_cache:
            return self._folder_cache[cache_key]

        # Busca no Drive
        folder_id = self._find_folder(folder_name, parent_id)

        if folder_id is None:
            # Cria a pasta
            folder_id = self._create_folder(folder_name, parent_id)

        # Salva no cache
        self._folder_cache[cache_key] = folder_id

        return folder_id

    def _get_month_folder(self, month: int, year: int) -> str:
        """
        Obtém ID da pasta do mês, criando-a se necessário.

        Estrutura: RootFolder/YYYY-MM/

        Args:
            month: Mês (1-12)
            year: Ano

        Returns:
            ID da pasta do mês
        """
        folder_name = f"{year}-{month:02d}"
        return self._get_or_create_folder(folder_name, self.root_folder_id)

    def _file_exists(self, file_name: str, folder_id: str) -> Optional[str]:
        """
        Verifica se arquivo já existe na pasta.

        Args:
            file_name: Nome do arquivo
            folder_id: ID da pasta

        Returns:
            ID do arquivo se existir, None caso contrário
        """
        service = self._get_service()

        query = f"name = '{file_name}' and '{folder_id}' in parents and trashed = false"

        try:
            results = (
                service.files()
                .list(q=query, spaces="drive", fields="files(id, name)")
                .execute()
            )

            files = results.get("files", [])
            if files:
                return files[0]["id"]
            return None

        except HttpError as e:
            logger.error(f"Erro ao verificar arquivo {file_name}: {e}")
            return None

    def upload_file(
        self,
        file_path: str,
        folder_id: Optional[str] = None,
        overwrite: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """
        Faz upload de um arquivo para o Google Drive.

        Args:
            file_path: Caminho local do arquivo
            folder_id: ID da pasta de destino (usa root se não fornecido)
            overwrite: Se True, sobrescreve arquivo existente

        Returns:
            Dicionário com informações do arquivo (id, name, webViewLink)
            ou None se falhar
        """
        if not os.path.exists(file_path):
            logger.error(f"Arquivo não encontrado: {file_path}")
            return None

        service = self._get_service()
        target_folder = folder_id or self.root_folder_id
        file_name = Path(file_path).name
        mime_type = self._get_mime_type(file_path)

        try:
            # Verifica se arquivo já existe
            existing_id = self._file_exists(file_name, target_folder)

            if existing_id:
                if overwrite:
                    # Atualiza arquivo existente
                    media = MediaFileUpload(file_path, mimetype=mime_type)

                    file = (
                        service.files()
                        .update(
                            fileId=existing_id,
                            media_body=media,
                            fields="id, name, webViewLink",
                        )
                        .execute()
                    )

                    logger.info(f"Arquivo atualizado: {file_name}")
                    return file
                else:
                    logger.info(f"Arquivo já existe (ignorado): {file_name}")
                    return {"id": existing_id, "name": file_name, "skipped": True}

            # Upload de novo arquivo
            file_metadata = {"name": file_name, "parents": [target_folder]}

            media = MediaFileUpload(file_path, mimetype=mime_type)

            file = (
                service.files()
                .create(
                    body=file_metadata, media_body=media, fields="id, name, webViewLink"
                )
                .execute()
            )

            logger.success(f"Upload concluído: {file_name}")
            return file

        except HttpError as e:
            logger.error(f"Erro no upload de {file_name}: {e}")
            return None

    def upload_files(
        self,
        file_paths: List[str],
        month: int,
        year: int,
        overwrite: bool = True,
    ) -> UploadResult:
        """
        Faz upload de múltiplos arquivos para a pasta do mês.

        Args:
            file_paths: Lista de caminhos de arquivos
            month: Mês para organização
            year: Ano para organização
            overwrite: Se True, sobrescreve arquivos existentes

        Returns:
            Resultado do upload com estatísticas
        """
        result = UploadResult(total_files=len(file_paths))

        if not file_paths:
            logger.warning("Nenhum arquivo para upload")
            return result

        logger.info("═══════════════════════════════════════════════════════════")
        logger.info(f"Iniciando upload para Google Drive: {len(file_paths)} arquivos")
        logger.info("═══════════════════════════════════════════════════════════")

        try:
            # Obtém/cria pasta do mês
            month_folder_id = self._get_month_folder(month, year)

            for file_path in file_paths:
                file_name = Path(file_path).name

                try:
                    upload_info = self.upload_file(
                        file_path, folder_id=month_folder_id, overwrite=overwrite
                    )

                    if upload_info:
                        result.uploaded_files += 1
                        result.file_details.append(
                            {
                                "file": file_name,
                                "id": upload_info.get("id"),
                                "link": upload_info.get("webViewLink"),
                                "skipped": upload_info.get("skipped", False),
                            }
                        )
                    else:
                        result.failed_files += 1
                        result.errors.append(f"Falha no upload: {file_name}")

                except Exception as e:
                    result.failed_files += 1
                    error_msg = f"Erro em {file_name}: {e}"
                    result.errors.append(error_msg)
                    logger.error(error_msg)

            # Log final
            logger.info("═══════════════════════════════════════════════════════════")
            logger.info("Upload concluído")
            logger.info(
                f"  Arquivos enviados: {result.uploaded_files}/{result.total_files}"
            )
            logger.info(f"  Falhas: {result.failed_files}")
            logger.info(f"  Taxa de sucesso: {result.success_rate:.1f}%")
            logger.info("═══════════════════════════════════════════════════════════")

            return result

        except Exception as e:
            error_msg = f"Erro crítico no upload: {e}"
            logger.error(error_msg)
            result.errors.append(error_msg)
            return result

    def test_connection(self) -> bool:
        """
        Testa conexão com o Google Drive.

        Returns:
            True se conexão bem-sucedida
        """
        try:
            service = self._get_service()

            # Tenta listar arquivos na pasta raiz
            service.files().list(
                q=f"'{self.root_folder_id}' in parents", pageSize=1, fields="files(id)"
            ).execute()

            logger.success("Conexão com Google Drive estabelecida com sucesso!")
            return True

        except FileNotFoundError as e:
            logger.error(f"Arquivo de credenciais não encontrado: {e}")
            return False
        except ValueError as e:
            logger.error(f"Configuração inválida: {e}")
            return False
        except HttpError as e:
            logger.error(f"Erro de API do Google Drive: {e}")
            return False
        except Exception as e:
            logger.error(f"Erro ao conectar com Google Drive: {e}")
            return False

    def revoke_token(self) -> bool:
        """
        Revoga o token salvo (para forçar novo login).

        Returns:
            True se token foi removido
        """
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
            logger.info("Token removido. Próxima execução exigirá novo login.")
            return True
        return False
