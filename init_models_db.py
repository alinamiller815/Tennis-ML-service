import sys
import os

# Добавляем корень проекта в Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy.orm import Session
from config.database import get_session, engine
from infra.db.models import ModelDB, Base
import json
import os

# Создаем таблицы, если их нет
Base.metadata.create_all(bind=engine)

# Функция для инициализации моделей
def init_models():
    # Модели и их стоимость
    models = [
        {"id": 1, "name": "Базовая модель (5 параметров)", "cost": 5.0},
        {"id": 2, "name": "Расширенная модель (11 параметров)", "cost": 10.0},
        {"id": 3, "name": "Премиум модель (15+ параметров)", "cost": 20.0}
    ]
    
    # Если есть файл с информацией о моделях, обновим точность
    model_info_path = "models/model_info.json"
    if os.path.exists(model_info_path):
        try:
            with open(model_info_path, 'r') as f:
                model_info = json.load(f)
                
            # Обновляем описание моделей с точностью
            for i, model in enumerate(models):
                model_name = {1: 'basic', 2: 'extended', 3: 'premium'}[model["id"]]
                if model_name in model_info:
                    accuracy = model_info[model_name].get('accuracy', 0)
                    models[i]["name"] = f"{model['name']} (точность: {accuracy:.2%})"
        except Exception as e:
            print(f"Ошибка чтения информации о моделях: {e}")
    
    # Добавляем модели в БД
    with Session(engine) as session:
        for model_data in models:
            # Проверяем, существует ли модель с таким ID
            existing_model = session.query(ModelDB).filter(ModelDB.id == model_data["id"]).first()
            
            if existing_model:
                # Обновляем существующую модель
                existing_model.name = model_data["name"]
                existing_model.cost = model_data["cost"]
                print(f"Модель {existing_model.name} обновлена")
            else:
                # Создаем новую модель
                model_db = ModelDB(
                    id=model_data["id"],
                    name=model_data["name"],
                    cost=model_data["cost"]
                )
                session.add(model_db)
                print(f"Модель {model_db.name} добавлена")
                
        # Фиксируем изменения
        session.commit()
    
    print("Модели успешно инициализированы в БД")

if __name__ == "__main__":
    init_models()