import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from base_module import (
    custom_openapi,
    exception_handler,
    setup_logging,
    get_app_version
)
# from app.config import config
# from app.injectors import services
from routers import api_router
from base_async.services import TracingService

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

    app.state.background_tasks = []

    yield
    # Закрываем все фоновые задачи при завершении работы приложения
    for task in app.state.background_tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


def setup_app():
    app = FastAPI(
        title='RealTimeTranslator',
        lifespan=lifespan,
        openapi_url=f'/api/v1/openapi.json',
        docs_url='/docs',
    )
    setup_logging(app, default_level=10)
    TracingService.setup_fastapi_tracing(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    custom_openapi(
        app,
        title='RealTimeTranslator Backend',
        version=get_app_version(),
        description='Бэкенд сервис RealTimeTranslator',
    )
    exception_handler(app)


    return app

app = setup_app()
app.include_router(api_router, prefix='/api/v1')

def main() -> None:
    uvicorn.run(
        app,
        host='127.0.0.1',
        port=8024,
        log_config=None,
    )


if __name__ == '__main__':
    main()