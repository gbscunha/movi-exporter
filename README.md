# 📘 **Documentação Inicial do Projeto – Movi Exporter App (Versão Corrigida)**

## 📌 **Visão Geral**

O **Movi Exporter App** é uma aplicação Python criada para **automatizar a extração e exportação dos dados históricos mensais dos veículos** monitorados pela empresa **Movi Solutions**.

O objetivo central é permitir que a empresa extraia **os dados de cada veículo, mês a mês**, de forma automática, organizada e padronizada, eliminando completamente o processo manual atual.

O sistema se conecta a **dois provedores de rastreamento veicular**, unifica os dados e gera arquivos de exportação (CSV/Excel), com possibilidade de enviá-los automaticamente para a nuvem (Google Drive).

---

## 🎯 **Objetivos do Projeto**

### 🥇 **Objetivo principal**

**Exportar automaticamente os dados históricos dos veículos por mês**, consumindo as APIs dos dois sistemas de rastreamento e gerando arquivos organizados.

### 🥈 Objetivos secundários

1. Automatizar a coleta de dados dos provedores de rastreamento.
2. Unificar a estrutura dos dados entre diferentes sistemas.
3. Gerar arquivos estruturados para análise (CSV/Excel).
4. Armazenar os arquivos na nuvem (Google Drive).
5. Oferecer uma CLI simples para execução manual do processo.
6. Possibilitar futuramente uma interface GUI para usuários não técnicos.

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
│   │   ├── system_a_client.py    # Integração com Sistema A
│   │   ├── system_b_client.py    # Integração com Sistema B
│   │
│   ├── services/
│   │   ├── normalizer.py         # Padronização dos dados (futuro)
│   │   ├── exporter.py           # Exportação CSV/Excel (futuro)
│   │   ├── uploader.py           # Upload no Google Drive (futuro)
│   │   └── vehicle_service.py    # Fluxo principal de exportação mensal
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

O projeto se conecta a dois sistemas diferentes de rastreamento.
Cada sistema tem seus endpoints e formatos, então usamos:

* uma **classe BaseClient**, com métodos GET padronizados
* duas implementações: **SystemAClient** e **SystemBClient**

Esses clientes permitem:

* listar veículos
* coletar dados históricos
* filtrar por mês
* filtrar por ID do veículo

---

## 🔐 **Configurações via .env**

Exemplo:

```
SYSTEM_A_BASE_URL=https://api.sistema-a.com
SYSTEM_A_TOKEN=token_a

SYSTEM_B_BASE_URL=https://api.sistema-b.com
SYSTEM_B_TOKEN=token_b
```

---

## 🧠 **Fluxo Principal (Core do Projeto)**

### Para cada sistema:

1. Buscar lista de veículos.
2. Para cada veículo:

   * Buscar dados históricos **referentes a um mês específico**.
3. Padronizar resposta entre os sistemas.
4. Exportar arquivo CSV/Excel por veículo e por mês.
5. (Opcional) Enviar o arquivo para a nuvem.

Esse fluxo será implementado em `vehicle_service.py`.

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

1. Implementar endpoints reais dos dois sistemas.
2. Criar fluxo de “exportação por mês”.
3. Criar normalizador.
4. Criar exporter CSV/Excel.
5. Criar uploader Google Drive.
6. Criar CLI robusta.
7. Escrever testes.
8. Opcional: Interface GUI.

---

## 📌 **Resumo Final**

O Movi Exporter App é um sistema Python destinado a automatizar a coleta e exportação mensal dos dados dos veículos monitorados pela Movi Solutions. Ele integra dois sistemas externos, normalize dados, gera arquivos e prepara os dados para armazenamento em nuvem. A arquitetura é modular e expansível, visando manutenção fácil e evolução futura.
