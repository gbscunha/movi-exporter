"""
Configuração de logging usando loguru.

Inclui handler customizado para integração com a GUI.
"""

from typing import Callable, Optional
from loguru import logger

# Handler para arquivo (rotação a 1 MB)
logger.add("app.log", rotation="1 MB")


class GUILogHandler:
    """
    Handler de logs para redirecionar mensagens do loguru para a GUI.

    Thread-safe: usa callback que deve ser chamado na thread principal da GUI.

    Uso:
        handler = GUILogHandler(callback=lambda msg, level: ...)
        handler_id = handler.register()
        # ... operações com logging ...
        handler.unregister()
    """

    # Mapeamento de níveis para ícones
    LEVEL_ICONS = {
        "DEBUG": "🔍",
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "CRITICAL": "🔥",
    }

    def __init__(self, callback: Callable[[str, str], None], min_level: str = "INFO"):
        """
        Inicializa o handler.

        Args:
            callback: Função chamada com (mensagem, nível) para cada log.
                      Deve ser thread-safe (ex: usar widget.after() no tkinter).
            min_level: Nível mínimo de log a capturar (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self._callback = callback
        self._min_level = min_level
        self._handler_id: Optional[int] = None

    def _sink(self, message):
        """Sink do loguru que repassa para o callback."""
        record = message.record
        level = record["level"].name

        # Formata mensagem com ícone
        icon = self.LEVEL_ICONS.get(level, "")
        text = record["message"]

        # Adiciona prefixo de ícone se não tiver
        if icon and not any(text.startswith(i) for i in self.LEVEL_ICONS.values()):
            formatted = f"{icon} {text}"
        else:
            formatted = text

        # Chama callback
        self._callback(formatted, level)

    def register(self) -> int:
        """
        Registra o handler no loguru.

        Returns:
            ID do handler para remoção posterior
        """
        self._handler_id = logger.add(
            self._sink,
            level=self._min_level,
            format="{message}",  # Formato simples, só a mensagem
            filter=lambda record: True,  # Aceita todos após filtro de nível
        )
        return self._handler_id

    def unregister(self):
        """Remove o handler do loguru."""
        if self._handler_id is not None:
            try:
                logger.remove(self._handler_id)
            except ValueError:
                pass  # Handler já removido
            self._handler_id = None

    def __enter__(self):
        """Context manager: registra ao entrar."""
        self.register()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager: remove ao sair."""
        self.unregister()
        return False
