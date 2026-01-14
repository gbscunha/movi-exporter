# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Movi Exporter App** is a Python automation tool that extracts and exports monthly historical vehicle data from a vehicle tracking system (currently System A) used by Movi Solutions. The goal is to eliminate manual data collection by automatically integrating with the tracking API, normalizing the data, and exporting it in structured formats (CSV/Excel) with optional Google Drive upload.

**Note:** The architecture is designed to support multiple tracking systems in the future, if needed.

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

This currently tests integration with System A by listing vehicles.

## Architecture

The codebase follows a modular architecture with clear separation of concerns:

### Core Layer (`src/core/`)

- `config.py`: Loads environment variables from `.env` using dotenv, exposes a `settings` singleton
- `logger.py`: Configures loguru with file rotation (1 MB) to `app.log`

### Client Layer (`src/clients/`)

**Key Pattern**: BaseClient provides standardized HTTP GET with Bearer token authentication

- `base_client.py`: Base HTTP client with `_headers()` and `get()` methods
- `system_a_client.py`: Integration for System A tracking API (currently active)
  - `listar_veiculos()`: Lists all vehicles
  - `buscar_historico(veiculo_id, mes)`: Fetches monthly history by vehicle ID

**Extensibility**: The architecture allows easy addition of new systems (SystemBClient, SystemCClient, etc.) by inheriting from `BaseClient` and implementing system-specific methods. Different systems may use different endpoint names and parameter names, but the base functionality remains standardized.

### Services Layer (`src/services/`)

- `normalizer.py`: ✅ **Implemented** - Standardizes data formats from different tracking systems
  - `DataNormalizer` class with configurable field mappings per system
  - `normalize_vehicle_list()`: Normalizes vehicle data to standard format
  - `normalize_history()`: Normalizes historical records to standard format
  - `add_system_mapping()`: Allows adding new system mappings dynamically
  - Supports nested field paths and multiple timestamp formats
  - Preserves raw data for audit purposes
  
- Planned services:
  - `exporter.py`: Generate CSV/Excel exports
  - `uploader.py`: Upload to Google Drive
  - `vehicle_service.py`: Main orchestration logic for monthly exports

**Normalizer Design**: The normalizer uses a mapping-based approach where each system has a dictionary mapping standard field names to system-specific field names. Currently supports `system_a`, but new systems can be added via `add_system_mapping()` method.

### CLI Layer (`src/cli/`)

- `main.py`: Command-line interface entry point with basic integration testing

## Configuration

All API credentials and URLs are stored in `.env`:

```
SYSTEM_A_BASE_URL=https://api.sistema-a.com
SYSTEM_A_TOKEN=token_a
```

Never commit `.env` to version control.

**Note:** If additional systems are added in the future, simply add new environment variables (SYSTEM_B_BASE_URL, SYSTEM_B_TOKEN, etc.) and update `config.py` accordingly.

## Core Workflow

Current workflow for System A:
1. Fetch list of vehicles using `SystemAClient.listar_veiculos()`
2. For each vehicle, fetch monthly historical data using `buscar_historico(veiculo_id, mes)`
3. Normalize data to common format using `DataNormalizer`
   - Vehicle data: `normalize_vehicle_list(raw_data, system="system_a")`
   - Historical data: `normalize_history(raw_data, system="system_a")`
4. Export to CSV/Excel with standardized columns (to be implemented)
5. Optionally upload to Google Drive (to be implemented)

The orchestration logic will be implemented in `vehicle_service.py`.

### Normalized Data Format

**Vehicles:**
```python
{
    "id": "ABC123",
    "name": "Vehicle Name",
    "plate": "ABC-1234",
    "system_source": "system_a",
    "raw_data": {...}  # Original data preserved
}
```

**Historical Records:**
```python
{
    "vehicle_id": "ABC123",
    "timestamp": "2024-01-15T14:30:00",  # ISO 8601 format
    "latitude": -23.5505,
    "longitude": -46.6333,
    "speed": 60.5,
    "odometer": 15000.0,
    "ignition": True,
    "address": "Street Address",
    "system_source": "system_a",
    "raw_data": {...}  # Original data preserved
}
```

## Key Design Decisions

- **Single System (Extensible Architecture)**: Currently uses System A, but architecture supports multiple systems
  - Clients inherit from `BaseClient` for standardized HTTP operations
  - Normalizer uses mapping-based approach for easy system addition
  - New systems can be added without modifying existing code
- **Bearer Token Auth**: All API requests use Bearer token authentication via `Authorization` header
- **Monthly Granularity**: Data extraction is organized by vehicle and month
- **Environment-based Config**: All secrets and URLs loaded from `.env` for security and flexibility
- **Data Preservation**: Normalized data includes `raw_data` field to preserve original system response
- **Flexible Field Mapping**: Normalizer supports nested field paths (e.g., `location.lat`) and default values
- **Type Safety**: Uses Python type hints throughout for better IDE support and error prevention
