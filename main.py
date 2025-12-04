import uvicorn
from config import settings, logger
from src.bootstrap.app import create_app

app = create_app()


if __name__ == '__main__':
    logger.info(f'Starting Auth Service on {settings.HOST}:{settings.PORT}')
    uvicorn.run(
        app='main:app',
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,  # Auto-reload в development
        access_log=False,  # Отключаем access log (логируем через logger)
    )
