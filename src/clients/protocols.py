"""
Protocolos (interfaces) para clientes de rastreamento.

Seguindo o Princípio da Inversão de Dependência (DIP), os serviços
dependem de abstrações (Protocols) ao invés de implementações concretas.

Isso permite:
- Trocar implementações sem modificar os serviços
- Facilitar testes com mocks
- Suportar múltiplos sistemas de rastreamento
"""

from typing import Any, Dict, Iterator, List, Optional, Protocol


class TrackingClient(Protocol):
    """
    Interface para clientes de sistemas de rastreamento veicular.

    Define o contrato que qualquer cliente de rastreamento deve implementar
    para ser usado pelos serviços da aplicação.
    """

    def authenticate(self) -> Dict[str, Any]:
        """
        Realiza autenticação no sistema de rastreamento.

        Returns:
            Dados da resposta de autenticação
        """
        ...

    def list_vehicles(self) -> List[Dict[str, Any]]:
        """
        Lista todos os veículos disponíveis.

        Returns:
            Lista de veículos com id, nome e outros atributos
        """
        ...

    def get_vehicle_sensors(self, vehicle_id: int) -> Dict[str, Dict[str, Any]]:
        """
        Obtém mapa de sensores de um veículo.

        Args:
            vehicle_id: ID do veículo

        Returns:
            Mapa de parâmetro base -> info do sensor
            Exemplo: {"io_2_94": {"name": "rpm", "formula": "io_2_94*const0.25"}}
        """
        ...

    def get_history(
        self,
        vehicle_id: int,
        time_from: int,
        time_to: int,
    ) -> Iterator[List[Dict[str, Any]]]:
        """
        Busca histórico de mensagens de um veículo em páginas.

        Args:
            vehicle_id: ID do veículo
            time_from: Timestamp Unix início
            time_to: Timestamp Unix fim

        Yields:
            Páginas de mensagens (lista de dicts)
        """
        ...

    def apply_sensor_formula(self, raw_value: Any, formula: str) -> Optional[float]:
        """
        Aplica a fórmula de um sensor ao valor bruto.

        Args:
            raw_value: Valor bruto do parâmetro
            formula: Fórmula do sensor

        Returns:
            Valor calculado ou None se falhar
        """
        ...

    def logout(self) -> bool:
        """
        Encerra a sessão com o sistema de rastreamento.

        Returns:
            True se logout bem-sucedido
        """
        ...
