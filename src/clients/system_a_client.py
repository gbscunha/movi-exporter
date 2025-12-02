from core.config import settings
from .base_client import BaseClient

class SystemAClient(BaseClient):
    def __init__(self):
        super().__init__(settings.SYSTEM_A_BASE_URL, settings.SYSTEM_A_TOKEN)

    def listar_veiculos(self):
        return self.get("veiculos")

    def buscar_historico(self, veiculo_id: str, mes: str):
        return self.get("historico", params={
            "veiculoId": veiculo_id,
            "mes": mes
        })
