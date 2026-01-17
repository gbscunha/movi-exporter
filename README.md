# 📘 **Movi Exporter App**

## 📌 **Visão Geral**

O **Movi Exporter App** é uma aplicação Python criada para **automatizar a extração e exportação dos dados históricos mensais dos veículos** monitorados pela empresa **Movi Solutions**.

O sistema se conecta à **API Wialon Hosting**, extrai dados de telemetria (posição, velocidade, sensores), normaliza e exporta em formatos padronizados (CSV/Excel).

**Status:** ✅ **Implementação completa** - Cliente Wialon, normalização, exportação e CLI funcionais.

---

## 🚀 **Início Rápido**

### Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd movi_exporter_app

# Crie e ative o ambiente virtual
python3.14 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou: venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env e adicione seu WIALON_TOKEN
```

### Uso Básico

```bash
# Iniciar a interface gráfica
python -m src.gui.main

# Ou via CLI:

# Testar conexão com Wialon
python -m src.cli.main test

# Listar veículos disponíveis
python -m src.cli.main list

# Exportar dados do mês anterior (padrão)
python -m src.cli.main export

# Exportar mês específico
python -m src.cli.main export --month 12 --year 2025

# Exportar veículos específicos
python -m src.cli.main export --month 12 --year 2025 --vehicles 123,456

# Exportar em Excel
python -m src.cli.main export --format xlsx

# Exportar em ambos os formatos
python -m src.cli.main export --format both

# Exportar e fazer upload para Google Drive
python -m src.cli.main export --format xlsx --upload

# Testar conexão com Google Drive
python -m src.cli.main test-drive
```

---

## 🧩 **Arquitetura do Projeto**

```
movi_exporter_app/
├── src/
│   ├── core/
│   │   ├── config.py             # Configurações (carrega .env)
│   │   └── logger.py             # Logging com loguru
│   │
│   ├── clients/
│   │   ├── base_client.py        # Classes base (REST e Stateful)
│   │   ├── wialon_client.py      # ✅ Cliente Wialon completo
│   │   └── system_a_client.py    # Cliente legado (exemplo)
│   │
│   ├── services/
│   │   ├── normalizer.py         # ✅ Normalização de dados
│   │   ├── exporter.py           # ✅ Exportação CSV/Excel
│   │   ├── vehicle_service.py    # ✅ Orquestração principal
│   │   └── uploader.py           # ✅ Upload Google Drive
│   │
│   └── cli/
│       └── main.py               # ✅ Interface de linha de comando
│
├── exports/                      # Arquivos exportados (por mês/ano)
├── .env                          # Variáveis de ambiente (não versionado)
├── .env.example                  # Exemplo de configuração
├── requirements.txt              # Dependências
└── README.md
```

---

## 🔌 **Integração com Wialon**

O cliente Wialon (`WialonClient`) implementa:

-   **Autenticação stateful** via sessão (`sid`), não Bearer Token
-   **Reautenticação automática** quando a sessão expira
-   **Listagem de veículos** via `core/search_items`
-   **Resolução de sensores** via `core/search_item` (com cache)
-   **Busca paginada de histórico** via `messages/load_interval`
-   **Tratamento de erros** específicos da API (error=1, error=4)

### Dados Extraídos

| Campo           | Origem Wialon        |
| --------------- | -------------------- |
| timestamp       | `t` (Unix timestamp) |
| latitude        | `pos.y`              |
| longitude       | `pos.x`              |
| speed           | `pos.sp`             |
| ignition        | Sensor (resolvido)   |
| fuel_level      | Sensor (resolvido)   |
| rpm             | Sensor (resolvido)   |
| battery_voltage | Sensor (resolvido)   |
| engine_hours    | Sensor (resolvido)   |
| driver          | `drv` (binding)      |

---

## 🔐 **Configuração**

Copie `.env.example` para `.env` e configure:

```bash
# OBRIGATÓRIO: Token Wialon
WIALON_TOKEN=seu_token_aqui

# OPCIONAL: Configurações de exportação
EXPORT_DIR=./exports
WIALON_PAGE_SIZE=1000

