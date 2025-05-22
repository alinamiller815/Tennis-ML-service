from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from config.database import get_session
from core.use_cases.user_use_cases import UserUseCases
from infra.db.user_repository_impl import UserRepositoryImpl


router = APIRouter(prefix="/users", tags=["Users"])

# ======= Pydantic схемы =======
class UserCreate(BaseModel):
    email: str
    name: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    balance: float

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Функция для получения текущего пользователя по токену
def get_current_user(token: str, db: Session = Depends(get_session)):
    try:
        # Простая имитация проверки токена
        user_id = int(token.split("_")[-1])
        repository = UserRepositoryImpl(db)
        user = repository.get_user_by_id(user_id)
        if not user:
            raise ValueError()
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные"
        )

# Функция для получения пользователя из заголовка Authorization
def get_current_user_from_header(
    request: Request,
    db: Session = Depends(get_session)
):
    """Извлекает токен из заголовка и получает пользователя"""
    authorization = request.headers.get("Authorization")
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
        
    return get_current_user(token, db)
    
# Зависимость для получения use cases
def get_user_use_cases(db: Session = Depends(get_session)):
    user_repository = UserRepositoryImpl(db)
    return UserUseCases(user_repository)


# ======= Роуты =======
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, use_cases: UserUseCases = Depends(get_user_use_cases)):
    """Регистрация нового пользователя"""
    try:
        user = use_cases.register_user(
            email=user_data.email,
            name=user_data.name,
            password=user_data.password
        )
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            balance=user.balance
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=TokenResponse)
def login_user(user_data: UserLogin, use_cases: UserUseCases = Depends(get_user_use_cases)):
    """Аутентификация пользователя"""
    user = use_cases.auth_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Генерация токена (в реальном приложении используйте JWT)
    token = f"fake_token_{user.id}"
    
    return TokenResponse(access_token=token, token_type="bearer")

@router.post("/add-funds", response_model=UserResponse)
def add_funds(
    amount: float, 
    current_user = Depends(get_current_user_from_header),
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Пополнение баланса пользователя"""
    try:
        user = use_cases.add_funds(current_user.id, amount)
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            balance=user.balance
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_user_from_header)):
    """Получение информации о текущем пользователе"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        balance=current_user.balance
    )