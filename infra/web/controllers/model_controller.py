from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List

from config.database import get_session
from core.use_cases.model_use_cases import ModelUseCases
from infra.db.model_repository_impl import ModelRepositoryImpl

# Определение Pydantic моделей
class ModelCreate(BaseModel):
    name: str
    cost: float = Field(gt=0.0)

class ModelResponse(BaseModel):
    id: int
    name: str
    cost: float

router = APIRouter(
    prefix="/models",
    tags=["models"]
)

# Зависимость для получения use cases
def get_model_use_cases(db: Session = Depends(get_session)):
    model_repository = ModelRepositoryImpl(db)
    return ModelUseCases(model_repository)

@router.post("/", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
def create_model(
    model_data: ModelCreate, 
    use_cases: ModelUseCases = Depends(get_model_use_cases)
):
    try:
        model = use_cases.create_model(
            name=model_data.name,
            cost=model_data.cost
        )
        return ModelResponse(
            id=model.id,
            name=model.name,
            cost=model.cost
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[ModelResponse])
def get_available_models(
    use_cases: ModelUseCases = Depends(get_model_use_cases)
):
    models = use_cases.get_available_models()
    return [
        ModelResponse(
            id=model.id,
            name=model.name,
            cost=model.cost
        ) for model in models
    ]

@router.get("/{model_id}", response_model=ModelResponse)
def get_model(
    model_id: int,
    use_cases: ModelUseCases = Depends(get_model_use_cases)
):
    model = use_cases.get_model(model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Модель не найдена"
        )
    
    return ModelResponse(
        id=model.id,
        name=model.name,
        cost=model.cost
    )