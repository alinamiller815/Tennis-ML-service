from abc import ABC, abstractmethod
from core.entities.model import Model

class ModelRepository(ABC):
    @abstractmethod
    def get_model_by_id(self, model_id = int):
        pass
    @abstractmethod
    def save_model(self, model: Model) -> None:
        pass
    @abstractmethod
    def update_model(self, model: Model) -> None:
        pass
    @abstractmethod
    def get_all_models(self) -> list[Model]:
        pass
    @abstractmethod
    def get_model_by_name(self, name: str) -> Model:
        pass