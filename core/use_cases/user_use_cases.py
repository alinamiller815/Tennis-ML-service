from core.entities.user import User
from core.entities.prediction import Prediction
from core.entities.model import Model
from core.repositories.user_repository import UserRepository
from core.repositories.prediction_repository import PredictionRepository
from core.repositories.model_repository import ModelRepository
import hashlib

class UserUseCases:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, email: str, name: str, password: str) -> User:
        # Отладочный вывод
        print(f"Регистрация пользователя: email={email}, name={name}")
        # Проверяем, нет ли уже пользователя с таким email
        existing_user = self.user_repository.get_user_by_email(email)
        if existing_user:
            raise ValueError("Пользователь с таким email уже существует")

        # Хешируем пароль (в реальном приложении используйте bcrypt или другие безопасные методы)
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Начальный баланс для одного предсказания
        initial_balance = 10.0  # Здесь указываем желаемое количество баллов
        
        new_user = User(
                email=email,
                name=name,
                hashed_password=hashed_password,
                balance=initial_balance,
                ident=1
            )
        
        
        # Еще отладка
        print(f"Созданный объект User: email={new_user.email}, name={new_user.name}")
        # user_repo.create_user(new_user)
        # Сохраняем пользователя
        self.user_repository.save_user(new_user)

        # Еще отладка
        print(f"Созданный объект User: email={new_user.email}, name={new_user.name} сохранен")

        return new_user

    def auth_user(self, email: str, password: str):
        print(f"Попытка авторизации: email={email}")
        user = self.user_repository.get_user_by_email(email)
        if not user:
            print(f"Пользователь с email {email} не найден")
            return None
        print(f"Найден пользователь: id={user.id}, email={user.email}, name={user.name}")
        # Хешируем введенный пароль и сравниваем с сохраненным
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        print(f"Хеш введенного пароля: {hashed_password}")
        print(f"Хеш сохраненного пароля: {user.hashed_password}")
        if user.hashed_password != hashed_password:
            print("Пароли не совпадают")
            return None
        print("Авторизация успешна")
        return user
    
    def add_funds(self, user_id: int, amount: float) -> User:
        """Пополнение баланса пользователя"""
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        
        user.add_balance(amount)
        self.user_repository.update_user(user)
        
        return user
    
    

    
