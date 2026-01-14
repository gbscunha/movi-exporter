# 📘 **Documentação Inicial do Projeto – Movi Exporter App**

## 📌 **Visão Geral**

O **Movi Exporter App** é uma aplicação Python criada para **automatizar a extração e exportação dos dados históricos mensais dos veículos** monitorados pela empresa **Movi Solutions**.

O objetivo central é permitir que a empresa extraia **os dados de cada veículo, mês a mês**, de forma automática, organizada e padronizada, eliminando completamente o processo manual atual.

O sistema se conecta a um **provedor de rastreamento veicular** (atualmente System A), normaliza os dados e gera arquivos de exportação (CSV/Excel), com possibilidade de enviá-los automaticamente para a nuvem (Google Drive).

**Nota:** A arquitetura está preparada para suportar múltiplos sistemas de rastreamento no futuro, caso necessário.

---

## 🎯 **Objetivos do Projeto**

### 🥇 **Objetivo principal**

**Exportar automaticamente os dados históricos dos veículos por mês**, consumindo as APIs dos dois sistemas de rastreamento e gerando arquivos organizados.

### 🥈 Objetivos secundários

1. Automatizar a coleta de dados do provedor de rastreamento (System A).
2. Normalizar a estrutura dos dados para formato padronizado.
3. Gerar arquivos estruturados para análise (CSV/Excel).
4. Armazenar os arquivos na nuvem (Google Drive).
5. Oferecer uma CLI simples para execução manual do processo.
6. Possibilitar futuramente uma interface GUI para usuários não técnicos.
7. Manter arquitetura extensível para adicionar novos sistemas no futuro.

---

## 🧩 **Arquitetura do Projeto (Python 3.14)**

O projeto usa uma arquitetura modular, organizada e expansível, com ambiente virtual Python 3.14.

### 📁 Estrutura Atual

```
movi_exporter_app/
│
├── venv/                         # Ambiente virtual Python 3.14
├── src/
│   ├── core/
│   │   ├── config.py             # Carrega variáveis do .env
│   │   ├── logger.py             # Configuração de logs
│   │
│   ├── clients/
│   │   ├── base_client.py        # Base para consumo de APIs
│   │   ├── system_a_client.py    # Integração com Sistema A (atual)
│   │
│   ├── services/
│   │   ├── normalizer.py         # ✅ Padronização dos dados
│   │   ├── exporter.py           # Exportação CSV/Excel (futuro)
│   │   ├── uploader.py           # Upload no Google Drive (futuro)
│   │   └── vehicle_service.py    # Fluxo principal de exportação mensal (futuro)
│   │
│   └── cli/
│       └── main.py               # Entrada da automação via CLI
│
├── tests/                        # Testes unitários (futuro)
├── .env                          # Tokens e URLs das APIs
├── requirements.txt
└── README.md
```

---

## 🔌 **Integração com APIs**

O projeto se conecta ao **System A** para rastreamento de veículos.
A arquitetura utiliza:

* uma **classe BaseClient**, com métodos GET padronizados e autenticação Bearer Token
* implementação **SystemAClient** para o sistema atual

O cliente permite:

* listar veículos
* coletar dados históricos
* filtrar por mês
* filtrar por ID do veículo

**Extensibilidade:** A arquitetura permite adicionar facilmente novos sistemas (SystemBClient, SystemCClient, etc.) no futuro, bastando herdar de `BaseClient` e implementar os métodos específicos.

---

## 🔐 **Configurações via .env**

Exemplo:

```
SYSTEM_A_BASE_URL=https://api.sistema-a.com
SYSTEM_A_TOKEN=token_a
```

**Nota:** Caso novos sistemas sejam adicionados no futuro, basta incluir novas variáveis (SYSTEM_B_BASE_URL, SYSTEM_B_TOKEN, etc.)

---

## 🧠 **Fluxo Principal (Core do Projeto)**

### Fluxo de exportação mensal:

1. Buscar lista de veículos do System A.
2. Para cada veículo:
   * Buscar dados históricos **referentes a um mês específico**.
   * Normalizar os dados para formato padronizado.
3. Exportar arquivo CSV/Excel por veículo e por mês.
4. (Opcional) Enviar o arquivo para a nuvem.

Esse fluxo será implementado em `vehicle_service.py`.

### 🔄 **Normalização de Dados**

O módulo `normalizer.py` é responsável por:

* **Converter dados do formato específico do sistema** para um formato padronizado universal
* **Suportar múltiplos sistemas** através de mapeamentos configuráveis
* **Manter dados originais** (campo `raw_data`) para referência e auditoria
* **Normalizar timestamps** para formato ISO 8601
* **Tratar campos ausentes** com valores padrão seguros

**Formato Padronizado de Veículos:**
```python
{
    "id": "ABC123",
    "name": "Veículo 01",
    "plate": "ABC-1234",
    "system_source": "system_a",
    "raw_data": {...}  # Dados originais
}
```

**Formato Padronizado de Histórico:**
```python
{
    "vehicle_id": "ABC123",
    "timestamp": "2024-01-15T14:30:00",
    "latitude": -23.5505,
    "longitude": -46.6333,
    "speed": 60.5,
    "odometer": 15000.0,
    "ignition": True,
    "address": "Av. Paulista, 1000",
    "system_source": "system_a",
    "raw_data": {...}  # Dados originais
}
```

---

## 🗂️ **Dependências atuais instaladas**

```
requests
python-dotenv
loguru
```

(Demais dependências serão instaladas conforme implementação avança.)

---

## 🧱 **Próximos passos**

1. ✅ ~~Criar normalizador de dados~~
2. Validar endpoints reais do System A
3. Criar fluxo de "exportação por mês" (`vehicle_service.py`)
4. Criar exporter CSV/Excel
5. Criar uploader Google Drive
6. Criar CLI robusta com argumentos
7. Escrever testes unitários
8. Opcional: Interface GUI

---

## 📌 **Resumo Final**

O Movi Exporter App é um sistema Python destinado a automatizar a coleta e exportação mensal dos dados dos veículos monitorados pela Movi Solutions. Ele integra o System A, normaliza dados para formato padronizado, gera arquivos e prepara os dados para armazenamento em nuvem. A arquitetura é modular e expansível, preparada para adicionar novos sistemas de rastreamento no futuro, visando manutenção fácil e evolução contínua.
