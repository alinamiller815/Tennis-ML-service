#!/usr/bin/env python3
"""
Скрипт для начисления баллов пользователям в системе прогнозирования матчей.
Может начислять баллы всем пользователям или только избранным по адресам почты.
"""

import os
import sys
import argparse
import logging
from sqlalchemy.orm import Session
from typing import List, Optional

# Добавляем родительскую директорию в путь импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем необходимые модули из нашего приложения
from config.database import engine
from infra.db.models import UserDB

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("credits_update.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("credits_updater")

def add_credits_to_all_users(amount: float = 50.0) -> None:
    """Начисляет баллы всем пользователям в системе"""
    with Session(engine) as session:
        try:
            # Получаем всех пользователей
            users = session.query(UserDB).all()
            
            if not users:
                logger.warning("Пользователи не найдены в системе")
                return
            
            logger.info(f"Начисление {amount} баллов всем пользователям ({len(users)} пользователей)")
            
            # Начисляем баллы каждому пользователю
            for user in users:
                old_balance = user.balance
                user.balance += amount
                logger.info(f"Пользователь {user.email}: баланс изменен с {old_balance} на {user.balance}")
            
            # Сохраняем изменения в БД
            session.commit()
            logger.info(f"Успешно начислены баллы {len(users)} пользователям")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка при начислении баллов: {str(e)}")

def add_credits_to_selected_users(emails: List[str], amount: float = 50.0) -> None:
    """Начисляет баллы только выбранным пользователям по их email"""
    with Session(engine) as session:
        try:
            # Счетчики для статистики
            updated_count = 0
            not_found_count = 0
            not_found_emails = []
            
            logger.info(f"Начисление {amount} баллов выбранным пользователям ({len(emails)} адресов)")
            
            # Обрабатываем каждый email
            for email in emails:
                # Ищем пользователя по email
                user = session.query(UserDB).filter(UserDB.email == email).first()
                
                if user:
                    old_balance = user.balance
                    user.balance += amount
                    updated_count += 1
                    logger.info(f"Пользователь {email}: баланс изменен с {old_balance} на {user.balance}")
                else:
                    not_found_count += 1
                    not_found_emails.append(email)
                    logger.warning(f"Пользователь с email {email} не найден")
            
            # Сохраняем изменения в БД
            session.commit()
            
            # Выводим статистику
            logger.info(f"Успешно начислены баллы {updated_count} пользователям")
            if not_found_count > 0:
                logger.warning(f"Не найдено {not_found_count} пользователей: {', '.join(not_found_emails)}")
                
        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка при начислении баллов: {str(e)}")

def main():
    """Основная функция скрипта"""
    parser = argparse.ArgumentParser(description="Начисление баллов пользователям системы прогнозирования матчей")
    
    # Группа для выбора пользователей
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all", 
        action="store_true", 
        help="Начислить баллы всем пользователям"
    )
    group.add_argument(
        "--emails", 
        type=str, 
        nargs="+", 
        help="Список email адресов пользователей для начисления баллов"
    )
    
    # Количество начисляемых баллов
    parser.add_argument(
        "--amount", 
        type=float, 
        default=50.0, 
        help="Количество начисляемых баллов (по умолчанию: 50.0)"
    )
    
    # Парсим аргументы
    args = parser.parse_args()
    
    # Начисляем баллы в зависимости от выбранного режима
    if args.all:
        add_credits_to_all_users(args.amount)
    else:
        add_credits_to_selected_users(args.emails, args.amount)

if __name__ == "__main__":
    main()