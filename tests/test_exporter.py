"""
Script de exemplo para testar o módulo DataExporter.

Este script demonstra como usar o DataExporter para exportar dados
de veículos e histórico para CSV e Excel.
"""

import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.exporter import DataExporter
from src.services.normalizer import DataNormalizer
from src.core.logger import logger


def test_vehicle_export():
    """Testa exportação de lista de veículos."""
    logger.info("=" * 60)
    logger.info("TESTE 1: Exportação de Lista de Veículos")
    logger.info("=" * 60)
    
    # Dados de exemplo (simulando dados normalizados)
    vehicles = [
        {
            "id": "VEI001",
            "name": "Caminhão Mercedes 1",
            "plate": "ABC-1234",
            "system_source": "system_a",
            "raw_data": {"veiculoId": "VEI001", "nome": "Caminhão Mercedes 1"}
        },
        {
            "id": "VEI002",
            "name": "Van Fiat 2",
            "plate": "DEF-5678",
            "system_source": "system_a",
            "raw_data": {"veiculoId": "VEI002", "nome": "Van Fiat 2"}
        },
        {
            "id": "VEI003",
            "name": "Carro Toyota 3",
            "plate": "GHI-9012",
            "system_source": "system_a",
            "raw_data": {"veiculoId": "VEI003", "nome": "Carro Toyota 3"}
        }
    ]
    
    # Cria instância do exportador
    exporter = DataExporter(base_export_dir="./exports_test")
    
    # Exporta para CSV
    logger.info("\n📄 Exportando veículos para CSV...")
    csv_path = exporter.export_vehicles_to_csv(vehicles, month=10, year=2024)
    logger.info(f"Arquivo CSV criado: {csv_path}")
    
    # Exporta para Excel
    logger.info("\n📊 Exportando veículos para Excel...")
    excel_path = exporter.export_vehicles_to_excel(vehicles, month=10, year=2024)
    logger.info(f"Arquivo Excel criado: {excel_path}")
    
    print()


def test_history_export():
    """Testa exportação de histórico de um veículo."""
    logger.info("=" * 60)
    logger.info("TESTE 2: Exportação de Histórico de Veículo")
    logger.info("=" * 60)
    
    # Dados de exemplo (simulando histórico normalizado com novos campos)
    history = [
        {
            "vehicle_id": "VEI001",
            "timestamp": "2024-10-01T08:00:00",
            "latitude": -23.5505,
            "longitude": -46.6333,
            "speed": 45.5,
            "odometer": 15000.0,
            "ignition": True,
            "address": "Av. Paulista, 1000 - São Paulo, SP",
            "fuel_level": 31.27,
            "rpm": 1198.0,
            "battery_voltage": 12.47,
            "driver": "João Silva",
            "system_source": "system_a",
            "raw_data": {}
        },
        {
            "vehicle_id": "VEI001",
            "timestamp": "2024-10-01T09:00:00",
            "latitude": -23.5489,
            "longitude": -46.6388,
            "speed": 60.0,
            "odometer": 15050.0,
            "ignition": True,
            "address": "Av. Brigadeiro Faria Lima, 500 - São Paulo, SP",
            "fuel_level": 30.84,
            "rpm": 2148.0,
            "battery_voltage": 13.38,
            "driver": "João Silva",
            "system_source": "system_a",
            "raw_data": {}
        },
        {
            "vehicle_id": "VEI001",
            "timestamp": "2024-10-01T10:00:00",
            "latitude": -23.5629,
            "longitude": -46.6544,
            "speed": 0.0,
            "odometer": 15100.0,
            "ignition": False,
            "address": "Rua Augusta, 2000 - São Paulo, SP",
            "fuel_level": 29.55,
            "rpm": 0.0,
            "battery_voltage": 12.02,
            "driver": None,
            "system_source": "system_a",
            "raw_data": {}
        }
    ]
    
    # Cria instância do exportador
    exporter = DataExporter(base_export_dir="./exports_test")
    
    # Exporta para CSV
    logger.info("\n📄 Exportando histórico para CSV...")
    csv_path = exporter.export_history_to_csv(
        history=history,
        vehicle_id="VEI001",
        month=10,
        year=2024
    )
    logger.info(f"Arquivo CSV criado: {csv_path}")
    
    # Exporta para Excel
    logger.info("\n📊 Exportando histórico para Excel...")
    excel_path = exporter.export_history_to_excel(
        history=history,
        vehicle_id="VEI001",
        month=10,
        year=2024
    )
    logger.info(f"Arquivo Excel criado: {excel_path}")
    
    print()


