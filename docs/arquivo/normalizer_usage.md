# 📚 Guia de Uso do DataNormalizer

## Visão Geral

O `DataNormalizer` é responsável por converter dados de diferentes sistemas de rastreamento para um formato padronizado. Atualmente suporta o Wialon, mas está preparado para adicionar novos sistemas no futuro.

## Instalação

O normalizer já está incluído no projeto. Basta importá-lo:

```python
from services.normalizer import DataNormalizer
```

## Uso Básico

### 1. Inicialização

```python
from services.normalizer import DataNormalizer

# Criar instância do normalizador
normalizer = DataNormalizer()
```

### 2. Normalizar Lista de Veículos

```python
# Dados brutos (Wialon, já pré-processados pelo VehicleService)
raw_vehicles = [
    {"vehicle_id": 1, "nm": "Caminhão 01", "plate": "ABC-1234"},
    {"vehicle_id": 2, "nm": "Van 02", "plate": "XYZ-5678"},
]

# Normalizar
normalized_vehicles = normalizer.normalize_vehicle_list(raw_vehicles, system="wialon")
```

### 3. Normalizar Dados Históricos

```python
# Registros já transformados pelo WialonTransformer
raw_history = [
    {
        "vehicle_id": 1,
        "timestamp": "2024-01-15T14:30:00",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "speed": 60.5,
        "odometer": 15000.0,
        "ignition": True,
        "address": "Av. Paulista, 1000",
    }
]

normalized_history = normalizer.normalize_history(raw_history, system="wialon")
```

## Formato Padronizado

### Veículos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | Identificador único do veículo |
| `name` | string | Nome do veículo |
| `plate` | string | Placa do veículo |
| `system_source` | string | Sistema de origem (ex: "wialon") |
| `raw_data` | dict | Dados originais completos |

### Registros Históricos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `vehicle_id` | string | ID do veículo |
| `timestamp` | string | Data/hora no formato ISO 8601 |
| `latitude` | float | Latitude (padrão: 0.0) |
| `longitude` | float | Longitude (padrão: 0.0) |
| `speed` | float | Velocidade em km/h (padrão: 0.0) |
| `odometer` | float | Odômetro em km (padrão: 0.0) |
| `ignition` | bool | Status da ignição (padrão: False) |
| `address` | string | Endereço (padrão: "") |
| `system_source` | string | Sistema de origem |
| `raw_data` | dict | Dados originais completos |

## Adicionar Novo Sistema

Para adicionar suporte a um novo sistema de rastreamento:

```python
# Definir mapeamento de campos
system_b_mapping = {
    "vehicle_id": "deviceId",
    "vehicle_name": "deviceName",
    "plate": "licensePlate",
    "timestamp": "eventTime",
    "latitude": "location.lat",  # Suporta campos aninhados
    "longitude": "location.lng",
    "speed": "speedKmh",
    "odometer": "totalDistance",
    "ignition": "engineOn",
    "address": "locationAddress"
}

# Adicionar ao normalizador
normalizer.add_system_mapping("system_b", system_b_mapping)

# Usar normalmente
normalized = normalizer.normalize_vehicle_list(raw_data, system="system_b")
```

## Recursos Avançados

### 1. Campos Aninhados

O normalizer suporta campos aninhados usando notação de ponto:

```python
mapping = {
    "latitude": "location.coordinates.lat",
    "longitude": "location.coordinates.lng"
}
```

### 2. Normalização de Timestamps

O normalizer converte automaticamente diversos formatos de timestamp:

- **String ISO 8601**: Mantém o formato
- **Unix timestamp** (int/float): Converte para ISO 8601
- **Objeto datetime**: Converte para ISO 8601
- **Formato desconhecido**: Usa timestamp atual (com warning no log)

### 3. Valores Padrão

Campos ausentes recebem valores padrão seguros:

- Números: `0.0`
- Booleanos: `False`
- Strings: `""`

### 4. Tratamento de Erros

O normalizer registra erros no log mas continua processando:

```python
# Se um veículo falhar, os outros continuam sendo processados
normalized = normalizer.normalize_vehicle_list(raw_vehicles)
# Veículos com erro são pulados, mas os válidos são normalizados
```

## Exemplo Completo

```python
from src.services.normalizer import DataNormalizer
from src.services.vehicle_service import VehicleService

normalizer = DataNormalizer()
svc = VehicleService()

# Os dados já vêm pré-processados pelo VehicleService
vehicles_raw = svc.list_vehicles()
history_raw = svc.get_vehicle_history(vehicle_id=1, month=1, year=2026)

vehicles = normalizer.normalize_vehicle_list(vehicles_raw, system="wialon")
history = normalizer.normalize_history(history_raw, system="wialon")
```

## Verificar Sistemas Suportados

```python
systems = normalizer.get_supported_systems()
print(f"Sistemas suportados: {systems}")
# Output: ['wialon']
```

## Logs

O normalizer usa `loguru` para logging:

- **INFO**: Início e fim de normalização
- **SUCCESS**: Normalização concluída com sucesso
- **ERROR**: Erros ao normalizar registros individuais
- **WARNING**: Formatos de timestamp não reconhecidos

Todos os logs são salvos em `app.log`.

