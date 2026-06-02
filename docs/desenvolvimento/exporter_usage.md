# 📤 Guia de Uso do DataExporter

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Instalação e Configuração](#instalação-e-configuração)
3. [Inicialização](#inicialização)
4. [Exportação de Veículos](#exportação-de-veículos)
5. [Exportação de Histórico](#exportação-de-histórico)
6. [Exportação Consolidada](#exportação-consolidada)
7. [Estrutura de Arquivos](#estrutura-de-arquivos)
8. [Metadados](#metadados)
9. [Estatísticas](#estatísticas)
10. [Exemplos Práticos](#exemplos-práticos)
11. [Integração com Normalizer](#integração-com-normalizer)

---

## 🎯 Visão Geral

O **DataExporter** é o módulo responsável por exportar dados normalizados de veículos e histórico para arquivos CSV e Excel. Ele oferece:

- ✅ Exportação para CSV e Excel
- ✅ Organização automática por mês/ano
- ✅ Nomenclatura padronizada de arquivos
- ✅ Adição automática de metadados
- ✅ Exportação individual ou consolidada
- ✅ Estatísticas de exportação

---

## 📦 Instalação e Configuração

### Dependências Necessárias

O DataExporter requer as seguintes bibliotecas:

```bash
pip install pandas openpyxl
```

Estas dependências já estão incluídas no `requirements.txt` do projeto.

### Estrutura de Diretórios

Por padrão, o DataExporter cria a seguinte estrutura:

```
exports/
├── 2024-10/
│   ├── veiculos_10_2024.csv
│   ├── veiculos_10_2024.xlsx
│   ├── historico_VEI001_10_2024.csv
│   ├── historico_VEI002_10_2024.csv
│   └── historico_consolidado_10_2024.csv
├── 2024-11/
│   └── ...
└── 2024-12/
    └── ...
```

---

## 🚀 Inicialização

### Importação

```python
from src.services.exporter import DataExporter
```

### Criando uma Instância

```python
# Usando diretório padrão (./exports)
exporter = DataExporter()

# Especificando diretório customizado
exporter = DataExporter(base_export_dir="./meus_exports")
```

---

## 🚗 Exportação de Veículos

### Exportar Lista de Veículos para CSV

```python
vehicles = [
    {
        "id": "VEI001",
        "name": "Caminhão Mercedes 1",
        "plate": "ABC-1234",
        "system_source": "wialon",
        "raw_data": {...}
    },
    {
        "id": "VEI002",
        "name": "Van Fiat 2",
        "plate": "DEF-5678",
        "system_source": "wialon",
        "raw_data": {...}
    }
]

# Exporta com organização automática por mês/ano
csv_path = exporter.export_vehicles_to_csv(
    vehicles=vehicles,
    month=10,
    year=2024
)
# Resultado: exports/2024-10/veiculos_10_2024.csv
```

### Exportar Lista de Veículos para Excel

```python
excel_path = exporter.export_vehicles_to_excel(
    vehicles=vehicles,
    month=10,
    year=2024
)
# Resultado: exports/2024-10/veiculos_10_2024.xlsx
```

### Exportar para Caminho Customizado

```python
csv_path = exporter.export_vehicles_to_csv(
    vehicles=vehicles,
    output_path="./custom_dir/meus_veiculos.csv"
)
```

### Estrutura do CSV de Veículos

```csv
export_date,system_source,id,name,plate
2024-12-03T10:30:00,wialon,VEI001,Caminhão Mercedes 1,ABC-1234
2024-12-03T10:30:00,wialon,VEI002,Van Fiat 2,DEF-5678
```

---

## 📊 Exportação de Histórico

### Exportar Histórico de um Veículo para CSV

```python
history = [
    {
        "vehicle_id": "VEI001",
        "timestamp": "2024-10-01T08:00:00",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "speed": 45.5,
        "odometer": 15000.0,
        "ignition": True,
        "address": "Av. Paulista, 1000",
        "system_source": "wialon",
        "raw_data": {...}
    },
    # ... mais registros
]

csv_path = exporter.export_history_to_csv(
    history=history,
    vehicle_id="VEI001",
    month=10,
    year=2024
)
# Resultado: exports/2024-10/historico_VEI001_10_2024.csv
```

### Exportar Histórico de um Veículo para Excel

```python
excel_path = exporter.export_history_to_excel(
    history=history,
    vehicle_id="VEI001",
    month=10,
    year=2024
)
# Resultado: exports/2024-10/historico_VEI001_10_2024.xlsx
```

### Estrutura do CSV de Histórico

```csv
export_date,system_source,vehicle_id,timestamp,latitude,longitude,speed,odometer,ignition,address
2024-12-03T10:30:00,wialon,VEI001,2024-10-01T08:00:00,-23.5505,-46.6333,45.5,15000.0,True,Av. Paulista 1000
2024-12-03T10:30:00,wialon,VEI001,2024-10-01T09:00:00,-23.5489,-46.6388,60.0,15050.0,True,Av. Faria Lima 500
```

---

## 📦 Exportação Consolidada

A exportação consolidada permite combinar o histórico de múltiplos veículos em um único arquivo.

### Exportar Histórico Consolidado para CSV

```python
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
            "system_source": "wialon",
            "raw_data": {}
        },
        # ... mais registros do VEI001
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
            "system_source": "wialon",
            "raw_data": {}
        },
        # ... mais registros do VEI002
    ]
}

csv_path = exporter.export_consolidated_history_to_csv(
    all_history=all_history,
    month=10,
    year=2024
)
# Resultado: exports/2024-10/historico_consolidado_10_2024.csv
```

### Exportar Histórico Consolidado para Excel

```python
excel_path = exporter.export_consolidated_history_to_excel(
    all_history=all_history,
    month=10,
    year=2024
)
# Resultado: exports/2024-10/historico_consolidado_10_2024.xlsx
```

### Características da Exportação Consolidada

- ✅ Combina dados de todos os veículos em um único arquivo
- ✅ Ordena automaticamente por `vehicle_id` e `timestamp`
- ✅ Mantém metadados consistentes
- ✅ Ideal para análises agregadas

---

## 📁 Estrutura de Arquivos

### Padrão de Nomenclatura

O DataExporter segue um padrão consistente de nomenclatura:

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Veículos | `veiculos_{mes}_{ano}.{ext}` | `veiculos_10_2024.csv` |
| Histórico Individual | `historico_{vehicle_id}_{mes}_{ano}.{ext}` | `historico_VEI001_10_2024.csv` |
| Histórico Consolidado | `historico_consolidado_{mes}_{ano}.{ext}` | `historico_consolidado_10_2024.csv` |

### Organização por Pastas

```
exports/
├── 2024-10/          # Outubro de 2024
├── 2024-11/          # Novembro de 2024
└── 2024-12/          # Dezembro de 2024
```

---

## 🏷️ Metadados

Todos os arquivos exportados incluem metadados automáticos:

### Campos de Metadados

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `export_date` | Data/hora da exportação | `2024-12-03T10:30:00` |
| `system_source` | Sistema de origem dos dados | `wialon` |

### Exemplo de CSV com Metadados

```csv
export_date,system_source,vehicle_id,timestamp,latitude,longitude,speed
2024-12-03T10:30:00,wialon,VEI001,2024-10-01T08:00:00,-23.5505,-46.6333,45.5
```

Os metadados são adicionados como **primeiras colunas** do arquivo, facilitando rastreabilidade e auditoria.

---

## 📈 Estatísticas

### Obter Estatísticas de Exportação

```python
stats = exporter.get_export_stats(month=10, year=2024)

print(stats)
# {
#     "month": 10,
#     "year": 2024,
#     "directory": "./exports/2024-10",
#     "exists": True,
#     "total_files": 8,
#     "csv_files": 4,
#     "excel_files": 4,
#     "total_size_mb": 2.45
# }
```

### Campos Retornados

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `month` | int | Mês consultado |
| `year` | int | Ano consultado |
| `directory` | str | Caminho do diretório |
| `exists` | bool | Se o diretório existe |
| `total_files` | int | Total de arquivos |
| `csv_files` | int | Arquivos CSV |
| `excel_files` | int | Arquivos Excel |
| `total_size_mb` | float | Tamanho total em MB |

---

## 💡 Exemplos Práticos

### Exemplo 1: Exportação Simples

```python
from src.services.exporter import DataExporter

# Dados normalizados
vehicles = [
    {"id": "VEI001", "name": "Caminhão 1", "plate": "ABC-1234", "system_source": "wialon", "raw_data": {}}
]

# Exporta
exporter = DataExporter()
csv_path = exporter.export_vehicles_to_csv(vehicles, month=10, year=2024)

print(f"Arquivo criado: {csv_path}")
```

### Exemplo 2: Exportação de Múltiplos Veículos

```python
from src.services.exporter import DataExporter

exporter = DataExporter()

# Para cada veículo, exporta seu histórico
for vehicle_id in ["VEI001", "VEI002", "VEI003"]:
    history = get_vehicle_history(vehicle_id, month=10, year=2024)  # função fictícia
    
    exporter.export_history_to_csv(
        history=history,
        vehicle_id=vehicle_id,
        month=10,
        year=2024
    )
```

### Exemplo 3: Exportação com Tratamento de Erros

```python
from src.services.exporter import DataExporter
from src.core.logger import logger

exporter = DataExporter()

try:
    csv_path = exporter.export_vehicles_to_csv(vehicles, month=10, year=2024)
    logger.success(f"Exportação bem-sucedida: {csv_path}")
except Exception as e:
    logger.error(f"Erro na exportação: {e}")
```

### Exemplo 4: Exportação Dupla (CSV + Excel)

```python
from src.services.exporter import DataExporter

exporter = DataExporter()

# Exporta para ambos os formatos
csv_path = exporter.export_history_to_csv(history, "VEI001", 10, 2024)
excel_path = exporter.export_history_to_excel(history, "VEI001", 10, 2024)

print(f"CSV: {csv_path}")
print(f"Excel: {excel_path}")
```

---

## 🔗 Integração com Normalizer

O DataExporter foi projetado para trabalhar perfeitamente com o DataNormalizer.

### Fluxo Completo: Normalizar → Exportar

```python
from src.services.normalizer import DataNormalizer
from src.services.exporter import DataExporter

# 1. Dados brutos da API
raw_vehicles = [
    {"veiculoId": "VEI001", "nome": "Caminhão 1", "placa": "ABC-1234"}
]

raw_history = [
    {
        "veiculoId": "VEI001",
        "dataHora": "2024-10-01T08:00:00",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "velocidade": 45.5,
        "odometro": 15000.0,
        "ignicao": True,
        "endereco": "Av. Paulista, 1000"
    }
]

# 2. Normaliza
normalizer = DataNormalizer()
normalized_vehicles = normalizer.normalize_vehicle_list(raw_vehicles)
normalized_history = normalizer.normalize_history(raw_history)

# 3. Exporta
exporter = DataExporter()
vehicles_csv = exporter.export_vehicles_to_csv(normalized_vehicles, month=10, year=2024)
history_csv = exporter.export_history_to_csv(normalized_history, "VEI001", 10, 2024)

print(f"Veículos: {vehicles_csv}")
print(f"Histórico: {history_csv}")
```

### Vantagens da Integração

- ✅ **Dados padronizados**: O normalizer garante formato consistente
- ✅ **Metadados preservados**: Campo `system_source` é mantido
- ✅ **Rastreabilidade**: Campo `raw_data` permite auditoria
- ✅ **Flexibilidade**: Suporta múltiplos sistemas de origem

---

## 🎯 Casos de Uso

### Caso 1: Exportação Mensal Completa

```python
def export_monthly_data(month: int, year: int):
    """Exporta todos os dados de um mês."""
    normalizer = DataNormalizer()
    exporter = DataExporter()
    
    # Busca e normaliza veículos
    raw_vehicles = api_client.listar_veiculos()
    vehicles = normalizer.normalize_vehicle_list(raw_vehicles)
    
    # Exporta lista de veículos
    exporter.export_vehicles_to_csv(vehicles, month, year)
    
    # Para cada veículo, exporta histórico
    all_history = {}
    for vehicle in vehicles:
        raw_history = api_client.buscar_historico(vehicle['id'], f"{month:02d}_{year}")
        history = normalizer.normalize_history(raw_history)
        
        # Exporta individual
        exporter.export_history_to_csv(history, vehicle['id'], month, year)
        
        # Guarda para consolidado
        all_history[vehicle['id']] = history
    
    # Exporta consolidado
    exporter.export_consolidated_history_to_csv(all_history, month, year)
```

### Caso 2: Exportação com Múltiplos Formatos

```python
def export_in_all_formats(data, vehicle_id, month, year):
    """Exporta dados em CSV e Excel."""
    exporter = DataExporter()
    
    paths = {
        'csv': exporter.export_history_to_csv(data, vehicle_id, month, year),
        'excel': exporter.export_history_to_excel(data, vehicle_id, month, year)
    }
    
    return paths
```

---

## 🔧 Configurações Avançadas

### Customizar Diretório Base

```python
# Via construtor
exporter = DataExporter(base_export_dir="/mnt/storage/exports")

# Via variável de ambiente (futuro)
# EXPORT_DIR=/mnt/storage/exports
```

### Nomenclatura Customizada

Para nomenclatura totalmente customizada, use o parâmetro `output_path`:

```python
custom_path = f"./custom_exports/dados_veiculo_{vehicle_id}_{datetime.now().strftime('%Y%m%d')}.csv"
exporter.export_history_to_csv(history, vehicle_id, month, year, output_path=custom_path)
```

---

## ✅ Boas Práticas

1. **Use organização por mês/ano**: Facilita localização de arquivos
2. **Exporte em ambos os formatos**: CSV para processamento, Excel para visualização
3. **Verifique estatísticas**: Use `get_export_stats()` para monitorar exportações
4. **Trate erros**: Sempre use try/except em produções
5. **Preserve raw_data**: Útil para debugging e auditoria
6. **Use logs**: O módulo já loga automaticamente operações importantes

---

## 🐛 Troubleshooting

### Problema: "Lista vazia, nenhum arquivo será criado"

**Causa**: A lista de dados está vazia.

**Solução**: Verifique se os dados foram normalizados corretamente antes de exportar.

### Problema: "Erro ao exportar para Excel"

**Causa**: Biblioteca `openpyxl` não instalada.

**Solução**:
```bash
pip install openpyxl
```

### Problema: "Permission denied"

**Causa**: Sem permissão para escrever no diretório.

**Solução**: Verifique permissões ou use outro diretório:
```python
exporter = DataExporter(base_export_dir="./exports")
```

---

## 📚 Referências

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [OpenPyXL Documentation](https://openpyxl.readthedocs.io/)
- [DataNormalizer Usage Guide](../normalizer/normalizer_usage.md)

---

## 🎉 Conclusão

O **DataExporter** fornece uma solução completa e robusta para exportação de dados de veículos e histórico. Com suporte a múltiplos formatos, organização automática e integração perfeita com o DataNormalizer, ele simplifica significativamente o processo de exportação de dados do sistema de rastreamento.

Para testar o módulo, execute:

```bash
source venv/bin/activate
python examples/test_exporter.py
```

