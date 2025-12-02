from clients.system_a_client import SystemAClient
from clients.system_b_client import SystemBClient
from core.logger import logger


def main():
    logger.info("Iniciando testes de integração...")

    client_a = SystemAClient()
    client_b = SystemBClient()

    print("Sistema A - Listando veículos...")
    print(client_a.listar_veiculos())

    print("Sistema B - Listando veículos...")
    print(client_b.listar_veiculos())


if __name__ == "__main__":
    main()
