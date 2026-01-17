"""
Services module for data processing and export operations.

Módulos:
- normalizer: Normalização de dados de diferentes sistemas
- exporter: Exportação para CSV/Excel
- vehicle_service: Orquestração do fluxo de extração
- uploader: Upload para Google Drive
"""

from .normalizer import DataNormalizer
from .exporter import DataExporter
from .vehicle_service import VehicleService, ExportResult, VehicleStats
from .uploader import DriveUploader, UploadResult

__all__ = [
    "DataNormalizer",
    "DataExporter",
    "VehicleService",
    "ExportResult",
    "VehicleStats",
    "DriveUploader",
    "UploadResult",
]
