import uvicorn
from src.bootstrap import App

app = App()
fastapi_app = app.create()


if __name__ == '__main__':
    uvicorn.run(
        app='main:fastapi_app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        access_log=True,
    )
