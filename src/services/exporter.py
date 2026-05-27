"""
Módulo responsável pela exportação de dados normalizados para arquivos CSV e Excel.

Este módulo fornece funcionalidades para:
- Exportar dados de veículos e histórico para CSV
- Exportar dados de veículos e histórico para Excel
- Criar estrutura de pastas organizadas por mês/ano
- Adicionar metadados aos arquivos exportados
- Gerar nomenclatura padronizada de arquivos
"""

import os
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.core.logger import logger


def _format_ignition(value: Any) -> Optional[str]:
    """
    Converte valor booleano de ignição para texto legível.

    Args:
        value: Valor da ignição (True/False ou None)

    Returns:
        "Ligado" se True, "Desligado" se False, None se None
    """
    if value is None:
        return None
    return "Ligado" if value else "Desligado"


# Colunas de sensor que podem legitimamente não ter dado para uma mensagem
# específica. Para essas, substituímos None por "N/D" no export para que o
# cliente veja explicitamente "sem dado" em vez de célula vazia.
# Latitude/longitude/velocidade/ignição/timestamp continuam obrigatórios.
OPTIONAL_SENSOR_COLS = [
    "odometer",
    "fuel_level",
    "rpm",
    "battery_voltage",
    "engine_hours",
    "driver",
    "address",
]


def _fill_nd(record: Dict[str, Any]) -> Dict[str, Any]:
    """Substitui None por "N/D" nas colunas de sensor opcionais."""
    for col in OPTIONAL_SENSOR_COLS:
        if record.get(col) is None:
            record[col] = "N/D"
    return record


# Mapeamento de tradução de colunas (inglês → português)
COLUMN_TRANSLATIONS = {
    # Metadados
    "export_date": "Data de Exportação",
    "system_source": "Sistema de Origem",
    # Dados de veículos
    "id": "ID do Veículo",
    "name": "Nome do Veículo",
    "plate": "Placa",
    # Dados de histórico
    "vehicle_id": "ID do Veículo",
    "vehicle_name": "Nome do Veículo",
    "timestamp": "Data/Hora",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "speed": "Velocidade (km/h)",
    "odometer": "Odômetro (km)",
    "ignition": "Ignição",
    "address": "Localização",
    "fuel_level": "Nível de Combustível (%)",
    "rpm": "RPM",
    "battery_voltage": "Tensão da Bateria (V)",
    "engine_hours": "Horas de Motor",
    "driver": "Motorista",
}


