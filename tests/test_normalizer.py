"""
Script de exemplo para testar o DataNormalizer
"""

import sys

sys.path.insert(0, "/Users/gbscunha/dev/movi_exporter_app/src")

from services.normalizer import DataNormalizer
from core.logger import logger


def test_vehicle_normalization():
    """Testa normalização de lista de veículos"""
    logger.info("=" * 60)
    logger.info("TESTE 1: Normalização de Veículos")
    logger.info("=" * 60)

    # Dados simulados do System A
    raw_vehicles = [
        {"veiculoId": "VEI001", "nome": "Caminhão Mercedes", "placa": "ABC-1234"},
        {"veiculoId": "VEI002", "nome": "Van Sprinter", "placa": "XYZ-5678"},
        {"veiculoId": "VEI003", "nome": "Carro Passeio", "placa": "DEF-9012"},
    ]

    normalizer = DataNormalizer()
    normalized = normalizer.normalize_vehicle_list(raw_vehicles, system="system_a")

    logger.info(f"\nVeículos normalizados: {len(normalized)}")
    for vehicle in normalized:
        logger.info(
            f"  - ID: {vehicle['id']}, Nome: {vehicle['name']}, Placa: {vehicle['plate']}"
        )

    return normalized


def test_history_normalization():
    """Testa normalização de dados históricos"""
    logger.info("\n" + "=" * 60)
    logger.info("TESTE 2: Normalização de Histórico")
    logger.info("=" * 60)

    # Dados simulados do System A (incluindo novos campos do cliente)
    raw_history = [
        {
            "veiculoId": "VEI001",
            "dataHora": "2024-01-15T08:30:00",
            "latitude": -23.5505,
            "longitude": -46.6333,
            "velocidade": 45.5,
            "odometro": 15000.0,
            "ignicao": True,
            "endereco": "Av. Paulista, 1000 - São Paulo",
            "nivelCombustivel": 31.27,
            "rpm": 1198.0,
            "voltagemBateria": 12.47,
            "motorista": "João Silva",
        },
        {
            "veiculoId": "VEI001",
            "dataHora": "2024-01-15T09:00:00",
            "latitude": -23.5520,
            "longitude": -46.6350,
            "velocidade": 60.0,
            "odometro": 15025.5,
            "ignicao": True,
            "endereco": "Av. Brigadeiro Luís Antônio - São Paulo",
            "nivelCombustivel": 30.84,
            "rpm": 2148.0,
            "voltagemBateria": 13.38,
            "motorista": "João Silva",
        },
        {
            "veiculoId": "VEI001",
            "dataHora": "2024-01-15T09:30:00",
            "latitude": -23.5535,
            "longitude": -46.6370,
            "velocidade": 0.0,
            "odometro": 15050.0,
            "ignicao": False,
            "endereco": "Rua Augusta, 500 - São Paulo",
            "nivelCombustivel": 29.55,
            "rpm": 0.0,
            "voltagemBateria": 12.02,
            "motorista": None,
        },
    ]

    normalizer = DataNormalizer()
    normalized = normalizer.normalize_history(raw_history, system="system_a")

    logger.info(f"\nRegistros históricos normalizados: {len(normalized)}")
    for record in normalized:
        logger.info(
            f"  - {record['timestamp']} | "
            f"Velocidade: {record['speed']} km/h | "
            f"Ignição: {'Ligada' if record['ignition'] else 'Desligada'} | "
            f"Odômetro: {record['odometer']} km | "
            f"Combustível: {record['fuel_level']} L | "
            f"RPM: {record['rpm']} | "
            f"Bateria: {record['battery_voltage']} V"
        )

    return normalized


def test_add_new_system():
    """Testa adição de um novo sistema"""
    logger.info("\n" + "=" * 60)
    logger.info("TESTE 3: Adição de Novo Sistema (System B)")
    logger.info("=" * 60)

    normalizer = DataNormalizer()

    # Adicionar mapeamento para System B (exemplo hipotético)
    system_b_mapping = {
        "vehicle_id": "deviceId",
        "vehicle_name": "deviceName",
        "plate": "licensePlate",
        "timestamp": "eventTime",
        "latitude": "gps.lat",
        "longitude": "gps.lng",
        "speed": "speedKmh",
        "odometer": "totalKm",
        "ignition": "engineOn",
        "address": "location",
        # Novos campos
        "fuel_level": "fuelLevel",
        "rpm": "engineRpm",
        "battery_voltage": "batteryVoltage",
        "driver": "driverName",
    }

    normalizer.add_system_mapping("system_b", system_b_mapping)

    # Dados simulados do System B
    raw_vehicles_b = [
        {"deviceId": "DEV001", "deviceName": "Truck 01", "licensePlate": "GHI-3456"}
    ]

    normalized = normalizer.normalize_vehicle_list(raw_vehicles_b, system="system_b")

    logger.info(f"\nVeículo do System B normalizado:")
    logger.info(
        f"  - ID: {normalized[0]['id']}, Nome: {normalized[0]['name']}, Placa: {normalized[0]['plate']}"
    )
    logger.info(f"  - Sistema de origem: {normalized[0]['system_source']}")

    # Listar sistemas suportados
    systems = normalizer.get_supported_systems()
    logger.info(f"\nSistemas suportados: {systems}")

    return normalized


def test_missing_fields():
    """Testa tratamento de campos ausentes"""
    logger.info("\n" + "=" * 60)
    logger.info("TESTE 4: Tratamento de Campos Ausentes")
    logger.info("=" * 60)

    # Dados incompletos
    raw_history = [
        {
            "veiculoId": "VEI001",
            "dataHora": "2024-01-15T10:00:00",
            # latitude e longitude ausentes
            # velocidade ausente
            # outros campos ausentes (incluindo novos campos)
        }
    ]

    normalizer = DataNormalizer()
    normalized = normalizer.normalize_history(raw_history, system="system_a")

    logger.info(f"\nRegistro com campos ausentes normalizado:")
    record = normalized[0]
    logger.info(f"  - Vehicle ID: {record['vehicle_id']}")
    logger.info(f"  - Timestamp: {record['timestamp']}")
    logger.info(f"  - Latitude: {record['latitude']} (padrão)")
    logger.info(f"  - Longitude: {record['longitude']} (padrão)")
    logger.info(f"  - Speed: {record['speed']} (padrão)")
    logger.info(f"  - Odometer: {record['odometer']} (padrão)")
    logger.info(f"  - Ignition: {record['ignition']} (padrão)")
    logger.info(f"  - Address: '{record['address']}' (padrão)")
    logger.info(f"  - Fuel Level: {record['fuel_level']} (padrão)")
    logger.info(f"  - RPM: {record['rpm']} (padrão)")
    logger.info(f"  - Battery Voltage: {record['battery_voltage']} (padrão)")
    logger.info(f"  - Driver: {record['driver']} (padrão)")

    return normalized


if __name__ == "__main__":
    logger.info("\n🚀 Iniciando testes do DataNormalizer\n")

    try:
        # Executar testes
        test_vehicle_normalization()
        test_history_normalization()
        test_add_new_system()
        test_missing_fields()

        logger.success("\n✅ Todos os testes concluídos com sucesso!")

    except Exception as e:
        logger.error(f"\n❌ Erro durante os testes: {e}")
        raise
