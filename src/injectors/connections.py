import typing as t

from base_module import FastAPILoggerAdapter
from base_async.base_module import PgConfig
from base_async.injectors import AsyncPgConnectionInj
from config import config


class ConnectionsInjector:
    """Инъектор подключений для управления соединениями с БД"""

    def __init__(
            self,
            pg_config: PgConfig,
            pg_init_statements: t.List[str] | None = None
    ) -> None:
        self._pg_config = pg_config
        self._pg_init_statements = pg_init_statements or []
        self._pg_connection: AsyncPgConnectionInj | None = None
        self._logger = FastAPILoggerAdapter.create(self)
        self._is_setup = False

    @property
    def pg(self) -> AsyncPgConnectionInj:
        """Получение подключения к PostgreSQL."""
        if self._pg_connection is None:
            self._pg_connection = AsyncPgConnectionInj(conf=self._pg_config)
        return self._pg_connection

    async def setup(self) -> None:
        """Инициализация всех подключений."""
        await self.pg.setup()

    async def __aenter__(self) -> 'ConnectionsInjector':
        """Асинхронный контекстный менеджер - вход."""
        await self.setup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Асинхронный контекстный менеджер - выход."""
        await self.close_all(rollback=exc_type is not None, e=exc_val)

    async def close_all(
            self, rollback: bool = True, e: Exception | None = None
    ) -> None:
        """Закрытие всех подключений."""
        if self._pg_connection:
            try:
                await self._pg_connection.disconnect()
            except Exception as e:
                self._logger.warn(
                    f'Error closing PostgreSQL connection', extra={'e': e}
                )

        self._is_setup = False