def test_consolidated_export():
    """Testa exportação consolidada de múltiplos veículos."""
    logger.info("=" * 60)
    logger.info("TESTE 3: Exportação Consolidada de Múltiplos Veículos")
    logger.info("=" * 60)
    
    # Dados de exemplo (simulando histórico de múltiplos veículos com novos campos)
    all_history = {
        "VEI001": [
            {
                "vehicle_id": "VEI001",
                "timestamp": "2024-10-01T08:00:00",
                "latitude": -23.5505,
                "longitude": -46.6333,
                "speed": 45.5,
                "odometer": 15000.0,
                "ignition": True,
                "address": "Av. Paulista, 1000",
                "fuel_level": 31.27,
                "rpm": 1198.0,
                "battery_voltage": 12.47,
                "driver": "João Silva",
                "system_source": "system_a",
                "raw_data": {}
            },
            {
                "vehicle_id": "VEI001",
                "timestamp": "2024-10-01T09:00:00",
                "latitude": -23.5489,
                "longitude": -46.6388,
                "speed": 60.0,
                "odometer": 15050.0,
                "ignition": True,
                "address": "Av. Faria Lima, 500",
                "fuel_level": 30.84,
                "rpm": 2148.0,
                "battery_voltage": 13.38,
                "driver": "João Silva",
                "system_source": "system_a",
                "raw_data": {}
            }
        ],
        "VEI002": [
            {
                "vehicle_id": "VEI002",
                "timestamp": "2024-10-01T08:30:00",
                "latitude": -23.5629,
                "longitude": -46.6544,
                "speed": 30.0,
                "odometer": 8000.0,
                "ignition": True,
                "address": "Rua Augusta, 2000",
                "fuel_level": 45.50,
                "rpm": 1500.0,
                "battery_voltage": 13.10,
                "driver": "Maria Santos",
                "system_source": "system_a",
                "raw_data": {}
            },
            {
                "vehicle_id": "VEI002",
                "timestamp": "2024-10-01T09:30:00",
                "latitude": -23.5700,
                "longitude": -46.6600,
                "speed": 0.0,
                "odometer": 8025.0,
                "ignition": False,
                "address": "Rua da Consolação, 1500",
                "fuel_level": 44.80,
                "rpm": 0.0,
                "battery_voltage": 12.50,
                "driver": None,
                "system_source": "system_a",
                "raw_data": {}
            }
        ]
    }
    
    # Informações dos veículos para inclusão de nome e placa
    vehicles_info = {
        "VEI001": {"name": "Caminhão Mercedes 1", "plate": "ABC-1234"},
        "VEI002": {"name": "Van Fiat 2", "plate": "DEF-5678"}
    }
    
    # Cria instância do exportador
    exporter = DataExporter(base_export_dir="./exports_test")
    
    # Exporta consolidado para CSV
    logger.info("\n📄 Exportando histórico consolidado para CSV...")
    csv_path = exporter.export_consolidated_history_to_csv(
        all_history=all_history,
        month=10,
        year=2024,
        vehicles_info=vehicles_info
    )
    logger.info(f"Arquivo CSV consolidado criado: {csv_path}")
    
    # Exporta consolidado para Excel
    logger.info("\n📊 Exportando histórico consolidado para Excel...")
    excel_path = exporter.export_consolidated_history_to_excel(
        all_history=all_history,
        month=10,
        year=2024,
        vehicles_info=vehicles_info
    )
    logger.info(f"Arquivo Excel consolidado criado: {excel_path}")
    
    print()


