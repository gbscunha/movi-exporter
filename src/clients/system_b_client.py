from core.config import settings
from .base_client import BaseClient

class SystemBClient(BaseClient):
    def __init__(self):
        super().__init__(settings.SYSTEM_B_BASE_URL, settings.SYSTEM_B_TOKEN)

    def listar_veiculos(self):
        return self.get("vehicles")

    def buscar_historico(self, device_id: str, month: str):
        return self.get("history", params={
            "device": device_id,
            "month": month
        })
