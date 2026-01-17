"""
Serviço de orquestração para extração de dados de veículos.

Coordena o fluxo completo:
1. Listagem de veículos
2. Resolução de sensores
3. Busca de histórico mensal paginado
4. Transformação de dados brutos para formato intermediário
5. Normalização via DataNormalizer
6. Exportação via DataExporter

Este serviço NÃO contém lógica específica de Wialon no normalizer/exporter.
A transformação de dados brutos acontece aqui, antes da normalização.
"""

import calendar
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.clients.wialon_client import WialonClient, WialonError
from src.core.config import settings
from src.core.logger import logger
from src.services.exporter import DataExporter
from src.services.normalizer import DataNormalizer
from src.services.uploader import DriveUploader, UploadResult


@dataclass
class VehicleStats:
    """Estatísticas de processamento de um veículo."""

    vehicle_id: int
    vehicle_name: str
    total_messages: int = 0
    exported_records: int = 0
    errors: List[str] = field(default_factory=list)
    success: bool = True


@dataclass
class ExportResult:
    """Resultado da exportação mensal."""

    month: int
    year: int
    total_vehicles: int = 0
    processed_vehicles: int = 0
    failed_vehicles: int = 0
    total_records: int = 0
    vehicle_stats: List[VehicleStats] = field(default_factory=list)
    exported_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    upload_result: Optional[UploadResult] = None

    @property
    def success_rate(self) -> float:
        """Taxa de sucesso do processamento."""
        if self.total_vehicles == 0:
            return 0.0
        return (self.processed_vehicles / self.total_vehicles) * 100