def test_export_stats():
    """Testa obtenção de estatísticas de exportação."""
    logger.info("=" * 60)
    logger.info("TESTE 4: Estatísticas de Exportação")
    logger.info("=" * 60)
    
    exporter = DataExporter(base_export_dir="./exports_test")
    
    # Obtém estatísticas
    stats = exporter.get_export_stats(month=10, year=2024)
    
    logger.info("\n📊 Estatísticas de Exportação:")
    logger.info(f"  Mês/Ano: {stats['month']:02d}/{stats['year']}")
    logger.info(f"  Diretório: {stats['directory']}")
    logger.info(f"  Existe: {stats['exists']}")
    
    if stats['exists']:
        logger.info(f"  Total de arquivos: {stats['total_files']}")
        logger.info(f"  Arquivos CSV: {stats['csv_files']}")
        logger.info(f"  Arquivos Excel: {stats['excel_files']}")
        logger.info(f"  Tamanho total: {stats['total_size_mb']} MB")
    
    print()


def test_integration_with_normalizer():
    """Testa integração entre Normalizer e Exporter."""
    logger.info("=" * 60)
    logger.info("TESTE 5: Integração Normalizer + Exporter")
    logger.info("=" * 60)
    
    # Dados brutos simulando resposta da API do System A (com novos campos)
    raw_vehicles = [
        {
            "veiculoId": "VEI001",
            "nome": "Caminhão Mercedes 1",
            "placa": "ABC-1234"
        },
        {
            "veiculoId": "VEI002",
            "nome": "Van Fiat 2",
            "placa": "DEF-5678"
        }
    ]
    
    raw_history = [
        {
            "veiculoId": "VEI001",
            "dataHora": "2024-10-15T14:30:00",
            "latitude": -23.5505,
            "longitude": -46.6333,
            "velocidade": 45.5,
            "odometro": 15000.0,
            "ignicao": True,
            "endereco": "Av. Paulista, 1000",
            "nivelCombustivel": 31.27,
            "rpm": 1198.0,
            "voltagemBateria": 12.47,
            "motorista": "João Silva"
        },
        {
            "veiculoId": "VEI001",
            "dataHora": "2024-10-15T15:30:00",
            "latitude": -23.5489,
            "longitude": -46.6388,
            "velocidade": 60.0,
            "odometro": 15050.0,
            "ignicao": True,
            "endereco": "Av. Faria Lima, 500",
            "nivelCombustivel": 30.84,
            "rpm": 2148.0,
            "voltagemBateria": 13.38,
            "motorista": "João Silva"
        }
    ]
    
    # Normaliza os dados
    logger.info("\n🔄 Normalizando dados...")
    normalizer = DataNormalizer()
    normalized_vehicles = normalizer.normalize_vehicle_list(raw_vehicles)
    normalized_history = normalizer.normalize_history(raw_history)
    
    # Exporta os dados normalizados
    logger.info("\n📤 Exportando dados normalizados...")
    exporter = DataExporter(base_export_dir="./exports_test")
    
    # Exporta veículos
    vehicles_csv = exporter.export_vehicles_to_csv(
        normalized_vehicles,
        month=10,
        year=2024
    )
    
    # Exporta histórico
    history_csv = exporter.export_history_to_csv(
        normalized_history,
        vehicle_id="VEI001",
        month=10,
        year=2024
    )
    
    logger.success("\n✅ Integração testada com sucesso!")
    logger.info(f"  Veículos: {vehicles_csv}")
    logger.info(f"  Histórico: {history_csv}")
    
    print()


def main():
    """Executa todos os testes."""
    logger.info("\n" + "=" * 60)
    logger.info("🚀 INICIANDO TESTES DO DATA EXPORTER")
    logger.info("=" * 60 + "\n")
    
    try:
        # Executa os testes
        test_vehicle_export()
        test_history_export()
        test_consolidated_export()
        test_export_stats()
        test_integration_with_normalizer()
        
        logger.success("\n" + "=" * 60)
        logger.success("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        logger.success("=" * 60)
        logger.info("\n💡 Os arquivos foram exportados para: ./exports_test/")
        logger.info("💡 Verifique os arquivos CSV e Excel gerados.")
        
    except Exception as e:
        logger.error(f"\n❌ Erro durante os testes: {e}")
        raise


if __name__ == "__main__":
    main()

