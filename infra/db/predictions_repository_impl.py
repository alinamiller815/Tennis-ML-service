from core.repositories.prediction_repository import PredictionRepository
from core.entities.prediction import Prediction
from sqlalchemy.orm import Session
from infra.db.models import PredictionDB


class PredictionRepositoryImpl(PredictionRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_predictions_by_user_id(self, user_id: int):
        prediction_db = self.session.query(PredictionDB).filter(PredictionDB.user_id == user_id).all()
        if not prediction_db:
            return []
        # Преобразуем каждое предсказание из БД в объект домена
        return [self._to_entity(pred_db) for pred_db in prediction_db]
    
    
    def get_prediction_by_id(self, id: int):
        prediction_db = self.session.query(PredictionDB).filter(PredictionDB.id == id).first()
        if not prediction_db:
            return None
        return self._to_entity(prediction_db)
    
    def save_prediction(self, prediction: Prediction):
        prediction_db = PredictionDB(
            id=prediction.id,
            user_id=prediction.user_id,
            model_id=prediction.model_id,
            input_data = prediction.input_data,
            output_data = prediction.output_data,
            created_at = prediction.created_at
        )
        self.session.add(prediction_db)
        self.session.commit()
    

    def _to_entity(self, prediction: PredictionDB) -> Prediction:
        return Prediction(
            id=prediction.id,
            user_id=prediction.user_id,
            model_id=prediction.model_id,
            input_data = prediction.input_data,
            output_data = prediction.output_data,
            created_at = prediction.created_at
        )