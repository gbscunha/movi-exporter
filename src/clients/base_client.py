"""
Módulo base para clientes HTTP.

Fornece duas classes base:
- BaseClient: Cliente tradicional com Bearer Token (REST)
- StatefulClient: Cliente com sessão stateful (para APIs como Wialon)
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import requests


class BaseClient:
    """
    Cliente HTTP base com autenticação Bearer Token.
    
    Adequado para APIs REST tradicionais.
    """
    
    def __init__(self, base_url: str, token: str):
        """
        Inicializa o cliente.
        
        Args:
            base_url: URL base da API
            token: Token de autenticação Bearer
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        """Retorna headers padrão com autenticação Bearer."""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Executa requisição GET.
        
        Args:
            path: Caminho do endpoint (será concatenado à base_url)
            params: Query parameters opcionais
            
        Returns:
            Resposta JSON parseada
            
        Raises:
            Exception: Se a requisição falhar
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self._session.get(url, headers=self._headers(), params=params)

        if response.status_code != 200:
            raise Exception(f"Erro na requisição GET {url}: {response.text}")

        return response.json()
    
    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Executa requisição POST.
        
        Args:
            path: Caminho do endpoint
            data: Dados a enviar no body
            
        Returns:
            Resposta JSON parseada
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self._session.post(url, headers=self._headers(), json=data)

        if response.status_code not in (200, 201):
            raise Exception(f"Erro na requisição POST {url}: {response.text}")

        return response.json()


class StatefulClient(ABC):
    """
    Cliente base para APIs stateful com sessão.
    
    Adequado para APIs que usam session ID ao invés de Bearer Token.
    Subclasses devem implementar os métodos abstratos.
    """
    
    def __init__(self, base_url: str):
        """
        Inicializa o cliente stateful.
        
        Args:
            base_url: URL base da API
        """
        self.base_url = base_url.rstrip("/")
        self.session_id: Optional[str] = None
        self._session = requests.Session()
    
    @abstractmethod
    def authenticate(self) -> Dict[str, Any]:
        """
        Realiza autenticação e obtém session ID.
        
        Deve ser implementado pela subclasse.
        
        Returns:
            Dados da resposta de autenticação
        """
        pass
    
    @abstractmethod
    def _request(self, service: str, params: Dict[str, Any]) -> Any:
        """
        Executa requisição à API com session ID.
        
        Deve ser implementado pela subclasse.
        
        Args:
            service: Nome do serviço/endpoint
            params: Parâmetros da requisição
            
        Returns:
            Resposta parseada
        """
        pass
    
    def is_authenticated(self) -> bool:
        """Verifica se existe uma sessão ativa."""
        return self.session_id is not None
    
    def ensure_authenticated(self) -> None:
        """Garante que existe uma sessão ativa."""
        if not self.is_authenticated():
            self.authenticate()
    
    def logout(self) -> bool:
        """
        Encerra a sessão.
        
        Returns:
            True se logout bem-sucedido
        """
        self.session_id = None
        return True