import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import glob
import datetime
import re

# Создаем директорию для моделей, если она не существует
os.makedirs('models', exist_ok=True)

# Загрузка и объединение данных ATP
def load_atp_data(data_dir='/Users/alinamiller/Desktop/'):
    """Загружает данные ATP из всех доступных CSV-файлов и объединяет их"""
    all_csv_files = glob.glob(f"{data_dir}/*.csv")
    
    if not all_csv_files:
        raise FileNotFoundError(f"В директории {data_dir} не найдены CSV-файлы")
    
    # Загружаем и объединяем все файлы
    dfs = []
    for file in all_csv_files:
        try:
            year_match = re.search(r'(\d{4})', file)
            year = year_match.group(1) if year_match else "unknown"
            print(f"Загрузка данных за {year} год из {file}")
            
            df = pd.read_csv(file)
            dfs.append(df)
        except Exception as e:
            print(f"Ошибка при загрузке {file}: {e}")
    
    if not dfs:
        raise ValueError("Не удалось загрузить данные из файлов")
    
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"Данные объединены. Общее количество строк: {combined_df.shape[0]}")
    
    return combined_df

# Предобработка данных ATP
def preprocess_atp_data(df):
    """Преобразует данные ATP в формат, необходимый для моделей"""
    print("Начало предобработки данных...")
    
    # Проверяем наличие необходимых колонок
    required_columns = [
        'winner_name', 'loser_name',
        'winner_rank', 'loser_rank',
        'surface'
    ]
    
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"В данных отсутствует обязательная колонка '{column}'")
    
    # Выбираем только матчи с известными рейтингами игроков
    df = df.dropna(subset=['winner_rank', 'loser_rank'])
    
    # Дополнительные колонки для расширенных моделей (проверяем их наличие)
    extended_columns = [
        'winner_age', 'loser_age',
        'winner_ht', 'loser_ht'  # ht - height (рост)
    ]
    
    premium_columns = [
        'tourney_level',
        'round',
        'w_ace', 'l_ace',  # эйсы
        'w_df', 'l_df'     # двойные ошибки
    ]
    
    # Создаем новый DataFrame для моделей
    matches_df = pd.DataFrame()
    
    # Базовые признаки (всегда доступны)
    matches_df['player1_name'] = df['winner_name']
    matches_df['player2_name'] = df['loser_name']
    matches_df['player1_rank'] = df['winner_rank'].astype(float)
    matches_df['player2_rank'] = df['loser_rank'].astype(float)
    matches_df['surface'] = df['surface']
    
    # Определяем игровые руки, если доступны
    if 'winner_hand' in df.columns and 'loser_hand' in df.columns:
        matches_df['player1_hand'] = df['winner_hand'].fillna('right')
        matches_df['player2_hand'] = df['loser_hand'].fillna('right')
    else:
        # Если нет данных о руках, предполагаем, что все играют правой
        matches_df['player1_hand'] = 'right'
        matches_df['player2_hand'] = 'right'
    
    # Расширенные признаки (если доступны)
    if all(col in df.columns for col in extended_columns):
        print("Добавляем расширенные признаки")
        matches_df['player1_age'] = df['winner_age'].fillna(df['winner_age'].median())
        matches_df['player2_age'] = df['loser_age'].fillna(df['loser_age'].median())
        matches_df['player1_height'] = df['winner_ht'].fillna(df['winner_ht'].median())
        matches_df['player2_height'] = df['loser_ht'].fillna(df['loser_ht'].median())
    
    # Расчет побед/поражений за последний год
    # Для этого нам нужна дата матча
    if 'tourney_date' in df.columns:
        print("Расчет статистики побед/поражений за последний год...")
        # Преобразуем дату из формата YYYYMMDD в datetime
        df['tourney_date'] = pd.to_datetime(df['tourney_date'], format='%Y%m%d', errors='coerce')
        
        # Сортируем по дате
        df_sorted = df.sort_values('tourney_date')
        
        # Создаем словари для отслеживания побед и поражений
        player_wins = {}
        player_losses = {}
        
        # Для каждого матча
        for _, row in df_sorted.iterrows():
            winner = row['winner_name']
            loser = row['loser_name']
            match_date = row['tourney_date']
            
            # Если игроки еще не в словарях, добавляем их
            if winner not in player_wins:
                player_wins[winner] = []
            if loser not in player_losses:
                player_losses[loser] = []
            
            # Добавляем победу и поражение
            player_wins[winner].append(match_date)
            player_losses[loser].append(match_date)
        
        # Функция для подсчета матчей за последний год
        def count_last_year_matches(player, dates, match_date):
            if player not in dates:
                return 0
            player_dates = dates[player]
            one_year_ago = match_date - pd.DateOffset(years=1)
            return sum(1 for date in player_dates if one_year_ago <= date < match_date)
        
        # Применяем функцию ко всем матчам
        matches_df['player1_wins_last_year'] = df_sorted.apply(
            lambda row: count_last_year_matches(row['winner_name'], player_wins, row['tourney_date']), axis=1
        )
        matches_df['player2_wins_last_year'] = df_sorted.apply(
            lambda row: count_last_year_matches(row['loser_name'], player_wins, row['tourney_date']), axis=1
        )
        matches_df['player1_losses_last_year'] = df_sorted.apply(
            lambda row: count_last_year_matches(row['winner_name'], player_losses, row['tourney_date']), axis=1
        )
        matches_df['player2_losses_last_year'] = df_sorted.apply(
            lambda row: count_last_year_matches(row['loser_name'], player_losses, row['tourney_date']), axis=1
        )
    else:
        # Если нет дат, используем средние значения
        print("Нет данных о датах, используем приближенные значения для побед/поражений")
        matches_df['player1_wins_last_year'] = 15  # приближенное значение
        matches_df['player2_wins_last_year'] = 15
        matches_df['player1_losses_last_year'] = 10
        matches_df['player2_losses_last_year'] = 10
    
    # Премиум признаки (если доступны)
    if 'w_ace' in df.columns and 'l_ace' in df.columns:
        matches_df['player1_aces'] = df['w_ace'].fillna(0)
        matches_df['player2_aces'] = df['l_ace'].fillna(0)
    
    if 'tourney_level' in df.columns:
        matches_df['tournament_level'] = df['tourney_level']
    
    if 'round' in df.columns:
        matches_df['round'] = df['round']
    
    # Добавляем целевую переменную (1 - победа первого игрока, что всегда верно в нашем случае)
    matches_df['winner'] = 1
    
    # Теперь создадим альтернативную версию каждого матча, поменяв игроков местами
    swapped_df = matches_df.copy()
    
    # Меняем имена игроков
    columns_to_swap = [col for col in matches_df.columns if ('player1' in col or 'player2' in col)]
    for col in columns_to_swap:
        new_col = col.replace('player1', 'temp').replace('player2', 'player1').replace('temp', 'player2')
        swapped_df[new_col] = matches_df[col]
    
    # Меняем целевую переменную
    swapped_df['winner'] = 0
    
    # Объединяем оригинальные и свопнутые матчи
    final_df = pd.concat([matches_df, swapped_df], ignore_index=True)
    
    # Удаляем дубликаты
    final_df = final_df.drop_duplicates()
    
    print(f"Итоговый датасет: {final_df.shape[0]} строк, {final_df.shape[1]} колонок")
    
    return final_df

