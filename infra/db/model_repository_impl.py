from core.repositories.model_repository import ModelRepository
from core.entities.model import Model
from sqlalchemy.orm import Session
from infra.db.models import ModelDB

class ModelRepositoryImpl(ModelRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_model_by_id(self, model_id: int):
        model_db = self.session.query(ModelDB).filter(ModelDB.id == model_id).first()
        if not model_db:
            return None
        return self._to_entity(model_db)
    
    def save_model(self, model: Model) -> None:
        model_db = ModelDB(
            id=model.id,
            name=model.name,
            cost=model.cost
        )
        self.session.add(model_db)
        self.session.commit()

    def update_model(self, model: Model) -> None:
        model_db = self.session.query(ModelDB).filter(ModelDB.id == model.id).first()
        if not model_db:
            raise ValueError("Model not found")
        
        model_db.name = model.name
        model_db.cost = model.cost
        self.session.commit()
    
    def get_all_models(self) -> list[Model]:
        models_db = self.session.query(ModelDB).all()
        return [self._to_entity(model_db) for model_db in models_db]

    def get_model_by_name(self, name: str) -> Model:
        model_db = self.session.query(ModelDB).filter(ModelDB.name == name).first()
        if not model_db:
            return None
        return self._to_entity(model_db)

    def _to_entity(self, model_db: ModelDB) -> Model:
        return Model(
            id=model_db.id,
            name=model_db.name,
            cost=model_db.cost
        )
    
