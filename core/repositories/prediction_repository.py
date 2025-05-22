from abc import ABC, abstractmethod
from core.entities.prediction import Prediction

class PredictionRepository(ABC):
    @abstractmethod
    def get_predictions_by_user_id(self, user_id: int) -> list[Prediction]:
        pass
    @abstractmethod
    def save_prediction(self, prediction: Prediction) -> Prediction:
        pass

    @abstractmethod
    def get_prediction_by_id(self, prediction_id: int) -> Prediction:
        pass
