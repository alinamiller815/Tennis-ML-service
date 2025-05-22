from core.repositories.user_repository import UserRepository
from core.entities.user import User
from sqlalchemy.orm import Session
from infra.db.models import UserDB 

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: int):
        # Добавьте отладку
        print(f"Поиск пользователя с ID: {user_id}")
        user_db = self.session.query(UserDB).filter(UserDB.id == user_id).first()
        if not user_db:
            print(f"Пользователь с ID {user_id} не найден в БД")
            return None
        
        # Проверяем метод _to_entity
        user = self._to_entity(user_db)
        print(f"Преобразован в объект User: id={user.id}, email={user.email}")
        return user
    
    def get_user_by_email(self, email: str):
        user_db = self.session.query(UserDB).filter(UserDB.email == email).first()
        if not user_db:
            return None
        return self._to_entity(user_db)
    
    def save_user(self, user: User) -> None:
        user_db = UserDB(
            id=user.id,
            email=user.email,
            name=user.name,
            hashed_password=user.hashed_password,
            balance=user.balance
        )
        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)

        user.id = user_db.id  # Эта строка очень важна!

    def update_user(self, user: User) -> None:
        # берем юзера
        user_db = self.session.query(UserDB).filter(UserDB.id == user.id).first()
        if not user_db:
            raise ValueError("User not found")
        # обновляем инфу по нему
        user_db.email = user.email
        user_db.hashed_password = user.hashed_password
        user_db.balance = user.balance
        self.session.commit()

    def _to_entity(self, user_db: UserDB) -> User:
        return User(
            id=user_db.id,
            email=user_db.email,
            name = user_db.name,
            hashed_password=user_db.hashed_password, 
            balance = user_db.balance,
            ident =  user_db.ident
        )


