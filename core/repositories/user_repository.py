from abc import ABC, abstractmethod
from core.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass  
    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass
    @abstractmethod
    def save_user(self, user: User) -> None:
        pass
    @abstractmethod
    def update_user(self, user: User) -> None:
        pass
    
