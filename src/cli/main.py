from clients.system_a_client import SystemAClient
from core.logger import logger


def main():
    logger.info("Iniciando testes de integração...")

    client_a = SystemAClient()

    print("Sistema A - Listando veículos...")
    print(client_a.listar_veiculos())

if __name__ == "__main__":
    main()