class VehicleService:
    """
    Serviço principal de extração e exportação de dados de veículos.

    Orquestra o fluxo completo desde a API até os arquivos exportados.
    """

    # Parâmetros conhecidos para busca direta nas mensagens
    # Mapeamento: campo normalizado -> lista de parâmetros possíveis na API
    KNOWN_PARAMS = {
        "ignition": ["in", "in1", "din1", "ignition", "ign"],
        "fuel_level": ["fuel1", "fuel2", "fuel_level", "can_fuel_level", "fuel", "fls"],
        "rpm": ["rpm", "can_rpm", "engine_rpm", "eng_rpm"],
        "battery_voltage": [
            "pwr_ext",
            "pwr_int",
            "voltage",
            "battery",
            "power",
            "batt",
        ],
        "engine_hours": ["engine_hours", "eng_hours", "horimeter", "eh", "mh"],
    }

    def __init__(
        self,
        client: Optional[WialonClient] = None,
        normalizer: Optional[DataNormalizer] = None,
        exporter: Optional[DataExporter] = None,
        export_dir: Optional[str] = None,
    ):
        """
        Inicializa o serviço.

        Args:
            client: Cliente Wialon (cria um novo se não fornecido)
            normalizer: Normalizador de dados (cria um novo se não fornecido)
            exporter: Exportador de dados (cria um novo se não fornecido)
            export_dir: Diretório de exportação (usa settings se não fornecido)
        """
        self.client = client or WialonClient()
        self.normalizer = normalizer or DataNormalizer()

        export_path = export_dir or settings.EXPORT_DIR
        self.exporter = exporter or DataExporter(base_export_dir=export_path)

        # Cache de sensores por veículo para evitar requisições repetidas
        # Formato: {vehicle_id: {param_base: {"name": str, "formula": str}}}
        self._sensor_cache: Dict[int, Dict[str, Dict[str, Any]]] = {}

        logger.info("VehicleService inicializado")

    def get_month_timestamps(self, month: int, year: int) -> tuple[int, int]:
        """
        Retorna timestamps Unix de início e fim do mês.

        Args:
            month: Mês (1-12)
            year: Ano

        Returns:
            Tupla (timestamp_inicio, timestamp_fim)
        """
        # Primeiro dia do mês às 00:00:00
        start_date = datetime(year, month, 1, 0, 0, 0)

        # Último dia do mês às 23:59:59
        last_day = calendar.monthrange(year, month)[1]
        end_date = datetime(year, month, last_day, 23, 59, 59)

        return int(start_date.timestamp()), int(end_date.timestamp())

    def get_vehicle_sensors(self, vehicle_id: int) -> Dict[str, Dict[str, Any]]:
        """
        Obtém mapa de sensores com cache.

        Args:
            vehicle_id: ID do veículo

        Returns:
            Mapa de parâmetro base -> info do sensor
            Exemplo: {"io_2_94": {"name": "rpm", "formula": "io_2_94*const0.25"}}
        """
        if vehicle_id not in self._sensor_cache:
            self._sensor_cache[vehicle_id] = self.client.get_vehicle_sensors(vehicle_id)
        return self._sensor_cache[vehicle_id]

    def transform_wialon_message(
        self,
        message: Dict[str, Any],
        vehicle_id: int,
        sensor_map: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Transforma mensagem bruta da Wialon para formato intermediário.

        Esta é a única função que conhece a estrutura da Wialon.
        O resultado é um dicionário com campos padronizados.

        Busca dados de duas formas:
        1. Via sensor_map (sensores configurados no Wialon, com fórmulas)
        2. Via KNOWN_PARAMS (parâmetros conhecidos diretamente nas mensagens)

        Args:
            message: Mensagem bruta da API Wialon
            vehicle_id: ID do veículo
            sensor_map: Mapa de sensores do veículo
                        Formato: {param_base: {"name": str, "formula": str}}

        Returns:
            Dicionário com dados transformados
        """
        # Extrai posição
        pos = message.get("pos", {}) or {}

        # Extrai parâmetros (dados de sensores)
        params = message.get("p", {}) or {}

        # Resolve sensores para valores conhecidos via sensor_map
        ignition = None
        fuel_level = None
        rpm = None
        battery_voltage = None
        engine_hours = None

        for param_key, param_value in params.items():
            sensor_info = sensor_map.get(param_key)

            if not sensor_info:
                continue

            sensor_name = sensor_info.get("name", "")
            formula = sensor_info.get("formula", "")

            # Aplica a fórmula do sensor ao valor bruto
            calculated_value = self.client.apply_sensor_formula(param_value, formula)

            if sensor_name == "ignition":
                # Ignição: 0 = desligado, 1 = ligado
                ignition = bool(param_value) if param_value is not None else None
            elif sensor_name == "fuel_level":
                fuel_level = (
                    calculated_value if calculated_value is not None else param_value
                )
            elif sensor_name == "rpm":
                rpm = calculated_value if calculated_value is not None else param_value
            elif sensor_name == "battery_voltage":
                battery_voltage = (
                    calculated_value if calculated_value is not None else param_value
                )
            elif sensor_name == "engine_hours":
                engine_hours = (
                    calculated_value if calculated_value is not None else param_value
                )

        # Busca direta de parâmetros conhecidos (fallback quando não há sensor configurado)
        # Ignição
        if ignition is None:
            for key in self.KNOWN_PARAMS["ignition"]:
                if key in params and params[key] is not None:
                    ignition = bool(params[key])
                    break

        # Nível de combustível
        if fuel_level is None:
            for key in self.KNOWN_PARAMS["fuel_level"]:
                if key in params and params[key] is not None:
                    fuel_level = params[key]
                    break

        # RPM
        if rpm is None:
            for key in self.KNOWN_PARAMS["rpm"]:
                if key in params and params[key] is not None:
                    rpm = params[key]
                    break

        # Voltagem da bateria
        if battery_voltage is None:
            for key in self.KNOWN_PARAMS["battery_voltage"]:
                if key in params and params[key] is not None:
                    battery_voltage = params[key]
                    break

        # Horas do motor
        if engine_hours is None:
            for key in self.KNOWN_PARAMS["engine_hours"]:
                if key in params and params[key] is not None:
                    engine_hours = params[key]
                    break

        # Monta registro transformado
        transformed = {
            "vehicle_id": vehicle_id,
            "timestamp": message.get("t"),  # Unix timestamp
            "latitude": pos.get("y"),
            "longitude": pos.get("x"),
            "speed": pos.get("s") or pos.get("sp"),  # Velocidade
            "odometer": None,  # Wialon não retorna odômetro direto nas mensagens
            "ignition": ignition,
            "fuel_level": fuel_level,
            "rpm": rpm,
            "battery_voltage": battery_voltage,
            "engine_hours": engine_hours,
            "driver": message.get("drv"),  # Motorista vinculado
            "address": None,  # Requer geocodificação reversa (não implementado)
            "raw_data": message,  # Preserva dados originais
        }

        return transformed

    def process_vehicle_history(
        self,
        vehicle: Dict[str, Any],
        month: int,
        year: int,
    ) -> tuple[List[Dict[str, Any]], VehicleStats]:
        """
        Processa histórico completo de um veículo para o mês.

        Args:
            vehicle: Dados do veículo (id, nm)
            month: Mês
            year: Ano

        Returns:
            Tupla (lista de registros transformados, estatísticas)
        """
        vehicle_id = vehicle.get("id")
        vehicle_name = vehicle.get("nm", f"Veículo {vehicle_id}")

        stats = VehicleStats(vehicle_id=vehicle_id, vehicle_name=vehicle_name)

        logger.info(f"Processando veículo: {vehicle_name} (ID: {vehicle_id})")

        try:
            # Obtém mapa de sensores (com cache)
            sensor_map = self.get_vehicle_sensors(vehicle_id)

            # Obtém timestamps do mês
            time_from, time_to = self.get_month_timestamps(month, year)

            # Processa histórico em páginas
            all_records = []

            for page in self.client.get_history(vehicle_id, time_from, time_to):
                for message in page:
                    transformed = self.transform_wialon_message(
                        message, vehicle_id, sensor_map
                    )
                    all_records.append(transformed)

                stats.total_messages += len(page)

            logger.success(
                f"Veículo {vehicle_name}: {stats.total_messages} mensagens processadas"
            )

            return all_records, stats

        except WialonError as e:
            error_msg = f"Erro ao processar veículo {vehicle_name}: {e}"
            logger.error(error_msg)
            stats.errors.append(error_msg)
            stats.success = False
            return [], stats

    def export_monthly_data(
        self,
        month: int,
        year: int,
        vehicle_ids: Optional[List[int]] = None,
        export_format: str = "csv",
        consolidated: bool = True,
        upload_to_drive: bool = False,
    ) -> ExportResult:
        """
        Exporta dados mensais de todos os veículos (ou lista específica).

        Args:
            month: Mês (1-12)
            year: Ano
            vehicle_ids: Lista opcional de IDs de veículos a processar
            export_format: Formato de exportação ("csv", "xlsx", ou "both")
            consolidated: Se True, gera arquivo consolidado além dos individuais
            upload_to_drive: Se True, faz upload dos arquivos para o Google Drive

        Returns:
            Resultado da exportação com estatísticas
        """
        result = ExportResult(month=month, year=year)

        logger.info(f"═══════════════════════════════════════════════════════════")
        logger.info(f"Iniciando exportação mensal: {month:02d}/{year}")
        logger.info(f"═══════════════════════════════════════════════════════════")

        try:
            # Autentica
            self.client.authenticate()

            # Lista veículos
            vehicles = self.client.list_vehicles()

            # Filtra por IDs específicos se fornecido
            if vehicle_ids:
                vehicles = [v for v in vehicles if v.get("id") in vehicle_ids]
                logger.info(f"Filtrado para {len(vehicles)} veículos específicos")

            result.total_vehicles = len(vehicles)

            if not vehicles:
                logger.warning("Nenhum veículo encontrado para processar")
                return result

            # Processa cada veículo
            all_history: Dict[str, List[Dict[str, Any]]] = {}
            vehicles_info: Dict[str, Dict[str, str]] = {}  # Para exportação consolidada

            for vehicle in vehicles:
                vehicle_id = vehicle.get("id")
                vehicle_name = vehicle.get("nm", f"Veículo {vehicle_id}")
                vehicle_plate = (
                    vehicle.get("_plate") or ""
                )  # Placa extraída do profile field

                try:
                    # Processa histórico
                    records, stats = self.process_vehicle_history(vehicle, month, year)
                    result.vehicle_stats.append(stats)

                    if not stats.success:
                        result.failed_vehicles += 1
                        continue

                    if not records:
                        logger.warning(
                            f"Veículo {vehicle_name}: nenhum registro no período"
                        )
                        result.processed_vehicles += 1
                        continue

                    # Normaliza registros
                    normalized = self.normalizer.normalize_history(
                        records, system="wialon"
                    )
                    stats.exported_records = len(normalized)
                    result.total_records += len(normalized)

                    # Exporta arquivo individual
                    if export_format in ("csv", "both"):
                        file_path = self.exporter.export_history_to_csv(
                            normalized,
                            str(vehicle_id),
                            month,
                            year,
                            vehicle_name=vehicle_name,
                            vehicle_plate=vehicle_plate,
                        )
                        if file_path:
                            result.exported_files.append(file_path)

                    if export_format in ("xlsx", "both"):
                        file_path = self.exporter.export_history_to_excel(
                            normalized,
                            str(vehicle_id),
                            month,
                            year,
                            vehicle_name=vehicle_name,
                            vehicle_plate=vehicle_plate,
                        )
                        if file_path:
                            result.exported_files.append(file_path)

                    # Guarda para consolidado
                    if consolidated:
                        all_history[str(vehicle_id)] = normalized
                        vehicles_info[str(vehicle_id)] = {
                            "name": vehicle_name,
                            "plate": vehicle_plate,
                        }

                    result.processed_vehicles += 1

                except Exception as e:
                    error_msg = f"Erro inesperado no veículo {vehicle_name}: {e}"
                    logger.error(error_msg)
                    result.errors.append(error_msg)
                    result.failed_vehicles += 1

            # Exporta consolidado
            if consolidated and all_history:
                logger.info("Gerando arquivo consolidado...")

                if export_format in ("csv", "both"):
                    file_path = self.exporter.export_consolidated_history_to_csv(
                        all_history, month, year, vehicles_info=vehicles_info
                    )
                    if file_path:
                        result.exported_files.append(file_path)

                if export_format in ("xlsx", "both"):
                    file_path = self.exporter.export_consolidated_history_to_excel(
                        all_history, month, year, vehicles_info=vehicles_info
                    )
                    if file_path:
                        result.exported_files.append(file_path)

            # Upload para Google Drive
            if upload_to_drive and result.exported_files:
                logger.info("Iniciando upload para Google Drive...")
                try:
                    uploader = DriveUploader()
                    result.upload_result = uploader.upload_files(
                        file_paths=result.exported_files,
                        month=month,
                        year=year,
                        overwrite=True,
                    )
                except Exception as e:
                    error_msg = f"Erro no upload para Google Drive: {e}"
                    logger.error(error_msg)
                    result.errors.append(error_msg)

            # Log final
            logger.info(f"═══════════════════════════════════════════════════════════")
            logger.info(f"Exportação concluída: {month:02d}/{year}")
            logger.info(
                f"  Veículos processados: {result.processed_vehicles}/{result.total_vehicles}"
            )
            logger.info(f"  Veículos com erro: {result.failed_vehicles}")
            logger.info(f"  Total de registros: {result.total_records}")
            logger.info(f"  Arquivos gerados: {len(result.exported_files)}")
            logger.info(f"  Taxa de sucesso: {result.success_rate:.1f}%")
            logger.info(f"═══════════════════════════════════════════════════════════")

            return result

        except WialonError as e:
            error_msg = f"Erro crítico na exportação: {e}"
            logger.error(error_msg)
            result.errors.append(error_msg)
            return result

        finally:
            # Encerra sessão
            try:
                self.client.logout()
            except Exception:
                pass

    def list_vehicles(self) -> List[Dict[str, Any]]:
        """
        Lista todos os veículos disponíveis.

        Returns:
            Lista de veículos com id e nome
        """
        try:
            self.client.authenticate()
            vehicles = self.client.list_vehicles()

            # Simplifica para exibição
            simplified = []
            for v in vehicles:
                simplified.append(
                    {
                        "id": v.get("id"),
                        "name": v.get("nm"),
                        "plate": v.get("_plate")
                        or v.get(
                            "uid", ""
                        ),  # Placa do profile field ou UID como fallback
                        "brand": v.get("_brand", ""),
                        "model": v.get("_model", ""),
                    }
                )

            return simplified

        finally:
            self.client.logout()

    def test_connection(self) -> bool:
        """
        Testa conexão com a API Wialon.

        Returns:
            True se conexão bem-sucedida
        """
        try:
            self.client.authenticate()
            logger.success("Conexão com Wialon estabelecida com sucesso!")
            return True
        except WialonError as e:
            logger.error(f"Falha na conexão: {e}")
            return False
        finally:
            self.client.logout()
