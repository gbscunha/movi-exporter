# Movi Exporter App - Guia do Usuário

Guia completo para utilização do Movi Exporter App, uma ferramenta de automação para extração e exportação de dados de rastreamento veicular.

> **Nota:** este é o guia **técnico / CLI** (para desenvolvedores). O manual do **usuário final** é o `docs/manual/manual.html`, aberto pelo botão **Manual** dentro do app.

---

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Requisitos](#2-requisitos)
3. [Instalação](#3-instalação)
4. [Configuração](#4-configuração)
5. [Comandos CLI](#5-comandos-cli)
6. [Dados Extraídos](#6-dados-extraídos)
7. [Estrutura de Arquivos Exportados](#7-estrutura-de-arquivos-exportados)
8. [Exemplos de Uso](#8-exemplos-de-uso)
9. [Solução de Problemas](#9-solução-de-problemas)
10. [Arquitetura](#10-arquitetura)
11. [API Wialon](#11-api-wialon)
12. [Extensibilidade](#12-extensibilidade)

---

## 1. Visão Geral

O **Movi Exporter App** é uma ferramenta de linha de comando (CLI) desenvolvida para automatizar a extração de dados históricos de veículos do sistema de rastreamento Wialon, utilizado pela Movi Solutions.

### Funcionalidades Principais

- ✅ Autenticação automática com a API Wialon
- ✅ Listagem de veículos com placa, marca e modelo
- ✅ Extração de histórico mensal com paginação
- ✅ Normalização de dados para formato padronizado
- ✅ Exportação para CSV e Excel
- ✅ Arquivo consolidado com todos os veículos
- ✅ Suporte a múltiplos sistemas (extensível)

### Dados Coletados

| Dado | Fonte | Status |
|------|-------|--------|
| Placa | Profile Fields | ✅ |
| Hora | Mensagens | ✅ |
| Velocidade | Mensagens | ✅ |
| Coordenadas (Lat/Lng) | Mensagens | ✅ |
| Ignição | Sensores/Parâmetros | ✅ |
| Nível de Combustível | Sensores/Parâmetros | ✅ |
| RPM do Motor | Sensores/Parâmetros | ✅ |
| Voltagem da Bateria | Sensores/Parâmetros | ✅ |
| Horas do Motor | Sensores/Parâmetros | ✅ |
| Motorista | Cartão RFID + Motoristas | ✅ |
| Localização (Endereço) | Geocodificação | ✅ (opt-in) |

> **Coluna Motorista:** o nome vem do cartão RFID lido pelo veículo, casado com
> a lista de **Motoristas** do Wialon (campo "Código" de cada cartão). Requisitos:
> o token precisa ter permissão de **ver motoristas** e cada cartão precisa estar
> com o **Código preenchido**. Linhas sem cartão lido saem como `N/D`.

> **Coluna Localização:** o endereço completo (rua, número, bairro, cidade, UF,
> CEP) é obtido por geocodificação das coordenadas. É **opcional** — marque
> **"Incluir endereço (mais lento)"** na tela Exportar para ativar; deixa o
> export um pouco mais demorado por causa das consultas. Pontos sem endereço
> mapeado saem como `N/D`.

---

## 2. Requisitos

### Sistema

- Python 3.10 ou superior (testado com Python 3.14)
- Sistema operacional: Windows, macOS ou Linux
- Conexão com a internet

### Credenciais

- Token de acesso à API Wialon (72 caracteres)
- Permissões de leitura para veículos e mensagens

---

## 3. Instalação

### 3.1 Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd movi_exporter_app
```

### 3.2 Criar Ambiente Virtual

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3.3 Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3.4 Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com suas credenciais
nano .env  # ou use seu editor preferido
```

---

## 4. Configuração

### 4.1 Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# ============================================
# WIALON (Obrigatório)
# ============================================
WIALON_TOKEN=seu_token_de_72_caracteres_aqui

# ============================================
# CONFIGURAÇÕES DE EXPORTAÇÃO (Opcional)
# ============================================
EXPORT_DIR=./exports
WIALON_PAGE_SIZE=1000
```

### 4.2 Variáveis Disponíveis

| Variável | Obrigatório | Padrão | Descrição |
|----------|-------------|--------|-----------|
| `WIALON_TOKEN` | ✅ Sim | - | Token de acesso à API Wialon |
| `EXPORT_DIR` | Não | `./exports` | Diretório para arquivos exportados |
| `WIALON_PAGE_SIZE` | Não | `1000` | Registros por página (500-2000) |

### 4.3 Obter Token Wialon

O token é gerado pelo fluxo de autorização web do Wialon: acesse a página de login, autentique-se e **o token volta na URL** (após `access_token=`). Copie esse valor e cole em `WIALON_TOKEN` no `.env` (ou use o botão **Gerar** na tela de Configurações do app). Passo a passo detalhado no manual do usuário (`docs/manual/manual.html`, seção 2).

---

## 5. Comandos CLI

### 5.1 Sintaxe Geral

```bash
python -m src.cli.main <comando> [opções]
```

### 5.2 Comandos Disponíveis

#### `test` - Testar Conexão

Verifica se a conexão com a API Wialon está funcionando.

```bash
python -m src.cli.main test
```

**Saída esperada:**
```
✅ Conexão com Wialon estabelecida com sucesso!
```

---

#### `list` - Listar Veículos

Lista todos os veículos disponíveis com ID, nome, placa, marca e modelo.

```bash
python -m src.cli.main list
```

**Saída esperada:**
```
┌────────────┬─────────────────────┬──────────┬───────────────┬─────────┐
│ ID         │ Nome                │ Placa    │ Marca         │ Modelo  │
├────────────┼─────────────────────┼──────────┼───────────────┼─────────┤
│ 401988378  │ AMY4G08_TSL_CEG     │ AMY4G08  │ MERCEDES-BENZ │ 915 C   │
│ 401988379  │ ABC1234_TSL_CEG     │ ABC1234  │ VOLKSWAGEN    │ 24.280  │
└────────────┴─────────────────────┴──────────┴───────────────┴─────────┘
```

---

#### `export` - Exportar Dados

Exporta dados históricos de veículos para CSV ou Excel.

```bash
python -m src.cli.main export [opções]
```

**Opções:**

| Opção | Curto | Tipo | Padrão | Descrição |
|-------|-------|------|--------|-----------|
| `--month` | `-m` | int | Mês anterior | Mês a exportar (1-12) |
| `--year` | `-y` | int | Ano atual | Ano a exportar |
| `--vehicles` | `-v` | string | Todos | IDs separados por vírgula |
| `--format` | `-f` | string | `csv` | Formato: `csv`, `xlsx` ou `both` |
| `--no-consolidated` | - | flag | False | Não gerar arquivo consolidado |
| `--output` | `-o` | string | `./exports` | Diretório de saída |
| `--upload` | `-u` | flag | False | Enviar os arquivos para o Google Drive |
| `--addresses` | `-A` | flag | False | Geocodificar e preencher a coluna Localização |
| `--account` | `-a` | int | `1` | Conta Wialon a usar (1 ou 2) |

**Exemplos:**

```bash
# Exportar mês anterior (padrão)
python -m src.cli.main export

# Exportar dezembro de 2024
python -m src.cli.main export --month 12 --year 2024

# Exportar veículos específicos
python -m src.cli.main export -m 12 -y 2024 -v 401988378,401988379

# Exportar em Excel
python -m src.cli.main export -m 12 -y 2024 -f xlsx

# Exportar em ambos formatos
python -m src.cli.main export -m 12 -y 2024 -f both

# Sem arquivo consolidado
python -m src.cli.main export -m 12 -y 2024 --no-consolidated

# Diretório customizado
python -m src.cli.main export -m 12 -y 2024 -o /caminho/personalizado
```

---

## 6. Dados Extraídos

### 6.1 Dados do Veículo

Obtidos via `list`:

| Campo | Descrição | Fonte |
|-------|-----------|-------|
| `id` | ID único do veículo no Wialon | API |
| `name` | Nome do veículo | `nm` |
| `plate` | Placa do veículo | `pflds.registration_plate` |
| `brand` | Marca do veículo | `pflds.brand` |
| `model` | Modelo do veículo | `pflds.model` |

### 6.2 Dados Históricos

Obtidos via `export`:

| Campo | Descrição | Tipo | Fonte |
|-------|-----------|------|-------|
| `vehicle_id` | ID do veículo | int | Mensagem |
| `timestamp` | Data/hora (ISO 8601) | string | `message.t` |
| `latitude` | Latitude | float | `pos.y` |
| `longitude` | Longitude | float | `pos.x` |
| `speed` | Velocidade (km/h) | float | `pos.s` |
| `ignition` | Ignição ligada/desligada | bool | Sensor ou `in1` |
| `fuel_level` | Nível de combustível | float | Sensor ou `fuel1` |
| `rpm` | Rotação do motor | int | Sensor ou `can_rpm` |
| `battery_voltage` | Voltagem da bateria (V) | float | Sensor ou `pwr_ext` |
| `engine_hours` | Horas do motor | float | Sensor |
| `driver` | Motorista (nome do cartão RFID) | string | `rfid_tag` + lista de motoristas |
| `odometer` | Hodômetro (km) | float | `params.odometer` (metros → km) |
| `address` | Endereço completo | string | Geocodificação (`gis_geocode`, opt-in) |

### 6.3 Parâmetros Buscados Automaticamente

O sistema busca dados de duas formas:

1. **Via Sensores Configurados** - Mapeamento do Wialon
2. **Via Parâmetros Diretos** - Busca automática nas mensagens

| Campo | Parâmetros Buscados |
|-------|---------------------|
| Ignição | `in`, `in1`, `din1`, `ignition`, `ign` |
| Combustível | `fuel1`, `fuel2`, `fuel_level`, `can_fuel_level`, `fuel`, `fls` |
| RPM | `rpm`, `can_rpm`, `engine_rpm`, `eng_rpm` |
| Voltagem | `pwr_ext`, `pwr_int`, `voltage`, `battery`, `power`, `batt` |
| Horas Motor | `engine_hours`, `eng_hours`, `horimeter`, `eh`, `mh` |

---

## 7. Estrutura de Arquivos Exportados

### 7.1 Organização de Diretórios

```
exports/
├── 2024-12/
│   ├── historico_401988378_12_2024.csv
│   ├── historico_401988378_12_2024.xlsx
│   ├── historico_401988379_12_2024.csv
│   ├── historico_401988379_12_2024.xlsx
│   ├── historico_consolidado_12_2024.csv
│   └── historico_consolidado_12_2024.xlsx
├── 2025-01/
│   └── ...
└── ...
```

### 7.2 Nomenclatura dos Arquivos

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Individual | `historico_{id}_{mes}_{ano}.{ext}` | `historico_401988378_12_2024.csv` |
| Consolidado | `historico_consolidado_{mes}_{ano}.{ext}` | `historico_consolidado_12_2024.csv` |
| Veículos | `veiculos_{mes}_{ano}.{ext}` | `veiculos_12_2024.csv` |

### 7.3 Estrutura do CSV/Excel

**Colunas exportadas:**

```csv
export_date,system_source,vehicle_id,timestamp,latitude,longitude,speed,odometer,ignition,address,fuel_level,rpm,battery_voltage,engine_hours,driver
```

**Exemplo de dados:**

```csv
2025-01-16T10:30:00,wialon,401988378,2024-12-15T14:30:00,-23.5505,-46.6333,60.5,0.0,True,,45.5,2500,12.4,1500.5,João Silva
```

---

## 8. Exemplos de Uso

### 8.1 Fluxo Básico

```bash
# 1. Ativar ambiente virtual
source venv/bin/activate

# 2. Testar conexão
python -m src.cli.main test

# 3. Listar veículos disponíveis
python -m src.cli.main list

# 4. Exportar dados do mês anterior
python -m src.cli.main export
```

### 8.2 Exportação Mensal Automatizada

```bash
# Exportar janeiro/2025 em CSV e Excel
python -m src.cli.main export -m 1 -y 2025 -f both
```

### 8.3 Exportação de Veículos Específicos

```bash
# Obter IDs dos veículos
python -m src.cli.main list

# Exportar apenas veículos específicos
python -m src.cli.main export -m 12 -y 2024 -v 401988378,401988379
```

### 8.4 Script de Automação (Cron)

Criar arquivo `export_monthly.sh`:

```bash
#!/bin/bash
cd /caminho/para/movi_exporter_app
source venv/bin/activate
python -m src.cli.main export -f both
```

Agendar no cron (todo dia 1º às 6h):

```bash
0 6 1 * * /caminho/para/export_monthly.sh >> /var/log/movi_export.log 2>&1
```

---

## 9. Solução de Problemas

### 9.1 Erros Comuns

#### Token Inválido

```
WialonAuthError: Falha na autenticação: error=8
```

**Solução:** Verifique se o token no `.env` está correto e tem 72 caracteres.

---

#### Sessão Expirada

```
WialonAuthError: Sessão expirada e máximo de retentativas excedido
```

**Solução:** O sistema tenta reautenticar automaticamente. Se persistir, verifique sua conexão.

---

#### Sem Dados no Período

```
Veículo XYZ: nenhum registro no período
```

**Causa:** O veículo não tem dados históricos no mês selecionado.

**Solução:** Verifique se o veículo estava ativo no período.

---

#### Campos Vazios na Exportação

```
fuel_level, rpm, battery_voltage = None
```

**Causas possíveis:**
1. Rastreador não envia esses dados
2. Sensores não configurados no Wialon
3. Parâmetros com nomes diferentes

**Solução:** Verifique os parâmetros das mensagens no Wialon.

---

### 9.2 Logs

Os logs são salvos em `app.log` com rotação de 1MB.

```bash
# Ver logs em tempo real
tail -f app.log

# Buscar erros
grep "ERROR" app.log
```

### 9.3 Debug

Para mais detalhes, verifique os dados brutos no campo `raw_data` dos arquivos exportados.

---

## 10. Arquitetura

### 10.1 Estrutura do Projeto

```
movi_exporter_app/
├── src/
│   ├── cli/
│   │   └── main.py              # Interface de linha de comando
│   ├── clients/
│   │   └── wialon_client.py     # Cliente da API Wialon
│   ├── core/
│   │   ├── config.py            # Configurações do ambiente
│   │   └── logger.py            # Configuração de logs
│   └── services/
│       ├── exporter.py          # Exportação CSV/Excel
│       ├── normalizer.py        # Normalização de dados
│       └── vehicle_service.py   # Orquestração principal
├── docs/                        # Documentação
├── tests/                       # Testes unitários
├── exports/                     # Arquivos exportados
├── .env                         # Variáveis de ambiente
├── .env.example                 # Exemplo de configuração
├── requirements.txt             # Dependências Python
└── README.md                    # Documentação principal
```

### 10.2 Fluxo de Dados

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Wialon API │────▶│ WialonClient │────▶│VehicleService│
└─────────────┘     └──────────────┘     └──────────────┘
                                                │
                    ┌──────────────┐            │
                    │   Exporter   │◀───────────┤
                    └──────────────┘            │
                           │            ┌──────────────┐
                           │            │  Normalizer  │
                    ┌──────▼──────┐     └──────────────┘
                    │  CSV/Excel  │
                    └─────────────┘
```

### 10.3 Responsabilidades

| Componente | Responsabilidade |
|------------|------------------|
| `WialonClient` | Comunicação com API Wialon |
| `VehicleService` | Orquestração do fluxo completo |
| `DataNormalizer` | Padronização de dados |
| `DataExporter` | Geração de arquivos CSV/Excel |

---

## 11. API Wialon

### 11.1 Endpoints Utilizados

| Endpoint | Descrição |
|----------|-----------|
| `token/login` | Autenticação via token |
| `core/search_items` | Listagem de veículos |
| `core/search_item` | Detalhes de um veículo |
| `messages/load_interval` | Histórico de mensagens |
| `core/logout` | Encerramento de sessão |

### 11.2 Flags Utilizadas

| Flag | Valor | Descrição |
|------|-------|-----------|
| Geral | 1 | Propriedades básicas |
| Custom Fields | 8 | Campos customizados |
| Sensores | 4096 | Configuração de sensores |
| Profile Fields | 8388608 | Placa, marca, modelo |
| **Total** | **8392713** | Todas as informações |

### 11.3 Documentação Completa

Consulte `docs/wialon_api_documentation/wialon_api_reference.md` para referência completa da API.

---

## 12. Extensibilidade

### 12.1 Adicionar Novo Sistema

O projeto suporta múltiplos sistemas de rastreamento via mapeamentos no normalizer:

```python
# Em normalizer.py
normalizer.add_system_mapping("novo_sistema", {
    "vehicle_id": "deviceId",
    "vehicle_name": "deviceName",
    "plate": "licensePlate",
    "timestamp": "dateTime",
    "latitude": "lat",
    "longitude": "lng",
    "speed": "velocity",
    # ... outros campos
})
```

### 12.2 Adicionar Novos Parâmetros

Para buscar novos parâmetros automaticamente, edite `KNOWN_PARAMS` em `vehicle_service.py`:

```python
KNOWN_PARAMS = {
    # ... existentes
    "novo_campo": ["param1", "param2", "param3"],
}
```

### 12.3 Funcionalidades Planejadas

- [x] Geocodificação reversa (endereços)
- [x] Upload para Google Drive
- [ ] Interface web
- [ ] Notificações por email
- [ ] Relatórios PDF

---

## Suporte

Para dúvidas ou problemas:

1. Verifique a seção [Solução de Problemas](#9-solução-de-problemas)
2. Consulte os logs em `app.log`
3. Abra uma issue no repositório

---

*Guia técnico (dev/CLI) — atualizado para o app v1.5.0.*
