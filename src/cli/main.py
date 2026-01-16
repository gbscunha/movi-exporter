"""
Interface de linha de comando do Movi Exporter App.

Comandos disponíveis:
- test: Testa conexão com a API Wialon
- list: Lista veículos disponíveis
- export: Exporta dados históricos mensais
"""

import argparse
import sys
from datetime import datetime
from typing import List, Optional

from src.core.logger import logger
from src.services.vehicle_service import VehicleService


def cmd_test() -> int:
    """Testa conexão com a API Wialon."""
    print("Testando conexão com Wialon...")
    
    service = VehicleService()
    success = service.test_connection()
    
    if success:
        print("✅ Conexão bem-sucedida!")
        return 0
    else:
        print("❌ Falha na conexão. Verifique o token WIALON_TOKEN no .env")
        return 1


def cmd_list() -> int:
    """Lista veículos disponíveis."""
    print("Buscando veículos...")
    
    service = VehicleService()
    
    try:
        vehicles = service.list_vehicles()
        
        if not vehicles:
            print("Nenhum veículo encontrado.")
            return 0
        
        print(f"\n{'='*60}")
        print(f"{'ID':>12} | {'Nome':<30} | {'Placa':<15}")
        print(f"{'='*60}")
        
        for v in vehicles:
            print(f"{v['id']:>12} | {v['name']:<30} | {v.get('plate', ''):<15}")
        
        print(f"{'='*60}")
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
    """
    print(f"Iniciando exportação: {month:02d}/{year}")
    
    if vehicle_ids:
        print(f"Veículos: {vehicle_ids}")
    else:
        print("Veículos: todos")
    
    print(f"Formato: {format}")
    print(f"Consolidado: {'sim' if consolidated else 'não'}")
    print()
    
    service = VehicleService(export_dir=output_dir)
    
    try:
        result = service.export_monthly_data(
            month=month,
            year=year,
            vehicle_ids=vehicle_ids,
            export_format=format,
            consolidated=consolidated,
        )
        
        # Exibe resultado
        print()
        print("=" * 60)
        print("RESULTADO DA EXPORTAÇÃO")
        print("=" * 60)
        print(f"Período: {month:02d}/{year}")
        print(f"Veículos processados: {result.processed_vehicles}/{result.total_vehicles}")
        print(f"Veículos com erro: {result.failed_vehicles}")
        print(f"Total de registros: {result.total_records}")
        print(f"Taxa de sucesso: {result.success_rate:.1f}%")
        print()
        
        if result.exported_files:
            print("Arquivos gerados:")
            for f in result.exported_files:
                print(f"  📄 {f}")
        
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
                raise argparse.ArgumentTypeError(
                    f"ID de veículo inválido: {part}"
                )
    return ids


def main():
    """Ponto de entrada principal."""
    parser = argparse.ArgumentParser(
        description="Movi Exporter App - Exportação de dados de veículos Wialon",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python -m src.cli.main test
  python -m src.cli.main list
  python -m src.cli.main export --month 12 --year 2025
  python -m src.cli.main export --month 12 --year 2025 --vehicles 123,456
  python -m src.cli.main export --month 12 --year 2025 --format xlsx
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")
    
    # Comando: test
    subparsers.add_parser("test", help="Testa conexão com a API Wialon")
    
    # Comando: list
    subparsers.add_parser("list", help="Lista veículos disponíveis")
    
    # Comando: export
    export_parser = subparsers.add_parser("export", help="Exporta dados históricos")
    
    # Data atual para valores padrão
    now = datetime.now()
    default_month = now.month - 1 if now.month > 1 else 12
    default_year = now.year if now.month > 1 else now.year - 1
    
    export_parser.add_argument(
        "--month", "-m",
        type=int,
        default=default_month,
        choices=range(1, 13),
        metavar="1-12",
        help=f"Mês para exportar (padrão: {default_month})"
    )
    
    export_parser.add_argument(
        "--year", "-y",
        type=int,
        default=default_year,
        help=f"Ano para exportar (padrão: {default_year})"
    )
    
    export_parser.add_argument(
        "--vehicles", "-v",
        type=parse_vehicle_ids,
        default=None,
        metavar="ID1,ID2,...",
        help="IDs de veículos específicos (separados por vírgula)"
    )
    
    export_parser.add_argument(
        "--format", "-f",
        choices=["csv", "xlsx", "both"],
        default="csv",
        help="Formato de exportação (padrão: csv)"
    )
    
    export_parser.add_argument(
        "--no-consolidated",
        action="store_true",
        help="Não gerar arquivo consolidado"
    )
    
    export_parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        metavar="DIR",
        help="Diretório de saída customizado"
    )
    
    # Parse args
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Executa comando
    if args.command == "test":
        return cmd_test()
    
    elif args.command == "list":
        return cmd_list()
    
    elif args.command == "export":
        return cmd_export(
            month=args.month,
            year=args.year,
            vehicle_ids=args.vehicles,
            format=args.format,
            consolidated=not args.no_consolidated,
            output_dir=args.output,
        )
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
