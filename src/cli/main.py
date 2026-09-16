"""
Interface de linha de comando do Movi Exporter App.

Comandos disponíveis:
- test: Testa conexão com a API Wialon
- list: Lista veículos disponíveis
- export: Exporta dados históricos mensais

Todos os comandos que falam com a Wialon aceitam `--account 1|2` para
escolher qual conta usar (WIALON_TOKEN ou WIALON_TOKEN_2). Útil para
testes via terminal sem depender da GUI.
"""

import argparse
import sys
from datetime import datetime
from typing import List, Optional

from src.core.config import settings
from src.core.logger import logger
from src.core.service_factory import build_vehicle_service
from src.services.uploader import DriveUploader


def _account_label(account: int) -> str:
    """Nome humano da conta para mensagens e subpastas."""
    return f"Conta {account}"


def cmd_test(account: int = 1) -> int:
    """Testa conexão com a API Wialon."""
    print(f"Testando conexão com Wialon ({_account_label(account)})...")

    try:
        service = build_vehicle_service(account=account)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    success = service.test_connection()

    if success:
        print("✅ Conexão bem-sucedida!")
        return 0
    else:
        env_var = "WIALON_TOKEN" if account == 1 else "WIALON_TOKEN_2"
        print(f"❌ Falha na conexão. Verifique o {env_var} no .env")
        return 1


def cmd_test_drive() -> int:
    """Testa conexão com o Google Drive."""
    print("Testando conexão com Google Drive...")

    uploader = DriveUploader()
    success = uploader.test_connection()

    if success:
        print("✅ Conexão com Google Drive bem-sucedida!")
        return 0
    else:
        print("❌ Falha na conexão com Google Drive.")
        print("   Verifique:")
        print("   - credentials.json existe e é válido")
        print("   - GOOGLE_DRIVE_FOLDER_ID está configurado no .env")
        print("   - A pasta foi compartilhada com o email do Service Account")
        return 1


def cmd_list(account: int = 1) -> int:
    """Lista veículos disponíveis."""
    print(f"Buscando veículos ({_account_label(account)})...")

    try:
        service = build_vehicle_service(account=account)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    try:
        vehicles = service.list_vehicles()

        if not vehicles:
            print("Nenhum veículo encontrado.")
            return 0

        print(f"\n{'=' * 60}")
        print(f"{'ID':>12} | {'Nome':<30} | {'Placa':<15}")
        print(f"{'=' * 60}")

        for vehicle in vehicles:
            print(
                f"{vehicle['id']:>12} | {vehicle['name']:<30} | {vehicle.get('plate', ''):<15}"
            )

        print(f"{'=' * 60}")
        print(f"Total: {len(vehicles)} veículos")

        return 0

    except Exception as e:
        print(f"❌ Erro ao listar veículos: {e}")
        return 1


def cmd_export(
    month: int,
    year: int,
    vehicle_ids: Optional[List[int]] = None,
    format: str = "csv",
    consolidated: bool = True,
    output_dir: Optional[str] = None,
    upload: bool = False,
    account: int = 1,
    include_addresses: bool = False,
) -> int:
    """
    Exporta dados históricos mensais.

    Args:
        month: Mês (1-12)
        year: Ano
        vehicle_ids: IDs específicos de veículos (None = todos)
        format: Formato de saída (csv, xlsx, both)
        consolidated: Se deve gerar arquivo consolidado
        output_dir: Diretório de saída customizado
        upload: Se deve fazer upload para Google Drive
        account: Conta Wialon a usar (1 ou 2)
        include_addresses: Se deve geocodificar e preencher a coluna Localização
    """
    print(f"Iniciando exportação ({_account_label(account)}): {month:02d}/{year}")

    if vehicle_ids:
        print(f"Veículos: {vehicle_ids}")
    else:
        print("Veículos: todos")

    print(f"Formato: {format}")
    print(f"Consolidado: {'sim' if consolidated else 'não'}")
    print(f"Incluir endereço: {'sim' if include_addresses else 'não'}")
    print(f"Upload Drive: {'sim' if upload else 'não'}")
    print()

    try:
        service = build_vehicle_service(account=account, export_dir=output_dir)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    # Quando Conta 2 está em uso, queremos subpasta dedicada
    # (mesmo comportamento da GUI quando ambas estão configuradas).
    account_name = (
        _account_label(account) if account == 2 or settings.WIALON_TOKEN_2 else None
    )

    try:
        result = service.export_monthly_data(
            month=month,
            year=year,
            vehicle_ids=vehicle_ids,
            export_format=format,
            consolidated=consolidated,
            upload_to_drive=upload,
            include_addresses=include_addresses,
            account_name=account_name,
        )

        # Exibe resultado
        print()
        print("=" * 60)
        print("RESULTADO DA EXPORTAÇÃO")
        print("=" * 60)
        print(f"Conta: {_account_label(account)}")
        print(f"Período: {month:02d}/{year}")
        print(
            f"Veículos processados: {result.processed_vehicles}/{result.total_vehicles}"
        )
        print(f"Veículos com erro: {result.failed_vehicles}")
        print(f"Total de registros: {result.total_records}")
        print(f"Taxa de sucesso: {result.success_rate:.1f}%")
        print()

        if result.exported_files:
            print("Arquivos gerados:")
            for f in result.exported_files:
                print(f"  📄 {f}")

        if result.upload_result:
            print()
            print("Upload Google Drive:")
            print(
                f"  Arquivos enviados: {result.upload_result.uploaded_files}/{result.upload_result.total_files}"
            )
            if result.upload_result.failed_files > 0:
                print(f"  Falhas: {result.upload_result.failed_files}")
            for detail in result.upload_result.file_details:
                status = "⏭️ ignorado" if detail.get("skipped") else "✅"
                print(f"  {status} {detail['file']}")

        if result.errors:
            print()
            print("Erros:")
            for e in result.errors:
                print(f"  ❌ {e}")

        print("=" * 60)

        return 0 if result.failed_vehicles == 0 else 1

    except Exception as e:
        print(f"❌ Erro na exportação: {e}")
        logger.exception("Erro na exportação")
        return 1


