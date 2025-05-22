import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from config.database import engine
from infra.db.models import Base

from infra.web.controllers.user_controller import router as user_router
from infra.web.controllers.model_controller import router as model_router
from infra.web.controllers.prediction_controller_old import router as prediction_router

# Создание директории для моделей, если она отсутствует
os.makedirs(settings.MODEL_DIR, exist_ok=True)

# Создание таблиц в базе данных (если их нет)
Base.metadata.create_all(bind=engine)

# Создание экземпляра приложения FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Сервис для прогнозирования исходов теннисных матчей",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(user_router)
app.include_router(model_router)
app.include_router(prediction_router)

# Корневой эндпоинт
@app.get("/")
def read_root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)