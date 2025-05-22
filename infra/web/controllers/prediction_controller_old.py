from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


from config.database import get_session
from core.use_cases.prediction_use_case import PredictionUseCase
from infra.db.predictions_repository_impl import PredictionRepositoryImpl
from infra.db.user_repository_impl import UserRepositoryImpl
from infra.db.model_repository_impl import ModelRepositoryImpl
from infra.ml.tennis_predictor import TennisPredictor
from infra.web.controllers.user_controller import get_current_user

# Определение Pydantic моделей
class PredictionRequest(BaseModel):
    model_id: int
    player1_name: str
    player2_name: str
    player1_rank: int
    player2_rank: int
    player1_age: float
    player2_age: float
    player1_height_cm: int
    player2_height_cm: int
    player1_hand: str  # "right" или "left"
    player2_hand: str  # "right" или "left"
    player1_wins_last_year: int
    player2_wins_last_year: int
    player1_losses_last_year: int
    player2_losses_last_year: int
    surface: str  # "clay", "hard", "grass", и т.д.
    tournament_level: str  # "grand_slam", "masters", "atp500", и т.д.

class PredictionResponse(BaseModel):
    id: Optional[int]
    user_id: int
    model_id: int
    input_data: Dict[str, Any]
    results: Dict[str, Any]
    created_at: datetime

router = APIRouter(
    prefix="/predictions",
    tags=["predictions"]
)

# для предсказателя теннисных матчей
tennis_predictor = TennisPredictor()

# Зависимость для получения use cases
def get_prediction_use_cases(db: Session = Depends(get_session)):
    prediction_repository = PredictionRepositoryImpl(db)
    user_repository = UserRepositoryImpl(db)
    model_repository = ModelRepositoryImpl(db)
    return PredictionUseCase(
        prediction_repository=prediction_repository,
        user_repository=user_repository,
        model_repository=model_repository,
        tennis_predictor=tennis_predictor
    )

def get_current_user_from_header(
    request: Request,
    db: Session = Depends(get_session)
):
    authorization = request.headers.get("Authorization")
    print(f"Заголовок Authorization: {authorization}")
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Отсутствует заголовок Authorization"
        )
        
    # Извлекаем токен
    if authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    else:
        token = authorization
    
    print(f"Извлеченный токен: {token}")
    
    # Получаем пользователя по токену
    try:
        # имитация проверки токена
        user_id = int(token.split("_")[-1])
        print(f"Извлеченный user_id: {user_id}")
        
        repository = UserRepositoryImpl(db)
        user = repository.get_user_by_id(user_id)
        
        if not user:
            print(f"Пользователь с ID {user_id} не найден")
            raise ValueError()
            
        print(f"Найден пользователь: id={user.id}, email={user.email}")
        return user
    except Exception as e:
        print(f"Ошибка при обработке токена: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )

@router.post("/", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
def make_prediction(
    prediction_data: PredictionRequest,
    current_user = Depends(get_current_user_from_header),
    use_cases: PredictionUseCase = Depends(get_prediction_use_cases),
    db: Session = Depends(get_session)
):

    
    try:
        # Преобразуем входные данные в словарь
        input_data = prediction_data.dict()
        input_data.pop("model_id", None)
        
        # Создаем предсказание
        prediction = use_cases.make_prediction(
            user_id=current_user.id,
            model_id=prediction_data.model_id,
            input_data=input_data
        )
        
        # Преобразуем выходные данные из JSON
        output_data = json.loads(prediction.output_data) if prediction.output_data else {}
        
        return PredictionResponse(
            id=prediction.id,
            user_id=prediction.user_id,
            model_id=prediction.model_id,
            input_data=input_data,
            results=output_data,
            created_at=prediction.created_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[PredictionResponse])
def get_user_predictions(
    current_user = Depends(get_current_user_from_header),
    use_cases: PredictionUseCase = Depends(get_prediction_use_cases),
    db: Session = Depends(get_session)
):
    
    predictions = use_cases.get_user_predictions(current_user.id)
    
    result = []
    for prediction in predictions:
        # Убедитесь, что все поля существуют и не None
        input_data = json.loads(prediction.input_data) if prediction.input_data else {}
        output_data = json.loads(prediction.output_data) if prediction.output_data else {}
        
        result.append(PredictionResponse(
            id=prediction.id,
            user_id=prediction.user_id,
            model_id=prediction.model_id,
            input_data=input_data,
            results=output_data,
            created_at=prediction.created_at
        ))
    
    return result
    
    return result

@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(
    prediction_id: int,
    current_user = Depends(get_current_user_from_header),
    use_cases: PredictionUseCase = Depends(get_prediction_use_cases),
    db: Session = Depends(get_session)
):

    prediction = use_cases.get_prediction(prediction_id)
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Предсказание не найдено"
        )
    
    # Проверяем, принадлежит ли предсказание текущему пользователю
    if prediction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет доступа к этому предсказанию"
        )
    
    # Преобразуем данные из JSON
    input_data = json.loads(prediction.input_data)
    output_data = json.loads(prediction.output_data)
    
    return PredictionResponse(
        id=prediction.id,
        user_id=prediction.user_id,
        model_id=prediction.model_id,
        input_data=input_data,
        results=output_data,
        created_at=prediction.created_at
    )