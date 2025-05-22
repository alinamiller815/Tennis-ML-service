from core.repositories.model_repository import ModelRepository
from core.entities.model import Model

class ModelUseCases:
    def __init__(self, model_repository: ModelRepository):
        self.model_repository = model_repository

    
    def create_model(self, name: str, cost: float)  -> Model:
        # Проверяем, нет ли уже модели с таким именем
        existing_model = self.model_repository.get_model_by_name(name)
        if existing_model:
            raise ValueError("Модель с таким именем уже существует")
        
        # Создаем новую модель
        model = Model(
            name=name,
            cost=cost
        )
        
        # Сохраняем модель
        self.model_repository.save_model(model)
        
        return model
    
    def get_available_models(self) -> list[Model]:
        return self.model_repository.get_all_models()
    
    def get_model(self, model_id: int,) ->  Model:
        return self.model_repository.get_model_by_id(model_id)