class DataExporter:
    """
    Classe responsável por exportar dados normalizados para diferentes formatos.

    Suporta exportação para CSV e Excel, com organização automática de pastas
    e nomenclatura padronizada de arquivos.
    """

    def __init__(self, base_export_dir: str = "./exports"):
        """
        Inicializa o exportador de dados.

        Args:
            base_export_dir: Diretório base para exportação (padrão: ./exports)
        """
        self.base_export_dir = Path(base_export_dir)
        self._ensure_base_dir()
        logger.info(
            f"DataExporter inicializado com diretório base: {self.base_export_dir}"
        )

    def _ensure_base_dir(self) -> None:
        """Garante que o diretório base de exportação existe."""
        self.base_export_dir.mkdir(parents=True, exist_ok=True)

    def _create_month_directory(
        self,
        month: int,
        year: int,
        account_name: Optional[str] = None,
    ) -> Path:
        """
        Cria e retorna o diretório para um mês/ano específico.

        Args:
            month: Mês (1-12)
            year: Ano (ex: 2024)
            account_name: Nome da conta — se fornecido, gera subpasta
                          dentro de `YYYY-MM/` para isolar exports de cada conta

        Returns:
            Path do diretório criado.
            Sem account_name: `exports/2024-10/`
            Com account_name: `exports/2024-10/Conta 1/`
        """
        month_dir = self.base_export_dir / f"{year}-{month:02d}"
        if account_name:
            month_dir = month_dir / account_name
        month_dir.mkdir(parents=True, exist_ok=True)
        return month_dir

    def _generate_filename(
        self,
        prefix: str,
        vehicle_plate: Optional[str] = None,
        extension: str = "csv",
    ) -> str:
        """
        Gera nome padronizado para arquivo de exportação.

        Formato: {PLACA}_Histórico_Padrão_{DD.MM.YYYY}_{HH-MM-SS}.{ext}
        Ou para consolidados: Histórico_Consolidado_{DD.MM.YYYY}_{HH-MM-SS}.{ext}

        Args:
            prefix: Tipo do arquivo (ex: "Histórico_Padrão", "Histórico_Consolidado", "Veículos")
            vehicle_plate: Placa do veículo (opcional, para arquivos individuais)
            extension: Extensão do arquivo (csv ou xlsx)

        Returns:
            Nome do arquivo (ex: "SYO6B89_Histórico_Padrão_15.12.2025_15-31-19.csv")
        """
        now = datetime.now()
        date_str = now.strftime("%d.%m.%Y")
        time_str = now.strftime("%H-%M-%S")

        if vehicle_plate:
            filename = f"{vehicle_plate}_{prefix}_{date_str}_{time_str}.{extension}"
        else:
            filename = f"{prefix}_{date_str}_{time_str}.{extension}"

        return filename

    def _add_metadata_to_dataframe(
        self, df: pd.DataFrame, system_source: str, export_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Adiciona metadados ao DataFrame.

        Args:
            df: DataFrame original
            system_source: Sistema de origem dos dados
            export_date: Data de exportação (opcional, usa data atual se não fornecida)

        Returns:
            DataFrame com colunas de metadados adicionadas
        """
        df_copy = df.copy()

        if export_date is None:
            export_date = datetime.now().isoformat()

        # Adiciona metadados como primeiras colunas
        df_copy.insert(0, "export_date", export_date)
        df_copy.insert(1, "system_source", system_source)

        return df_copy

    def _translate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Traduz os nomes das colunas de inglês para português.

        Args:
            df: DataFrame com colunas em inglês

        Returns:
            DataFrame com colunas traduzidas para português
        """
        translated_columns = {
            col: COLUMN_TRANSLATIONS.get(col, col) for col in df.columns
        }
        return df.rename(columns=translated_columns)

    def export_vehicles_to_csv(
        self,
        vehicles: List[Dict[str, Any]],
        output_path: Optional[str] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        account_name: Optional[str] = None,
    ) -> str:
        """
        Exporta lista de veículos para arquivo CSV.

        Args:
            vehicles: Lista de veículos normalizados
            output_path: Caminho completo do arquivo de saída (opcional)
            month: Mês para organização de pastas (opcional)
            year: Ano para organização de pastas (opcional)

        Returns:
            Caminho do arquivo criado
        """
        if not vehicles:
            logger.warning("Lista de veículos vazia, nenhum arquivo será criado")
            return ""

        try:
            # Extrai dados sem o campo raw_data para o CSV
            clean_vehicles = []
            system_source = vehicles[0].get("system_source", "unknown")

            for vehicle in vehicles:
                clean_vehicle = {
                    "id": vehicle.get("id"),
                    "name": vehicle.get("name"),
                    "plate": vehicle.get("plate"),
                }
                clean_vehicles.append(clean_vehicle)

            # Cria DataFrame
            df = pd.DataFrame(clean_vehicles)

            # Adiciona metadados
            df = self._add_metadata_to_dataframe(df, system_source)

            # Define caminho de saída
            if output_path:
                file_path = Path(output_path)
            else:
                if month and year:
                    month_dir = self._create_month_directory(month, year, account_name)
                else:
                    month_dir = self.base_export_dir
                filename = self._generate_filename("Veículos", extension="csv")
                file_path = month_dir / filename

            # Garante que o diretório existe
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Traduz colunas para português
            df = self._translate_columns(df)

            # Exporta para CSV
            df.to_csv(file_path, index=False, encoding="utf-8-sig")

            logger.success(f"{len(vehicles)} veículos exportados para: {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Erro ao exportar veículos para CSV: {e}")
            raise

    def export_vehicles_to_excel(
        self,
        vehicles: List[Dict[str, Any]],
        output_path: Optional[str] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        account_name: Optional[str] = None,
    ) -> str:
        """
        Exporta lista de veículos para arquivo Excel.

        Args:
            vehicles: Lista de veículos normalizados
            output_path: Caminho completo do arquivo de saída (opcional)
            month: Mês para organização de pastas (opcional)
            year: Ano para organização de pastas (opcional)

        Returns:
            Caminho do arquivo criado
        """
        if not vehicles:
            logger.warning("Lista de veículos vazia, nenhum arquivo será criado")
            return ""

        try:
            # Extrai dados sem o campo raw_data para o Excel
            clean_vehicles = []
            system_source = vehicles[0].get("system_source", "unknown")

            for vehicle in vehicles:
                clean_vehicle = {
                    "id": vehicle.get("id"),
                    "name": vehicle.get("name"),
                    "plate": vehicle.get("plate"),
                }
                clean_vehicles.append(clean_vehicle)

            # Cria DataFrame
            df = pd.DataFrame(clean_vehicles)

            # Adiciona metadados
            df = self._add_metadata_to_dataframe(df, system_source)

            # Define caminho de saída
            if output_path:
                file_path = Path(output_path)
            else:
                if month and year:
                    month_dir = self._create_month_directory(month, year, account_name)
                else:
                    month_dir = self.base_export_dir
                filename = self._generate_filename("Veículos", extension="xlsx")
                file_path = month_dir / filename

            # Garante que o diretório existe
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Traduz colunas para português
            df = self._translate_columns(df)

            # Exporta para Excel
            df.to_excel(file_path, index=False, engine="openpyxl")

            logger.success(f"{len(vehicles)} veículos exportados para: {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Erro ao exportar veículos para Excel: {e}")
            raise

    def export_history_to_csv(
        self,
        history: List[Dict[str, Any]],
        vehicle_id: str,
        month: int,
        year: int,
        output_path: Optional[str] = None,
        vehicle_name: Optional[str] = None,
        vehicle_plate: Optional[str] = None,
        account_name: Optional[str] = None,
    ) -> str:
        """
        Exporta histórico de um veículo para arquivo CSV.

        Args:
            history: Lista de registros históricos normalizados
            vehicle_id: ID do veículo
            month: Mês dos dados (1-12)
            year: Ano dos dados
            output_path: Caminho completo do arquivo de saída (opcional)
            vehicle_name: Nome do veículo (opcional)
            vehicle_plate: Placa do veículo (opcional)

        Returns:
            Caminho do arquivo criado
        """
        if not history:
            logger.warning(
                f"Histórico vazio para veículo {vehicle_id}, nenhum arquivo será criado"
            )
            return ""

        try:
            # Extrai dados sem o campo raw_data para o CSV
            clean_history = []
            system_source = history[0].get("system_source", "unknown")

            for record in history:
                clean_record = {
                    "vehicle_id": record.get("vehicle_id"),
                    "vehicle_name": vehicle_name or record.get("vehicle_name"),
                    "plate": vehicle_plate or record.get("plate"),
                    "timestamp": record.get("timestamp"),
                    "latitude": record.get("latitude"),
                    "longitude": record.get("longitude"),
                    "speed": record.get("speed"),
                    "odometer": record.get("odometer"),
                    "ignition": _format_ignition(record.get("ignition")),
                    "address": record.get("address"),
                    "fuel_level": record.get("fuel_level"),
                    "rpm": record.get("rpm"),
                    "battery_voltage": record.get("battery_voltage"),
                    "engine_hours": record.get("engine_hours"),
                    "driver": record.get("driver"),
                }
                clean_history.append(_fill_nd(clean_record))

            # Cria DataFrame
            df = pd.DataFrame(clean_history)

            # Adiciona metadados
            df = self._add_metadata_to_dataframe(df, system_source)

            # Define caminho de saída
            if output_path:
                file_path = Path(output_path)
            else:
                month_dir = self._create_month_directory(month, year, account_name)
                # Usa placa para nome do arquivo, ou ID como fallback
                plate_for_filename = vehicle_plate or vehicle_id
                filename = self._generate_filename(
                    "Histórico_Padrão",
                    vehicle_plate=plate_for_filename,
                    extension="csv",
                )
                file_path = month_dir / filename

            # Garante que o diretório existe
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Traduz colunas para português
            df = self._translate_columns(df)

            # Exporta para CSV
            df.to_csv(file_path, index=False, encoding="utf-8-sig")

            logger.success(
                f"{len(history)} registros do veículo {vehicle_plate or vehicle_id} "
                f"({month:02d}/{year}) exportados para: {file_path}"
            )
            return str(file_path)

        except Exception as e:
            logger.error(f"Erro ao exportar histórico para CSV: {e}")
            raise

    def export_history_to_excel(
        self,
        history: List[Dict[str, Any]],
        vehicle_id: str,
        month: int,
        year: int,
        output_path: Optional[str] = None,
        vehicle_name: Optional[str] = None,
        vehicle_plate: Optional[str] = None,
        account_name: Optional[str] = None,
    ) -> str:
        """
        Exporta histórico de um veículo para arquivo Excel.

        Args:
            history: Lista de registros históricos normalizados
            vehicle_id: ID do veículo
            month: Mês dos dados (1-12)
            year: Ano dos dados
            output_path: Caminho completo do arquivo de saída (opcional)
            vehicle_name: Nome do veículo (opcional)
            vehicle_plate: Placa do veículo (opcional)

        Returns:
            Caminho do arquivo criado
        """
        if not history:
            logger.warning(
                f"Histórico vazio para veículo {vehicle_id}, nenhum arquivo será criado"
            )
            return ""

        try:
            # Extrai dados sem o campo raw_data para o Excel
            clean_history = []
            system_source = history[0].get("system_source", "unknown")

            for record in history:
                clean_record = {
                    "vehicle_id": record.get("vehicle_id"),
                    "vehicle_name": vehicle_name or record.get("vehicle_name"),
                    "plate": vehicle_plate or record.get("plate"),
                    "timestamp": record.get("timestamp"),
                    "latitude": record.get("latitude"),
                    "longitude": record.get("longitude"),
                    "speed": record.get("speed"),
                    "odometer": record.get("odometer"),
                    "ignition": _format_ignition(record.get("ignition")),
                    "address": record.get("address"),
                    "fuel_level": record.get("fuel_level"),
                    "rpm": record.get("rpm"),
                    "battery_voltage": record.get("battery_voltage"),
                    "engine_hours": record.get("engine_hours"),
                    "driver": record.get("driver"),
                }
                clean_history.append(_fill_nd(clean_record))

            # Cria DataFrame
            df = pd.DataFrame(clean_history)

            # Adiciona metadados
            df = self._add_metadata_to_dataframe(df, system_source)

            # Define caminho de saída
            if output_path:
                file_path = Path(output_path)
            else:
                month_dir = self._create_month_directory(month, year, account_name)
                # Usa placa para nome do arquivo, ou ID como fallback
                plate_for_filename = vehicle_plate or vehicle_id
                filename = self._generate_filename(
                    "Histórico_Padrão",
                    vehicle_plate=plate_for_filename,
                    extension="xlsx",
                )
                file_path = month_dir / filename

            # Garante que o diretório existe
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Traduz colunas para português
            df = self._translate_columns(df)

            # Exporta para Excel
            df.to_excel(file_path, index=False, engine="openpyxl")

            logger.success(
                f"{len(history)} registros do veículo {vehicle_plate or vehicle_id} "
                f"({month:02d}/{year}) exportados para: {file_path}"
            )
            return str(file_path)

        except Exception as e:
            logger.error(f"Erro ao exportar histórico para Excel: {e}")
            raise

    def export_consolidated_history_to_csv(
        self,
        all_history: Dict[str, List[Dict[str, Any]]],
        month: int,
        year: int,
        output_path: Optional[str] = None,
        vehicles_info: Optional[Dict[str, Dict[str, str]]] = None,
        account_name: Optional[str] = None,
    ) -> str:
        """
        Exporta histórico consolidado de todos os veículos para um único arquivo CSV.

        Args:
            all_history: Dicionário {vehicle_id: [registros]}
            month: Mês dos dados (1-12)
            year: Ano dos dados
            output_path: Caminho completo do arquivo de saída (opcional)
            vehicles_info: Dicionário {vehicle_id: {"name": nome, "plate": placa}} (opcional)

        Returns:
            Caminho do arquivo criado
        """
        if not all_history:
            logger.warning("Histórico consolidado vazio, nenhum arquivo será criado")
            return ""

        vehicles_info = vehicles_info or {}

        try:
            # Consolida todos os registros
            all_records = []
            system_source = "unknown"

            for vid, history in all_history.items():
                vehicle_data = vehicles_info.get(vid, {})
                for record in history:
                    if system_source == "unknown":
                        system_source = record.get("system_source", "unknown")

                    clean_record = {
                        "vehicle_id": record.get("vehicle_id"),
                        "vehicle_name": vehicle_data.get("name")
                        or record.get("vehicle_name"),
                        "plate": vehicle_data.get("plate") or record.get("plate"),
                        "timestamp": record.get("timestamp"),
                        "latitude": record.get("latitude"),
                        "longitude": record.get("longitude"),
                        "speed": record.get("speed"),
                        "odometer": record.get("odometer"),
                        "ignition": _format_ignition(record.get("ignition")),
                        "address": record.get("address"),
                        "fuel_level": record.get("fuel_level"),
                        "rpm": record.get("rpm"),
                        "battery_voltage": record.get("battery_voltage"),
                        "engine_hours": record.get("engine_hours"),
                        "driver": record.get("driver"),
                    }
                    all_records.append(_fill_nd(clean_record))

            if not all_records:
                logger.warning("Nenhum registro encontrado no histórico consolidado")
                return ""

            # Cria DataFrame
            df = pd.DataFrame(all_records)

            # Ordena por vehicle_id e timestamp
            df = df.sort_values(["vehicle_id", "timestamp"])

            # Adiciona metadados
            df = self._add_metadata_to_dataframe(df, system_source)

            # Define caminho de saída
            if output_path:
                file_path = Path(output_path)
            else:
                month_dir = self._create_month_directory(month, year, account_name)
                filename = self._generate_filename(
                    "Histórico_Consolidado", extension="csv"
                )
                file_path = month_dir / filename

            # Garante que o diretório existe
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Traduz colunas para português
            df = self._translate_columns(df)

            # Exporta para CSV
            df.to_csv(file_path, index=False, encoding="utf-8-sig")

            logger.success(
                f"{len(all_records)} registros consolidados de "
                f"{len(all_history)} veículos ({month:02d}/{year}) exportados para: {file_path}"
            )
            return str(file_path)

        except Exception as e:
            logger.error(f"Erro ao exportar histórico consolidado para CSV: {e}")
            raise

    def export_consolidated_history_to_excel(
        self,
        all_history: Dict[str, List[Dict[str, Any]]],
        month: int,
        year: int,
        output_path: Optional[str] = None,
        vehicles_info: Optional[Dict[str, Dict[str, str]]] = None,
        account_name: Optional[str] = None,
    ) -> str:
        """
        Exporta histórico consolidado de todos os veículos para um único arquivo Excel.

        Args:
            all_history: Dicionário {vehicle_id: [registros]}
            month: Mês dos dados (1-12)
            year: Ano dos dados
            output_path: Caminho completo do arquivo de saída (opcional)
            vehicles_info: Dicionário {vehicle_id: {"name": nome, "plate": placa}} (opcional)

        Returns:
            Caminho do arquivo criado
        """
        if not all_history:
            logger.warning("Histórico consolidado vazio, nenhum arquivo será criado")
            return ""

        vehicles_info = vehicles_info or {}

        try:
            # Consolida todos os registros
            all_records = []
            system_source = "unknown"

            for vid, history in all_history.items():
                vehicle_data = vehicles_info.get(vid, {})
                for record in history:
                    if system_source == "unknown":
                        system_source = record.get("system_source", "unknown")

                    clean_record = {
                        "vehicle_id": record.get("vehicle_id"),
                        "vehicle_name": vehicle_data.get("name")
                        or record.get("vehicle_name"),
                        "plate": vehicle_data.get("plate") or record.get("plate"),
                        "timestamp": record.get("timestamp"),
                        "latitude": record.get("latitude"),
                        "longitude": record.get("longitude"),
                        "speed": record.get("speed"),
                        "odometer": record.get("odometer"),
                        "ignition": _format_ignition(record.get("ignition")),
                        "address": record.get("address"),
                        "fuel_level": record.get("fuel_level"),
                        "rpm": record.get("rpm"),
                        "battery_voltage": record.get("battery_voltage"),
                        "engine_hours": record.get("engine_hours"),
                        "driver": record.get("driver"),
                    }
                    all_records.append(_fill_nd(clean_record))

            if not all_records:
                logger.warning("Nenhum registro encontrado no histórico consolidado")
                return ""

            # Cria DataFrame
            df = pd.DataFrame(all_records)

            # Ordena por vehicle_id e timestamp
            df = df.sort_values(["vehicle_id", "timestamp"])

            # Adiciona metadados
            df = self._add_metadata_to_dataframe(df, system_source)

            # Define caminho de saída
            if output_path:
                file_path = Path(output_path)
            else:
                month_dir = self._create_month_directory(month, year, account_name)
                filename = self._generate_filename(
                    "Histórico_Consolidado", extension="xlsx"
                )
                file_path = month_dir / filename

            # Garante que o diretório existe
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Traduz colunas para português
            df = self._translate_columns(df)

            # Exporta para Excel
            df.to_excel(file_path, index=False, engine="openpyxl")

            logger.success(
                f"{len(all_records)} registros consolidados de "
                f"{len(all_history)} veículos ({month:02d}/{year}) exportados para: {file_path}"
            )
            return str(file_path)

        except Exception as e:
            logger.error(f"Erro ao exportar histórico consolidado para Excel: {e}")
            raise

    def get_export_stats(self, month: int, year: int) -> Dict[str, Any]:
        """
        Retorna estatísticas sobre os arquivos exportados para um mês/ano.

        Args:
            month: Mês (1-12)
            year: Ano

        Returns:
            Dicionário com estatísticas dos arquivos exportados
        """
        month_dir = self.base_export_dir / f"{year}-{month:02d}"

        if not month_dir.exists():
            return {
                "month": month,
                "year": year,
                "directory": str(month_dir),
                "exists": False,
                "total_files": 0,
                "csv_files": 0,
                "excel_files": 0,
                "total_size_mb": 0.0,
            }

        csv_files = list(month_dir.glob("*.csv"))
        excel_files = list(month_dir.glob("*.xlsx"))
        all_files = csv_files + excel_files

        total_size = sum(f.stat().st_size for f in all_files)
        total_size_mb = total_size / (1024 * 1024)

        return {
            "month": month,
            "year": year,
            "directory": str(month_dir),
            "exists": True,
            "total_files": len(all_files),
            "csv_files": len(csv_files),
            "excel_files": len(excel_files),
            "total_size_mb": round(total_size_mb, 2),
        }
