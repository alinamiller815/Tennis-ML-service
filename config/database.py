import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение настроек из переменных окружения или использование значений по умолчанию
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tennis_predictions.db")

# Создание движка базы данных
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Получение новой сессии
def get_session():
    return SessionLocal()