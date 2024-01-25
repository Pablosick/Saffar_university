from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from api.handlers import user_router


# Создание экземпляра приложения
app = FastAPI(title="Saffar_university")


# Главный роутер, который будет собирать в себе остальные роутеры
main_router = APIRouter()
main_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
