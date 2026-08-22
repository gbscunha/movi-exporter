# 📘 **Movi Exporter App**

## 📌 **Visão Geral**

O **Movi Exporter App** é um aplicativo desktop (Python + CustomTkinter) criado para **automatizar a extração e exportação dos dados históricos mensais dos veículos** monitorados pela **Movi Solutions**.

Ele se conecta à **API Wialon Hosting**, extrai a telemetria do mês (posição, velocidade, odômetro, sensores, motorista), normaliza e exporta em CSV/Excel — com upload opcional para o Google Drive. Também tem uma CLI para uso técnico/automatizado.

**Status:** ✅ **v1.5.0 em produção** (1 cliente, Windows). Manual do usuário final embarcado no app: [`docs/manual/manual.html`](docs/manual/manual.html).

---

## 🚀 **Início Rápido**

### Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd movi_exporter_app

# Crie e ative o ambiente virtual
python3.12 -m venv venv   # mesma versão do CI e do build (no macOS: brew install python@3.12 python-tk@3.12)
source venv/bin/activate  # Linux/macOS
# ou: venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env e adicione seu WIALON_TOKEN (ou configure pela tela Configurações do app)
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

# Exportar em Excel / em ambos os formatos
python -m src.cli.main export --format xlsx
python -m src.cli.main export --format both

# Preencher a coluna Localização (geocodificação — mais lento)
python -m src.cli.main export --addresses

# Usar a segunda conta Wialon (WIALON_TOKEN_2)
python -m src.cli.main export --account 2

# Exportar e fazer upload para Google Drive
python -m src.cli.main export --format xlsx --upload

# Testar conexão com Google Drive
python -m src.cli.main test-drive
```

Outras opções: `--no-consolidated` (não gera o arquivo consolidado) e `--output DIR`.

---

## 🧩 **Arquitetura do Projeto**

```
movi_exporter_app/
├── src/
│   ├── core/
│   │   ├── config.py             # Configurações (carrega .env, recarregável em runtime)
│   │   ├── logger.py             # Logging com loguru (app.log + handler da GUI)
│   │   ├── env_writer.py         # Grava chaves no .env (tela Configurações)
│   │   └── service_factory.py    # Ponto único de criação do VehicleService (GUI/CLI nunca instanciam o client)
│   │
│   ├── clients/
│   │   ├── protocols.py          # Protocol TrackingClient (interface)
│   │   └── wialon_client.py      # Cliente Wialon (stateful: sid + gis_sid, re-auth, paginação)
│   │
│   ├── services/
│   │   ├── vehicle_service.py    # Orquestração do export (lotes de 100 veículos)
│   │   ├── wialon_transformer.py # Mensagens Wialon → formato intermediário (sensores, motorista)
│   │   ├── tracker_profiles/     # Perfis por fabricante (Suntech, Jimi, Default)
│   │   ├── normalizer.py         # Normalização de campos
│   │   ├── exporter.py           # CSV/Excel, colunas em PT-BR, N/D
│   │   ├── uploader.py           # Upload Google Drive
│   │   └── export_history.py     # Histórico de exports (tela Home)
│   │
│   ├── gui/                      # CustomTkinter: app, frames/, components/, dialogs/, updater
│   └── cli/
│       └── main.py               # Interface de linha de comando
│
├── tests/                        # pytest (247 testes)
├── scripts/build.py              # Build local com PyInstaller
├── docs/                         # manual do usuário, specs, ADRs, planos, docs da API Wialon
├── exports/                      # Arquivos exportados (por mês/conta) — não versionado
├── .env / .env.example           # Configuração (o .env não é versionado)
└── requirements.txt              # Dependências pinadas (gerado de requirements.in)
```

Sentido das dependências: `gui`/`cli` → `core/service_factory` → `services` → `clients` → rede. Detalhes em [`CLAUDE.md`](CLAUDE.md) e [`.claude/rules/code-conventions.md`](.claude/rules/code-conventions.md).

---

## 🔌 **Integração com Wialon**

O cliente Wialon (`WialonClient`) implementa:

-   **Autenticação stateful** via sessão (`sid`), não Bearer Token — o login também devolve `gis_sid` e as URLs de GIS
-   **Reautenticação automática** quando a sessão expira
-   **Listagem de veículos** via `core/search_items`
-   **Resolução de sensores** via `core/search_item` (com cache) e **perfis por fabricante** (`tracker_profiles/`)
-   **Busca paginada de histórico** via `messages/load_interval` com `flagsMask=0` (captura mensagens data-only, ex.: tensão do veículo)
-   **Motoristas** via cartão RFID (`rfid_tag` → lista `drvrs` do resource)
-   **Geocodificação** opcional (coluna Localização) via `gis_geocode`, com cache por coordenada
-   **Export em lotes de 100 veículos** para limitar memória em frotas grandes
-   **Tratamento de erros** específicos da API (error=1, error=4)

### Dados Extraídos

| Coluna (export)         | Origem Wialon                                                                 |
| ----------------------- | ----------------------------------------------------------------------------- |
| Data/Hora               | `t` (Unix timestamp)                                                          |
| Latitude / Longitude    | `pos.y` / `pos.x`                                                             |
| Velocidade (km/h)       | `pos.sp`                                                                      |
| Odômetro (km)           | `params.odometer` (metros → km)                                               |
| Ignição                 | Sensor (via perfil do tracker)                                                |
| Localização             | Geocodificação das coordenadas (opcional, `--addresses` / opção na GUI)       |
| Nível de Combustível (%)| Sensor                                                                        |
| RPM                     | Sensor                                                                        |
| Tensão do Veículo (V)   | `pwr_ext` (~12–28 V)                                                          |
| Bateria Interna (V)     | `pwr_int` / `voltage` (~4 V — bateria do próprio rastreador)                  |
| Horas de Motor          | Sensor                                                                        |
| Motorista               | `rfid_tag` casado com o Código do motorista (forward-fill por veículo)        |

Campos de sensor sem dado saem como **`N/D`** — nunca vazio ou `NaN`.

---

## 🔐 **Configuração**

Copie `.env.example` para `.env` e configure (ou use a tela **Configurações** do app, que grava o `.env`):

```bash
# OBRIGATÓRIO: Token Wialon da conta principal
WIALON_TOKEN=seu_token_aqui