# Подготовка данных для моделей
def prepare_model_data(df):
    """Разделяет данные на наборы для разных моделей"""
    # Базовые признаки (для базовой модели)
    basic_features = [
        'player1_rank', 'player2_rank',
        'player1_hand', 'player2_hand',
        'surface'
    ]
    
    # Расширенные признаки (для расширенной модели)
    extended_features = basic_features + [
        'player1_age', 'player2_age',
        'player1_height', 'player2_height',
        'player1_wins_last_year', 'player2_wins_last_year'
    ]
    
    # Премиум признаки (для премиум модели)
    premium_features = extended_features + [
        'player1_losses_last_year', 'player2_losses_last_year'
    ]
    
    # Добавляем дополнительные признаки, если они есть
    if 'player1_aces' in df.columns:
        premium_features += ['player1_aces', 'player2_aces']
    
    if 'tournament_level' in df.columns:
        premium_features.append('tournament_level')
    
    if 'round' in df.columns:
        premium_features.append('round')
    
    # Целевая переменная (победитель)
    target = 'winner'
    
    # Проверяем наличие всех необходимых признаков
    available_features = df.columns.tolist()
    
    def check_and_filter_features(feature_list):
        return [f for f in feature_list if f in available_features]
    
    basic_features = check_and_filter_features(basic_features)
    extended_features = check_and_filter_features(extended_features)
    premium_features = check_and_filter_features(premium_features)
    
    print(f"Базовые признаки ({len(basic_features)}): {basic_features}")
    print(f"Расширенные признаки ({len(extended_features)}): {extended_features}")
    print(f"Премиум признаки ({len(premium_features)}): {premium_features}")
    
    # Создаем наборы данных для каждой модели
    basic_X = df[basic_features]
    extended_X = df[extended_features]
    premium_X = df[premium_features]
    y = df[target]
    
    # Разделение на обучающий и тестовый наборы
    basic_X_train, basic_X_test, y_train, y_test = train_test_split(
        basic_X, y, test_size=0.2, random_state=42)
    
    extended_X_train, extended_X_test, _, _ = train_test_split(
        extended_X, y, test_size=0.2, random_state=42)
    
    premium_X_train, premium_X_test, _, _ = train_test_split(
        premium_X, y, test_size=0.2, random_state=42)
    
    # Определение категориальных признаков
    categorical_features = [col for col in basic_features if df[col].dtype == 'object']
    extended_categorical = [col for col in extended_features if df[col].dtype == 'object']
    premium_categorical = [col for col in premium_features if df[col].dtype == 'object']
    
    print(f"Категориальные признаки (базовая): {categorical_features}")
    print(f"Категориальные признаки (расширенная): {extended_categorical}")
    print(f"Категориальные признаки (премиум): {premium_categorical}")
    
    # Создание преобразователей
    basic_preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'
    )
    
    extended_preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), extended_categorical)
        ],
        remainder='passthrough'
    )
    
    premium_preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), premium_categorical)
        ],
        remainder='passthrough'
    )
    
    # Возвращаем данные и преобразователи
    return {
        'basic': (basic_X_train, basic_X_test, basic_preprocessor, basic_features),
        'extended': (extended_X_train, extended_X_test, extended_preprocessor, extended_features),
        'premium': (premium_X_train, premium_X_test, premium_preprocessor, premium_features)
    }, y_train, y_test

