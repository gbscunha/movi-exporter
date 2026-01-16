# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Movi Exporter App** is a Python automation tool that extracts and exports monthly historical vehicle data from a vehicle tracking system (currently Wialon) used by Movi Solutions. The goal is to eliminate manual data collection by automatically integrating with the tracking API, normalizing the data, and exporting it in structured formats (CSV/Excel) with optional Google Drive upload.

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

**Key Pattern**: Two base classes for different authentication models:
- `BaseClient`: HTTP client with Bearer token (for REST APIs)
- `StatefulClient`: HTTP client with session ID (for stateful APIs like Wialon)

- `base_client.py`: Base HTTP clients with standardized methods
- `wialon_client.py`: **Main client** - Integration with Wialon Hosting API
  - Stateful authentication via `sid` (session ID)
  - Automatic re-authentication on session expiry
  - `authenticate()`: Login via token/login
  - `list_vehicles()`: Lists all units via core/search_items
  - `get_vehicle_sensors(vehicle_id)`: Gets sensor mapping via core/search_item
  - `get_history(vehicle_id, time_from, time_to)`: Paginated history via messages/load_interval
- `system_a_client.py`: Legacy client for System A (example)

**Extensibility**: New systems can be added by inheriting from `BaseClient` or `StatefulClient`.

### Services Layer (`src/services/`)

- `normalizer.py`: ✅ **Implemented** - Standardizes data formats from different tracking systems
  - `DataNormalizer` class with configurable field mappings per system
  - `normalize_vehicle_list()`: Normalizes vehicle data to standard format
  - `normalize_history()`: Normalizes historical records to standard format
  - `add_system_mapping()`: Allows adding new system mappings dynamically
  - Supports nested field paths and multiple timestamp formats
  - Preserves raw data for audit purposes
  - **Supports**: `system_a` and `wialon` mappings

- `exporter.py`: ✅ **Implemented** - Export to CSV/Excel
  - `DataExporter` class with organized folder structure by month/year
  - `export_vehicles_to_csv/excel()`: Export vehicle list
  - `export_history_to_csv/excel()`: Export individual vehicle history
  - `export_consolidated_history_to_csv/excel()`: Export all vehicles in one file
  - Adds metadata (export_date, system_source) to exported files

- `vehicle_service.py`: ✅ **Implemented** - Main orchestration service
  - `VehicleService` class coordinating full extraction flow
  - `export_monthly_data()`: Main method for monthly extraction
  - `list_vehicles()`: Lists available vehicles
  - `test_connection()`: Tests Wialon API connection
  - Handles pagination, sensor resolution, error recovery
  - Returns detailed statistics via `ExportResult` dataclass

- Planned services:
  - `uploader.py`: Upload to Google Drive

**Normalizer Design**: The normalizer uses a mapping-based approach where each system has a dictionary mapping standard field names to system-specific field names. Supports `system_a` and `wialon`. New systems can be added via `add_system_mapping()` method.

### CLI Layer (`src/cli/`)

- `main.py`: Command-line interface entry point with basic integration testing

## Configuration

All API credentials and URLs are stored in `.env`:

```
# Wialon (main system)
WIALON_TOKEN=your_wialon_api_token

# System A (legacy/example)
SYSTEM_A_BASE_URL=https://api.sistema-a.com
SYSTEM_A_TOKEN=token_a

# Export settings
EXPORT_DIR=./exports
WIALON_PAGE_SIZE=1000
```

Never commit `.env` to version control.

**Note:** The Wialon API is stateful and uses session-based authentication (NOT Bearer token). The `WIALON_TOKEN` is used only for initial login, after which a session ID (`sid`) is used.

## Core Workflow

Current workflow for Wialon (via `VehicleService`):

1. **Authentication**: Login via `token/login`, obtain session ID (`sid`)
2. **List vehicles**: Fetch units via `core/search_items`
3. **For each vehicle**:
   - Fetch sensor mapping via `core/search_item` (cached)
   - Fetch paginated history via `messages/load_interval`
   - Transform raw Wialon messages to intermediate format
   - Normalize data via `DataNormalizer.normalize_history(data, system="wialon")`
   - Export to CSV/Excel via `DataExporter`
4. **Generate consolidated file** with all vehicles (optional)
5. **Logout**: End Wialon session

**CLI Usage**:
```bash
# Test connection
python -m src.cli.main test

# List vehicles
python -m src.cli.main list

# Export monthly data (default: previous month)
python -m src.cli.main export --month 12 --year 2025

# Export specific vehicles
python -m src.cli.main export --month 12 --year 2025 --vehicles 123,456

# Export to Excel
python -m src.cli.main export --month 12 --year 2025 --format xlsx
```

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

- **Wialon as Primary System**: Main integration with Wialon Hosting API
  - Stateful authentication via session ID (`sid`), NOT Bearer token
  - Automatic re-authentication on session expiry
  - Paginated data fetching to avoid memory issues
- **Extensible Architecture**: Supports multiple systems via mapping approach
  - `BaseClient`: For REST APIs with Bearer token
  - `StatefulClient`: For session-based APIs (like Wialon)
  - Normalizer mappings isolate system-specific logic
- **No Wialon Logic in Normalizer/Exporter**: 
  - Raw data transformation happens in `VehicleService`
  - Normalizer receives pre-processed data
- **Monthly Granularity**: Data extraction is organized by vehicle and month
- **Sensor Resolution**: Wialon raw parameters (io_23, etc.) are mapped to readable names
- **Environment-based Config**: All secrets and URLs loaded from `.env`
- **Data Preservation**: `raw_data` field preserves original system response
- **Type Safety**: Python type hints throughout for IDE support
