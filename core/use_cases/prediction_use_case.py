

# from core.entities.user import User
from core.entities.prediction import Prediction
# from core.entities.model import Model
from core.repositories.user_repository import UserRepository
from core.repositories.prediction_repository import PredictionRepository
from core.repositories.model_repository import ModelRepository


import hashlib
import json

class PredictionUseCase:
    def __init__(self, 
                 prediction_repository: PredictionRepository,
                 user_repository: UserRepository,
                 model_repository: ModelRepository
                 ,tennis_predictor
                 ):
        self.prediction_repository = prediction_repository
        self.user_repository = user_repository
        self.model_repository = model_repository
        self.tennis_predictor = tennis_predictor

    def make_prediction(self, user_id: int, model_id: int, input_data: dict):
        # Проверки пользователя и модели
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        model = self.model_repository.get_model_by_id(model_id)
        if not model:
            raise ValueError("Модель не найдена")

        # Проверяем баланс пользователя
        if not user.deduct_balance(model.cost):
            raise ValueError(f"Недостаточно средств на балансе. Требуется: {model.cost}")
        
        # Обновляем баланс пользователя
        self.user_repository.update_user(user)

        # Преобразуем входные данные в json
        input_json = json.dumps(input_data)
        
        # Получаем предсказание от модели
        try:
            prediction_result = self.tennis_predictor.predict(model_id, input_data)
            output_json = json.dumps(prediction_result)
        except Exception as e:
            # Возвращаем средства в случае ошибки
            user.add_balance(model.cost)
            self.user_repository.update_user(user)
            raise ValueError(f"Ошибка при создании предсказания: {str(e)}")

        # Сохраняем предсказание
        prediction = Prediction(
            id=None,
            user_id=user_id,
            model_id=model_id,
            input_data=input_json,
            output_data=output_json
        )
        self.prediction_repository.save_prediction(prediction)

        return prediction
    
    def get_user_predictions(self, user_id: int):
        return self.prediction_repository.get_predictions_by_user_id(user_id)
    
    def get_prediction(self, prediction_id: int):
        return self.prediction_repository.get_predictions_by_id(prediction_id)