# OPCIONAL: Google Drive (para upload automático)
GOOGLE_DRIVE_CREDENTIALS_FILE=./client_secrets.json
GOOGLE_DRIVE_FOLDER_ID=seu_folder_id_aqui
```

**Obtendo o Token Wialon:**

1. Acesse o Wialon
2. Vá em Gestão de Usuários > Token de Acesso
3. Crie um novo token com permissões de leitura

**Configurando Google Drive (opcional):**

1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Crie um projeto e ative a **Google Drive API**
3. Configure a **Tela de consentimento OAuth** (tipo: Externo)
4. Crie credenciais **ID do cliente OAuth** → **App para computador**
5. Baixe o JSON e salve como `client_secrets.json` na raiz do projeto
6. Crie uma pasta no Google Drive e copie o ID da URL
7. Na primeira execução com `--upload`, o navegador abrirá para login

---

## 🧠 **Fluxo de Exportação**

1. **Autenticação**: Login na API Wialon, obtém session ID
2. **Listar veículos**: Busca todas as units disponíveis
3. **Para cada veículo**:
    - Buscar mapa de sensores (com cache)
    - Buscar histórico paginado do mês
    - Transformar dados brutos para formato intermediário
    - Normalizar via `DataNormalizer`
    - Exportar arquivo individual (CSV/Excel)
4. **Arquivo consolidado**: Todos os veículos em um único arquivo
5. **Logout**: Encerra sessão Wialon

### Arquivos Gerados

```
exports/
└── 2025-12/
    ├── historico_123456_12_2025.csv      # Individual por veículo
    ├── historico_789012_12_2025.csv
    ├── historico_consolidado_12_2025.csv # Todos os veículos
    └── veiculos_12_2025.csv              # Lista de veículos
```

---

## 🗂️ **Dependências**

```
requests                    # HTTP client
python-dotenv               # Carrega .env
loguru                      # Logging
pandas                      # Manipulação de dados
openpyxl                    # Exportação Excel
google-auth                 # Autenticação Google
google-auth-oauthlib        # OAuth2 Google
google-api-python-client    # API Google Drive
```

Instale com: `pip install -r requirements.txt`

---

## ✅ **Status de Implementação**

| Componente                  | Status       |
| --------------------------- | ------------ |
| Cliente Wialon              | ✅ Completo  |
| Autenticação Stateful       | ✅ Completo  |
| Listagem de Veículos        | ✅ Completo  |
| Resolução de Sensores       | ✅ Completo  |
| Busca Paginada de Histórico | ✅ Completo  |
| Normalização de Dados       | ✅ Completo  |
| Exportação CSV              | ✅ Completo  |
| Exportação Excel            | ✅ Completo  |
| CLI Completa                | ✅ Completo  |
| Upload Google Drive         | ✅ Completo  |
| Interface GUI               | ✅ Completo  |
| Auto-Update                 | ✅ Completo  |
| Build/Distribuição          | ✅ Completo  |
| Testes Automatizados        | ⏳ Planejado |

---

---

## 📦 **Build e Distribuição**

### Gerar Executável Localmente

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou: venv\Scripts\activate  # Windows

# Executar build
python scripts/build.py

# O executável será gerado em dist/MoviExporter.exe (Windows) ou dist/MoviExporter.app (macOS)
```

### Build Automático via GitHub Actions

O projeto está configurado para gerar executáveis automaticamente a cada release:

1. Crie uma tag de versão:

```bash
git tag v1.0.0
git push origin v1.0.0
```

2. O GitHub Actions irá:
    - Compilar para Windows (.exe) e macOS (.app)
    - Criar uma Release automaticamente
    - Anexar os executáveis à Release

### Sistema de Auto-Update

O app verifica automaticamente por atualizações no GitHub Releases ao iniciar.
Configure seu repositório em `src/gui/updater.py`:

```python
GITHUB_OWNER = "seu-usuario"
GITHUB_REPO = "movi_exporter_app"
```

---

## 📌 **Resumo**

O Movi Exporter App automatiza a extração de dados de telemetria veicular da API Wialon, normalizando e exportando em formatos padronizados (CSV/Excel). A arquitetura é modular e extensível, suportando adição de novos sistemas de rastreamento no futuro.
