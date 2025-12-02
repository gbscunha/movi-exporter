# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Movi Exporter App** is a Python automation tool that extracts and exports monthly historical vehicle data from two different vehicle tracking systems used by Movi Solutions. The goal is to eliminate manual data collection by automatically integrating with both tracking APIs, normalizing the data, and exporting it in structured formats (CSV/Excel) with optional Google Drive upload.

## Development Environment

- Python 3.14 with virtual environment (venv)
- Dependencies: `requests`, `python-dotenv`, `loguru`
- Install dependencies: Activate venv first, then run `pip install -r requirements.txt`
- Activate venv: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)

## Running the Application

The main entry point is `src/cli/main.py`. Run from project root:

```bash
python -m src.cli.main
```

This currently tests integration with both tracking systems by listing vehicles.

## Architecture

The codebase follows a modular architecture with clear separation of concerns:

### Core Layer (`src/core/`)

- `config.py`: Loads environment variables from `.env` using dotenv, exposes a `settings` singleton
- `logger.py`: Configures loguru with file rotation (1 MB) to `app.log`

### Client Layer (`src/clients/`)

**Key Pattern**: BaseClient provides standardized HTTP GET with Bearer token authentication

- `base_client.py`: Base HTTP client with `_headers()` and `get()` methods
- `system_a_client.py`: Integration for System A tracking API
  - `listar_veiculos()`: Lists all vehicles
  - `buscar_historico(veiculo_id, mes)`: Fetches monthly history by vehicle ID
- `system_b_client.py`: Integration for System B tracking API
  - `listar_veiculos()`: Lists all vehicles
  - `buscar_historico(device_id, month)`: Fetches monthly history by device ID

**Important**: The two systems use different endpoint names and parameter names (e.g., `veiculos` vs `vehicles`, `veiculoId` vs `device`), but the base functionality is identical.

### Services Layer (`src/services/`)

Currently empty but planned for:
- `normalizer.py`: Standardize data formats between System A and System B
- `exporter.py`: Generate CSV/Excel exports
- `uploader.py`: Upload to Google Drive
- `vehicle_service.py`: Main orchestration logic for monthly exports

### CLI Layer (`src/cli/`)

- `main.py`: Command-line interface entry point with basic integration testing

## Configuration

All API credentials and URLs are stored in `.env`:

```
SYSTEM_A_BASE_URL=https://api.sistema-a.com
SYSTEM_A_TOKEN=token_a
SYSTEM_B_BASE_URL=https://api.sistema-b.com
SYSTEM_B_TOKEN=token_b
```

Never commit `.env` to version control.

## Core Workflow (Planned)

For each tracking system:
1. Fetch list of vehicles using client's `listar_veiculos()`
2. For each vehicle, fetch monthly historical data using `buscar_historico()`
3. Normalize data to common format (handles differences between systems)
4. Export to CSV/Excel with standardized columns
5. Optionally upload to Google Drive

This will be implemented in `vehicle_service.py`.

## Key Design Decisions

- **Dual System Support**: Both tracking systems are treated as first-class citizens with dedicated client implementations
- **Bearer Token Auth**: All API requests use Bearer token authentication via `Authorization` header
- **Monthly Granularity**: Data extraction is organized by vehicle and month
- **Environment-based Config**: All secrets and URLs loaded from `.env` for security and flexibility