# OPCIONAL: segunda conta Wialon (habilita o seletor de conta no app e --account 2 na CLI)
WIALON_TOKEN_2=

# OPCIONAL: exportação
EXPORT_DIR=./exports
WIALON_PAGE_SIZE=1000

# OPCIONAL: Google Drive (para upload automático)
GOOGLE_DRIVE_CREDENTIALS_FILE=./client_secrets.json
GOOGLE_DRIVE_FOLDER_ID=seu_folder_id_aqui

# OPCIONAL: tema da interface (dark | light | system)
APP_THEME=dark
```

**Obtendo o Token Wialon:** o token é gerado pelo **fluxo de autorização web** da Wialon (o botão **Gerar** na tela Configurações abre o login; após entrar, o token volta na URL, após `access_token=`). Passo a passo com telas no manual, seção 2.

**Configurando Google Drive (opcional):**

1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Crie um projeto e ative a **Google Drive API**
3. Configure a **Tela de consentimento OAuth** (tipo: Externo)
4. Crie credenciais **ID do cliente OAuth** → **App para computador**
5. Baixe o JSON e salve como `client_secrets.json` na raiz do projeto
6. Crie uma pasta no Google Drive e copie o ID da URL
7. Na primeira execução com upload, o navegador abrirá para login (gera `token.json`, não versionado)

---

## 🧠 **Fluxo de Exportação**

1. **Autenticação**: login na API Wialon (obtém `sid`, `gis_sid` e URLs de GIS)
2. **Listar veículos** e **motoristas** da conta
3. **Em lotes de 100 veículos**, para cada veículo:
    - Buscar mapa de sensores (com cache) e detectar o perfil do tracker
    - Buscar histórico paginado do mês
    - Transformar (sensores, motorista via RFID) → normalizar → exportar arquivo individual
4. **Geocodificação** (se habilitada): coordenadas deduplicadas → coluna Localização
5. **Arquivo consolidado**: todos os veículos em um único arquivo (+ lista de veículos)
6. **Upload** opcional para o Google Drive e **logout**

### Arquivos Gerados

```
exports/
└── 2025-12/                      # YYYY-MM (com conta 2 configurada: 2025-12/<conta>/)
    ├── ABC1D23_Histórico_Padrão_15.12.2025_15-31-19.csv    # Individual por veículo (placa)
    ├── DEF4G56_Histórico_Padrão_15.12.2025_15-31-19.csv
    ├── Histórico_Consolidado_15.12.2025_15-31-19.csv        # Todos os veículos
    └── Veículos_15.12.2025_15-31-19.csv                     # Lista de veículos
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
customtkinter               # Interface gráfica
pillow                      # Imagens/ícones da GUI
packaging                   # Comparação de versões (auto-update)
pyinstaller                 # Build do executável
```

`requirements.txt` é pinado a partir de `requirements.in` (`pip-compile`). Não adicione dependência sem decisão registrada — o PyInstaller é sensível a imports inesperados.

---

## ✅ **Status de Implementação**

| Componente                                   | Status       |
| -------------------------------------------- | ------------ |
| Cliente Wialon (stateful, re-auth, paginação)| ✅ Completo  |
| Perfis de tracker (Suntech, Jimi, Default)   | ✅ Completo  |
| Normalização e exportação CSV/Excel (`N/D`)  | ✅ Completo  |
| Export em lotes de 100 veículos              | ✅ v1.5.0    |
| Motorista via RFID                           | ✅ v1.4.0    |
| Localização (geocodificação)                 | ✅ v1.4.0    |
| Duas contas Wialon (`WIALON_TOKEN_2`)        | ✅ Completo  |
| Interface GUI (CustomTkinter, tema, manual)  | ✅ Completo  |
| CLI completa                                 | ✅ Completo  |
| Upload Google Drive                          | ✅ Completo  |
| Auto-update via GitHub Releases              | ✅ Completo  |
| Build/Distribuição (Windows + macOS)         | ✅ Completo  |
| Testes automatizados                         | ✅ 247 testes (pytest) + CI |

---

## 📦 **Build e Distribuição**

### Gerar Executável Localmente

```bash
source venv/bin/activate  # ou: venv\Scripts\activate  # Windows
python scripts/build.py
# Gera dist/MoviExporter.exe (Windows) ou dist/MoviExporter.app (macOS)
```

### Build Automático via GitHub Actions

1. Atualize `__version__` em `src/gui/__init__.py` e crie a tag correspondente (o workflow **falha** se tag ≠ `__version__`):

```bash
git tag v1.5.0
git push origin v1.5.0
```

2. O workflow `build.yml` compila para Windows (.exe) e macOS (.app), cria a Release e anexa os executáveis.

### Sistema de Auto-Update

O app verifica atualizações nas Releases de `gbscunha/movi-exporter` ao iniciar (`src/gui/updater.py`) e oferece o download quando há versão nova.

---

## 🛠️ **Desenvolvimento**

```bash
pytest -q                          # testes
ruff check src/                    # lint
ruff format src/ tests/            # formatter (o CI roda --check)
git config blame.ignoreRevsFile .git-blame-ignore-revs   # uma vez: ignora commits só de formatação no blame
```

- CI (`.github/workflows/ci.yml`): pytest + ruff check + ruff format --check em todo push/PR. Python 3.12.
- Regras do projeto e ciclo de desenvolvimento: [`CLAUDE.md`](CLAUDE.md), [`.claude/skills/xp-cycle/SKILL.md`](.claude/skills/xp-cycle/SKILL.md)
- Specs de feature: [`docs/specs/`](docs/specs/) · Decisões arquiteturais: [`docs/decisions/`](docs/decisions/)
- Guia técnico da CLI: [`docs/cliente/USER_GUIDE.md`](docs/cliente/USER_GUIDE.md) · Referência da API Wialon: [`docs/wialon-api-docs/`](docs/wialon-api-docs/)

---

## 📌 **Resumo**

O Movi Exporter App automatiza a extração de dados de telemetria veicular da API Wialon, normalizando e exportando em formatos padronizados (CSV/Excel), com interface gráfica para o cliente e CLI para automação. A arquitetura é modular (client → services → GUI/CLI via `service_factory`), com perfis por fabricante de rastreador e suporte a múltiplas contas.