# Обучение и оценка моделей
def train_and_evaluate_models(data_dict, y_train, y_test):
    models = {}
    results = {}
    
    # Базовая модель (логистическая регрессия)
    print("Обучение базовой модели...")
    basic_X_train, basic_X_test, basic_preprocessor, basic_features = data_dict['basic']
    basic_model = Pipeline([
        ('preprocessor', basic_preprocessor),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42))
    ])
    basic_model.fit(basic_X_train, y_train)
    basic_preds = basic_model.predict(basic_X_test)
    basic_proba = basic_model.predict_proba(basic_X_test)
    basic_accuracy = accuracy_score(y_test, basic_preds)
    print(f"Базовая модель - Точность: {basic_accuracy:.4f}")
    models['basic'] = basic_model
    results['basic'] = {
        'accuracy': basic_accuracy,
        'report': classification_report(y_test, basic_preds),
        'features': basic_features
    }
    
    # Расширенная модель (случайный лес)
    print("Обучение расширенной модели...")
    extended_X_train, extended_X_test, extended_preprocessor, extended_features = data_dict['extended']
    extended_model = Pipeline([
        ('preprocessor', extended_preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    extended_model.fit(extended_X_train, y_train)
    extended_preds = extended_model.predict(extended_X_test)
    extended_proba = extended_model.predict_proba(extended_X_test)
    extended_accuracy = accuracy_score(y_test, extended_preds)
    print(f"Расширенная модель - Точность: {extended_accuracy:.4f}")
    models['extended'] = extended_model
    results['extended'] = {
        'accuracy': extended_accuracy,
        'report': classification_report(y_test, extended_preds),
        'features': extended_features
    }
    
    # Премиум модель (градиентный бустинг)
    print("Обучение премиум модели...")
    premium_X_train, premium_X_test, premium_preprocessor, premium_features = data_dict['premium']
    premium_model = Pipeline([
        ('preprocessor', premium_preprocessor),
        ('classifier', GradientBoostingClassifier(n_estimators=100, random_state=42))
    ])
    premium_model.fit(premium_X_train, y_train)
    premium_preds = premium_model.predict(premium_X_test)
    premium_proba = premium_model.predict_proba(premium_X_test)
    premium_accuracy = accuracy_score(y_test, premium_preds)
    print(f"Премиум модель - Точность: {premium_accuracy:.4f}")
    models['premium'] = premium_model
    results['premium'] = {
        'accuracy': premium_accuracy,
        'report': classification_report(y_test, premium_preds),
        'features': premium_features
    }
    
    return models, results

# Сохранение моделей
def save_models(models, results):
    model_info = {}
    for name, model in models.items():
        filename = f"models/{name}_model.joblib"
        joblib.dump(model, filename)
        print(f"Модель {name} сохранена в {filename}")
        
        # Сохраняем информацию о модели
        model_info[name] = {
            'filename': filename,
            'features': results[name]['features'],
            'accuracy': float(results[name]['accuracy'])
        }
        
    # Сохраняем информацию о моделях в JSON
    import json
    with open('models/model_info.json', 'w') as f:
        json.dump(model_info, f, indent=4)
    
    return model_info

# Главная функция
if __name__ == "__main__":
    print("Начало обучения моделей для прогнозирования теннисных матчей...")
    
    try:
        # Загружаем данные ATP
        data = load_atp_data()
        
        # Предобрабатываем данные
        print("Предобработка данных...")
        processed_data = preprocess_atp_data(data)
        
        # Подготовка данных для моделей
        print("Подготовка данных для разных моделей...")
        data_dict, y_train, y_test = prepare_model_data(processed_data)
        
        # Обучение моделей
        print("Обучение моделей...")
        models, results = train_and_evaluate_models(data_dict, y_train, y_test)
        
        # Сохранение моделей
        print("Сохранение моделей...")
        model_info = save_models(models, results)
        
        print("Готово! Все модели обучены и сохранены.")
        
        # Вывод результатов
        for name, result in results.items():
            print(f"\n{name.capitalize()} модель:")
            print(f"Точность: {result['accuracy']:.4f}")
            print("Отчет о классификации:")
            print(result['report'])
            
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()