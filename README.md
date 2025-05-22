# 🎾 Tennis Match Prediction Service

Сервис машинного обучения для прогнозирования исходов теннисных матчей с веб-интерфейсом и API.


## 🎯 Описание проекта

Tennis Match Prediction Service - это полнофункциональная система для прогнозирования исходов теннисных матчей, использующая машинное обучение. Сервис предоставляет три уровня моделей прогнозирования с различной точностью и стоимостью использования.

### Основные возможности

- **Три модели ML**: Базовая, Расширенная и Премиум с различными наборами параметров
- **Веб-интерфейс**: Удобный интерфейс на Streamlit для создания прогнозов
- **Система пользователей**: Регистрация, аутентификация и управление балансом
- **Платная система**: Оплата за каждый прогноз в зависимости от модели

### Модели прогнозирования

| Модель | Параметры | Стоимость | Точность |
|--------|-----------|-----------|----------|
| **Базовая** | Ранг игроков, рука, покрытие корта (5 параметров) | 5 ед. | ~60-65% |
| **Расширенная** | + возраст, рост, статистика побед (10 параметров) | 10 ед. | ~70-75% |
| **Премиум** | + поражения, уровень турнира (13+ параметров) | 20 ед. | ~80-85% |

## 🏗️ Архитектура

## 🚀 Установка и настройка

### Требования
- Python 3.9+
- pip или conda

### Клонирование репозитория

git clone <repository-url>
cd Tennis-ML-service

## Модели 
Модели находятся на гугл-диске https://drive.google.com/drive/folders/1N2D0i_irTMT45Fw6rNQBlSr6moHUSCSJ

Перед запуском проекта нужно скачать их и положить в папку models.

# Начисление начальных баллов пользователям
python add_credits_to_users.py --all --amount 100

### Использование
python main.py

## Запуск frontend
streamlit run app.py
Веб-интерфейс будет доступен по адресу: http://localhost:8501



## 📁 Структура проекта

```bash
Tennis-ML-service/
├── app.py                          # Streamlit фронтенд
├── main.py                         # Точка входа FastAPI
├── requirements.txt                # Зависимости Python
├── init_db.py                      # Инициализация базы данных
├── init_models_db.py               # Инициализация ML моделей в БД
├── add_credits_to_users.py         # Скрипт начисления баллов пользователям
├── tennis_train_models.py          # Скрипт обучения ML моделей

├── config/
│   └── database.py                 # Конфигурация подключения к БД

├── core/
│   ├── entities/                   # Доменные сущности (User, Model, Prediction)
│   │   ├── user.py
│   │   ├── model.py
│   │   └── prediction.py
│   ├── repositories/              # Интерфейсы репозиториев
│   │   ├── user_repository.py
│   │   ├── model_repository.py
│   │   └── prediction_repository.py
│   └── use_cases/                 # Бизнес-логика (Use Cases)
│       ├── user_use_cases.py
│       ├── model_use_cases.py
│       └── prediction_use_case.py

├── infra/
│   ├── db/
│   │   ├── models.py               # SQLAlchemy модели
│   │   ├── user_repository_impl.py
│   │   ├── model_repository_impl.py
│   │   └── predictions_repository_impl.py
│   ├── ml/
│   │   └── tennis_predictor.py     # Предиктор для матчей в теннисе
│   └── web/
│       └── controllers/            # Контроллеры FastAPI
│           ├── user_controller.py
│           ├── model_controller.py
│           └── prediction_controller.py

└── models/                         # Сохранённые ML модели
    ├── basic_model.joblib
    ├── extended_model.joblib
    ├── premium_model.joblib
    └── model_info.json
```