def parse_vehicle_ids(value: str) -> List[int]:
    """Converte string de IDs para lista de inteiros."""
    if not value:
        return []

    ids = []
    for part in value.split(","):
        part = part.strip()
        if part:
            try:
                ids.append(int(part))
            except ValueError:
                raise argparse.ArgumentTypeError(f"ID de veículo inválido: {part}")
    return ids


def _add_account_arg(subparser: argparse.ArgumentParser) -> None:
    """Adiciona o argumento `--account` a um subparser."""
    subparser.add_argument(
        "--account",
        "-a",
        type=int,
        choices=[1, 2],
        default=1,
        metavar="1|2",
        help="Conta Wialon (1=WIALON_TOKEN, 2=WIALON_TOKEN_2). Padrão: 1",
    )


def main():
    """Ponto de entrada principal."""
    parser = argparse.ArgumentParser(
        description="Movi Exporter App - Exportação de dados de veículos Wialon",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python -m src.cli.main test
  python -m src.cli.main test --account 2
  python -m src.cli.main list
  python -m src.cli.main list --account 2
  python -m src.cli.main export --month 12 --year 2025
  python -m src.cli.main export --month 12 --year 2025 --vehicles 123,456
  python -m src.cli.main export --month 12 --year 2025 --format xlsx
  python -m src.cli.main export --month 12 --year 2025 --upload --account 2
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")

    # Comando: test (aceita --account)
    test_parser = subparsers.add_parser("test", help="Testa conexão com a API Wialon")
    _add_account_arg(test_parser)

    # Comando: test-drive (Drive não tem conta)
    subparsers.add_parser("test-drive", help="Testa conexão com o Google Drive")

    # Comando: list (aceita --account)
    list_parser = subparsers.add_parser("list", help="Lista veículos disponíveis")
    _add_account_arg(list_parser)

    # Comando: export
    export_parser = subparsers.add_parser("export", help="Exporta dados históricos")

    # Data atual para valores padrão
    now = datetime.now()
    default_month = now.month - 1 if now.month > 1 else 12
    default_year = now.year if now.month > 1 else now.year - 1

    export_parser.add_argument(
        "--month",
        "-m",
        type=int,
        default=default_month,
        choices=range(1, 13),
        metavar="1-12",
        help=f"Mês para exportar (padrão: {default_month})",
    )

    export_parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=default_year,
        help=f"Ano para exportar (padrão: {default_year})",
    )

    export_parser.add_argument(
        "--vehicles",
        "-v",
        type=parse_vehicle_ids,
        default=None,
        metavar="ID1,ID2,...",
        help="IDs de veículos específicos (separados por vírgula)",
    )

    export_parser.add_argument(
        "--format",
        "-f",
        choices=["csv", "xlsx", "both"],
        default="csv",
        help="Formato de exportação (padrão: csv)",
    )

    export_parser.add_argument(
        "--no-consolidated",
        action="store_true",
        help="Não gerar arquivo consolidado",
    )

    export_parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        metavar="DIR",
        help="Diretório de saída customizado",
    )

    export_parser.add_argument(
        "--upload",
        "-u",
        action="store_true",
        help="Faz upload dos arquivos para Google Drive",
    )

    export_parser.add_argument(
        "--addresses",
        "-A",
        action="store_true",
        help="Geocodifica coordenadas e preenche a coluna Localização (mais lento)",
    )

    _add_account_arg(export_parser)

    # Parse args
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Executa comando
    if args.command == "test":
        return cmd_test(account=args.account)

    elif args.command == "test-drive":
        return cmd_test_drive()

    elif args.command == "list":
        return cmd_list(account=args.account)

    elif args.command == "export":
        return cmd_export(
            month=args.month,
            year=args.year,
            vehicle_ids=args.vehicles,
            format=args.format,
            consolidated=not args.no_consolidated,
            output_dir=args.output,
            upload=args.upload,
            account=args.account,
            include_addresses=args.addresses,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
