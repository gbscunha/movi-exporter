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
from statistics import median
from typing import Any, Callable, Dict, List, Optional

from src.clients.protocols import TrackingClient
from src.clients.wialon_client import WialonClient, WialonError
from src.core.config import settings
from src.core.logger import logger
from src.services.exporter import DataExporter
from src.services.normalizer import DataNormalizer
from src.services.uploader import DriveUploader, UploadResult
from src.services.wialon_transformer import WialonTransformer

# Limiares (V) para detectar tensão do veículo e bateria interna trocadas no
# cadastro Wialon: bateria interna lendo acima de VOLTAGE_SWAP_HIGH_V e tensão
# do veículo abaixo de VOLTAGE_SWAP_LOW_V é o padrão claro de inversão. A folga
# entre os dois evita falso-positivo do caso legítimo "tensão do veículo = 0".
VOLTAGE_SWAP_HIGH_V = 10
VOLTAGE_SWAP_LOW_V = 6


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

    def __init__(
        self,
        client: Optional[TrackingClient] = None,
        normalizer: Optional[DataNormalizer] = None,
        exporter: Optional[DataExporter] = None,
        export_dir: Optional[str] = None,
        transformer: Optional[WialonTransformer] = None,
    ):
        """
        Inicializa o serviço.

        Args:
            client: Cliente de rastreamento (cria WialonClient se não fornecido)
            normalizer: Normalizador de dados (cria um novo se não fornecido)
            exporter: Exportador de dados (cria um novo se não fornecido)
            export_dir: Diretório de exportação (usa settings se não fornecido)
            transformer: Transformer de mensagens (cria WialonTransformer se não fornecido)
        """
        self.client: TrackingClient = client or WialonClient()
        self.normalizer = normalizer or DataNormalizer()

        export_path = export_dir or settings.EXPORT_DIR
        self.exporter = exporter or DataExporter(base_export_dir=export_path)

        # Transformer para converter mensagens do sistema de rastreamento
        self.transformer = transformer or WialonTransformer(self.client)

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
            last_pwr_ext: Optional[float] = None
            last_ignition: Optional[bool] = None

            page_size = settings.WIALON_PAGE_SIZE or 1000
            for page in self.client.get_history(
                vehicle_id, time_from, time_to, page_size=page_size
            ):
                for message in page:
                    params = message.get("p", {}) or {}
                    if "pwr_ext" in params:
                        last_pwr_ext = params["pwr_ext"]

                    transformed = self.transformer.transform_message(
                        message, vehicle_id, sensor_map
                    )
                    if transformed is None:
                        continue

                    # Propaga pwr_ext mais recente para registros GPS sem leitura própria.
                    # `pwr_ext` é tensão do veículo (12-28V). Bateria interna do tracker
                    # (`pwr_int`, ~4V) vem em quase toda mensagem — sem necessidade de propagar.
                    if (
                        transformed.get("vehicle_voltage") is None
                        and last_pwr_ext is not None
                    ):
                        transformed["vehicle_voltage"] = last_pwr_ext

                    # Carry-forward de ignição: o painel Wialon mantém o último
                    # estado conhecido entre mensagens sem sinal de ignição.
                    # Sem isso, marcávamos "Desligado" em mensagens que apenas
                    # não repetem o sinal (ex.: Suntech model 170 alterna STT
                    # com `mode` e ALT só com evento `alert_id`).
                    ignition = transformed.get("ignition")
                    if ignition is None:
                        transformed["ignition"] = last_ignition
                    else:
                        last_ignition = ignition

                    all_records.append(transformed)

                stats.total_messages += len(page)

            # Sanity-check de tensão (não-destrutivo): em alguns veículos o
            # cadastro de sensores na Wialon troca "tensão do veículo" com
            # "bateria interna". NÃO alteramos o dado (é fiel à fonte), apenas
            # avisamos no log para o cliente corrigir o cadastro na Wialon.
            self._warn_if_voltages_swapped(vehicle_name, all_records)

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

    @staticmethod
    def _warn_if_voltages_swapped(
        vehicle_name: str, records: List[Dict[str, Any]]
    ) -> bool:
        """Avisa (sem alterar dado) se tensão do veículo e bateria interna
        parecem trocadas no cadastro Wialon.

        Padrão claro de inversão: a "bateria interna" lê como tensão de veículo
        (>10V) e a "tensão do veículo" lê como bateria interna (<6V). O limiar
        evita falso-positivo do caso legítimo "tensão do veículo = 0".

        Returns:
            True se emitiu o aviso (usado nos testes).
        """
        veic = [
            r["vehicle_voltage"]
            for r in records
            if isinstance(r.get("vehicle_voltage"), (int, float))
        ]
        intern = [
            r["internal_battery_voltage"]
            for r in records
            if isinstance(r.get("internal_battery_voltage"), (int, float))
        ]
        if not veic or not intern:
            return False

        med_veic = median(veic)
        med_intern = median(intern)
        if med_intern > VOLTAGE_SWAP_HIGH_V and med_veic < VOLTAGE_SWAP_LOW_V:
            logger.warning(
                f"{vehicle_name}: tensão do veículo (~{med_veic:.1f}V) menor que "
                f"a bateria interna (~{med_intern:.1f}V) — provável sensor trocado "
                f"no cadastro da Wialon. Dado exportado como está (fiel à fonte)."
            )
            return True
        return False

    def export_monthly_data(
        self,
        month: int,
        year: int,
        vehicle_ids: Optional[List[int]] = None,
        export_format: str = "csv",
        consolidated: bool = True,
        upload_to_drive: bool = False,
        account_name: Optional[str] = None,
        on_progress: Optional[Callable[[int, int, str], None]] = None,
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
            account_name: Se fornecido, exports vão para subpasta `YYYY-MM/<name>/`
                          em vez de `YYYY-MM/` — útil quando há mais de uma conta
                          Wialon configurada.
            on_progress: Callback opcional `(atual, total, nome_veiculo)` chamado
                         ao iniciar o processamento de cada veículo — usado pela
                         GUI para mostrar progresso real (barra determinada).

        Returns:
            Resultado da exportação com estatísticas
        """
        result = ExportResult(month=month, year=year)

        logger.info("═══════════════════════════════════════════════════════════")
        logger.info(f"Iniciando exportação mensal: {month:02d}/{year}")
        logger.info("═══════════════════════════════════════════════════════════")

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

            # Wialon é fonte não-confiável: registration_plate é texto livre,
            # podendo vir vazio, com typo ou DUPLICADO/trocado entre unidades.
            # Como o nome do arquivo é a placa, duas unidades com a mesma placa
            # gerariam arquivos de mesmo nome — risco de sobrescrita silenciosa
            # (e foi o que ocorreu em produção: TEP0B26 saiu como SYN3D86).
            # Mapeia placas repetidas no lote para desambiguar o arquivo via ID.
            plate_counts: Dict[str, int] = {}
            for v in vehicles:
                plate = (v.get("_plate") or "").strip()
                if plate:
                    plate_counts[plate] = plate_counts.get(plate, 0) + 1
            duplicated_plates = {p for p, c in plate_counts.items() if c > 1}

            # Processa cada veículo
            all_history: Dict[str, List[Dict[str, Any]]] = {}
            vehicles_info: Dict[str, Dict[str, str]] = {}  # Para exportação consolidada

            for index, vehicle in enumerate(vehicles, start=1):
                vehicle_id = vehicle.get("id")
                vehicle_name = vehicle.get("nm", f"Veículo {vehicle_id}")
                vehicle_plate = (
                    vehicle.get("_plate") or ""
                ).strip()  # Placa extraída do profile field

                # Placa usada SÓ no nome do arquivo. Em caso de placa duplicada
                # na conta, anexa o ID para manter o arquivo único e rastreável.
                # O consolidado mantém a placa original (fidelidade ao dado).
                plate_for_file = vehicle_plate
                if vehicle_plate and vehicle_plate in duplicated_plates:
                    plate_for_file = f"{vehicle_plate}_{vehicle_id}"
                    logger.warning(
                        f"Placa '{vehicle_plate}' duplicada na conta Wialon — "
                        f"anexando ID {vehicle_id} ao arquivo do veículo "
                        f"'{vehicle_name}' para evitar sobrescrita."
                    )

                # Notifica a GUI do progresso (veículo atual / total).
                if on_progress is not None:
                    on_progress(index, result.total_vehicles, vehicle_name)

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
                            vehicle_plate=plate_for_file,
                            account_name=account_name,
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
                            vehicle_plate=plate_for_file,
                            account_name=account_name,
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

            # Exporta consolidado — SEMPRE em CSV, independente do formato
            # escolhido para os arquivos individuais. O consolidado junta todos
            # os veículos num único arquivo, que facilmente passa do limite de
            # 1.048.576 linhas do Excel (.xlsx) — uma frota grande estoura esse
            # teto e o xlsx falha. CSV não tem limite e é o formato adequado
            # para um dataset desse porte (análise/BI).
            if consolidated and all_history:
                logger.info("Gerando arquivo consolidado (CSV)...")
                if export_format == "xlsx":
                    logger.info(
                        "Obs: o consolidado é gerado em CSV mesmo com formato "
                        "Excel selecionado — o Excel não suporta mais de ~1 "
                        "milhão de linhas, e o consolidado da frota costuma "
                        "passar disso. Os arquivos por veículo seguem em xlsx."
                    )
                file_path = self.exporter.export_consolidated_history_to_csv(
                    all_history,
                    month,
                    year,
                    vehicles_info=vehicles_info,
                    account_name=account_name,
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
            logger.info("═══════════════════════════════════════════════════════════")
            logger.info(f"Exportação concluída: {month:02d}/{year}")
            logger.info(
                f"  Veículos processados: {result.processed_vehicles}/{result.total_vehicles}"
            )
            logger.info(f"  Veículos com erro: {result.failed_vehicles}")
            logger.info(f"  Total de registros: {result.total_records}")
            logger.info(f"  Arquivos gerados: {len(result.exported_files)}")
            logger.info(f"  Taxa de sucesso: {result.success_rate:.1f}%")
            logger.info("═══════════════════════════════════════════════════════════")

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
            except Exception as e:
                logger.debug(f"Erro: {e}")

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
