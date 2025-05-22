#!/usr/bin/env python3
"""
Скрипт для создания и инициализации базы данных.
"""
import os
import sys
import argparse
import logging
import hashlib

# Настраиваем логгирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("db_init")

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем необходимые модули
try:
    from config.database import engine, get_session
    from infra.db.models import Base, UserDB
    logger.info("Модули успешно импортированы")
except ImportError as e:
    logger.error(f"Ошибка импорта: {e}")
    sys.exit(1)

def create_tables():
    """Создает все таблицы в базе данных."""
    logger.info("Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    logger.info("Таблицы успешно созданы")

def add_test_users():
    """Добавляет тестовых пользователей, если они не существуют."""
    
    # Данные тестовых пользователей
    test_users = [
        {
            "email": "test@example.com", 
            "name": "Test User", 
            "password": "password123", 
            "balance": 100.0,
            "is_admin": False
        },
        {
            "email": "admin@example.com", 
            "name": "Administrator", 
            "password": "admin123", 
            "balance": 1000.0,
            "is_admin": True
        }
    ]
    
    from sqlalchemy.orm import Session
    
    with Session(engine) as session:
        for user_data in test_users:
            # Проверяем, существует ли пользователь
            existing_user = session.query(UserDB).filter(UserDB.email == user_data["email"]).first()
            
            if not existing_user:
                # Хешируем пароль
                hashed_password = hashlib.sha256(user_data["password"].encode('utf-8')).hexdigest()
                
                # Создаем нового пользователя
                user = UserDB(
                    email=user_data["email"],
                    name=user_data["name"],
                    hashed_password=hashed_password,
                    balance=user_data["balance"]
                )
                
                # Если есть поле is_admin, добавляем его
                if hasattr(UserDB, 'is_admin'):
                    user.is_admin = user_data["is_admin"]
                
                session.add(user)
                logger.info(f"Пользователь {user_data['email']} успешно создан")
            else:
                logger.info(f"Пользователь {user_data['email']} уже существует")
        
        # Сохраняем изменения
        session.commit()

def check_tables():
    """Проверяет, какие таблицы есть в базе данных."""
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    logger.info(f"Таблицы в базе данных: {tables}")
    
    for table in tables:
        columns = inspector.get_columns(table)
        column_names = [col['name'] for col in columns]
        logger.info(f"Таблица '{table}' имеет столбцы: {column_names}")

def main():
    """Основная функция скрипта."""
    parser = argparse.ArgumentParser(description="Инициализация базы данных")
    
    # Добавляем параметры командной строки
    parser.add_argument('--create', action='store_true', help='Создать таблицы')
    parser.add_argument('--add-users', action='store_true', help='Добавить тестовых пользователей')
    parser.add_argument('--check-tables', action='store_true', help='Проверить таблицы в базе данных')
    
    args = parser.parse_args()
    
    # Если нет аргументов, выводим справку
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # Выполняем соответствующие действия
    if args.create:
        create_tables()
    
    if args.add_users:
        add_test_users()
    
    if args.check_tables:
        check_tables()
    
    logger.info("Операции с базой данных завершены")

if __name__ == "__main__":
    main()