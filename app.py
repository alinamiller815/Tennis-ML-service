import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime, timedelta

# Базовый URL API
API_URL = "http://localhost:8000"

# Настройка страницы
st.set_page_config(
    page_title="Прогноз теннисных матчей",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Функция для получения данных о топ-100 теннисистах
def get_top_players():
    """Возвращает словарь с данными топ-100 теннисистов"""
    return {
        "Янник Синнер": {
            "rank": 1, "age": 22.8, "height": 188,
            "hand": "right", "wins": 48, "losses": 7
        },
        "Новак Джокович": {
            "rank": 2, "age": 36.7, "height": 188,
            "hand": "right", "wins": 42, "losses": 10
        },
        "Карлос Алькарас": {
            "rank": 3, "age": 20.9, "height": 183,
            "hand": "right", "wins": 45, "losses": 8
        },
        "Александр Зверев": {
            "rank": 4, "age": 27.1, "height": 198, 
            "hand": "right", "wins": 38, "losses": 15
        },
        "Даниил Медведев": {
            "rank": 5, "age": 28.2, "height": 198,
            "hand": "right", "wins": 40, "losses": 14
        },
        "Андрей Рублев": {
            "rank": 6, "age": 26.5, "height": 188,
            "hand": "right", "wins": 36, "losses": 16
        },
        "Хуберт Хуркач": {
            "rank": 7, "age": 27.2, "height": 196,
            "hand": "right", "wins": 32, "losses": 18
        },
        "Каспер Рууд": {
            "rank": 8, "age": 25.4, "height": 183,
            "hand": "right", "wins": 34, "losses": 17
        },
        "Алекс Де Минаур": {
            "rank": 9, "age": 25.3, "height": 183,
            "hand": "right", "wins": 31, "losses": 19
        },
        "Григор Димитров": {
            "rank": 10, "age": 32.9, "height": 191,
            "hand": "right", "wins": 29, "losses": 21
        },
        "Стефанос Циципас": {
            "rank": 11, "age": 25.8, "height": 193,
            "hand": "right", "wins": 33, "losses": 18
        },
        "Томми Пол": {
            "rank": 12, "age": 27.1, "height": 185,
            "hand": "right", "wins": 28, "losses": 22
        },
        "Тейлор Фриц": {
            "rank": 13, "age": 26.6, "height": 193,
            "hand": "right", "wins": 32, "losses": 19
        },
        "Бен Шелтон": {
            "rank": 14, "age": 21.5, "height": 193,
            "hand": "left", "wins": 29, "losses": 21
        },
        "Холгер Руне": {
            "rank": 15, "age": 21.1, "height": 188,
            "hand": "right", "wins": 30, "losses": 20
        },
        "Феликс Оже-Альяссим": {
            "rank": 16, "age": 23.9, "height": 193,
            "hand": "right", "wins": 28, "losses": 22
        },
        "Себастьян Корда": {
            "rank": 17, "age": 23.8, "height": 196,
            "hand": "right", "wins": 27, "losses": 23
        },
        "Лоренцо Музетти": {
            "rank": 18, "age": 22.3, "height": 185,
            "hand": "right", "wins": 26, "losses": 24
        },
        "Николас Харри": {
            "rank": 19, "age": 28.5, "height": 198,
            "hand": "right", "wins": 25, "losses": 25
        },
        "Карен Хачанов": {
            "rank": 20, "age": 28.1, "height": 198,
            "hand": "right", "wins": 27, "losses": 23
        },
        "Фрэнсис Тиафо": {
            "rank": 21, "age": 26.2, "height": 188,
            "hand": "right", "wins": 26, "losses": 24
        },
        "Уго Умбер": {
            "rank": 22, "age": 25.8, "height": 191,
            "hand": "left", "wins": 24, "losses": 26
        },
        "Акира Сантиллан": {
            "rank": 23, "age": 27.1, "height": 185,
            "hand": "right", "wins": 23, "losses": 27
        },
        "Адриан Маннарино": {
            "rank": 24, "age": 35.9, "height": 180,
            "hand": "left", "wins": 22, "losses": 28
        },
        "Франческо Пассаро": {
            "rank": 25, "age": 22.6, "height": 188,
            "hand": "right", "wins": 21, "losses": 29
        },
        "Мартон Фучович": {
            "rank": 26, "age": 32.3, "height": 188,
            "hand": "right", "wins": 20, "losses": 30
        },
        "Фабио Фоньини": {
            "rank": 27, "age": 37.0, "height": 178,
            "hand": "right", "wins": 19, "losses": 31
        },
        "Джек Дрейпер": {
            "rank": 28, "age": 22.4, "height": 193,
            "hand": "left", "wins": 23, "losses": 27
        },
        "Борна Чорич": {
            "rank": 29, "age": 27.6, "height": 188,
            "hand": "right", "wins": 22, "losses": 28
        },
        "Жереми Шарди": {
            "rank": 30, "age": 37.2, "height": 183,
            "hand": "right", "wins": 18, "losses": 32
        },
        "Артур Филс": {
            "rank": 31, "age": 19.8, "height": 191,
            "hand": "right", "wins": 26, "losses": 24
        },
        "Марин Чилич": {
            "rank": 32, "age": 35.5, "height": 198,
            "hand": "right", "wins": 17, "losses": 33
        },
        "Денис Шаповалов": {
            "rank": 33, "age": 25.1, "height": 185,
            "hand": "left", "wins": 21, "losses": 29
        },
        "Ян-Леннард Штруфф": {
            "rank": 34, "age": 34.0, "height": 193,
            "hand": "right", "wins": 20, "losses": 30
        },
        "Пабло Каррено Буста": {
            "rank": 35, "age": 32.8, "height": 188,
            "hand": "right", "wins": 19, "losses": 31
        },
        "Рафаэль Надаль": {
            "rank": 287, "age": 37.9, "height": 185,
            "hand": "left", "wins": 8, "losses": 4
        },
        "Роджер Федерер": {
            "rank": None, "age": 42.8, "height": 185,
            "hand": "right", "wins": 0, "losses": 0
        },
        "Энди Маррей": {
            "rank": 512, "age": 37.0, "height": 191,
            "hand": "right", "wins": 5, "losses": 7
        },
        "Доминик Тим": {
            "rank": 98, "age": 30.5, "height": 185,
            "hand": "right", "wins": 15, "losses": 35
        },
        "Ник Кирьос": {
            "rank": 116, "age": 29.1, "height": 193,
            "hand": "right", "wins": 12, "losses": 8
        },
        "Стэн Вавринка": {
            "rank": 67, "age": 39.2, "height": 183,
            "hand": "right", "wins": 18, "losses": 32
        },
        "Кеи Нисикори": {
            "rank": 355, "age": 34.4, "height": 180,
            "hand": "right", "wins": 6, "losses": 10
        },
        "Хуан Мартин дель Потро": {
            "rank": None, "age": 35.7, "height": 198,
            "hand": "right", "wins": 0, "losses": 0
        },
        "Гаэль Монфис": {
            "rank": 46, "age": 37.7, "height": 193,
            "hand": "right", "wins": 19, "losses": 31
        },
        "Жо-Вилфрид Цонга": {
            "rank": None, "age": 39.1, "height": 188,
            "hand": "right", "wins": 0, "losses": 0
        },
        "Джон Изнер": {
            "rank": None, "age": 39.0, "height": 208,
            "hand": "right", "wins": 0, "losses": 0
        },
        # Добавить больше игроков...
    }

# Функции для работы с API
def login(email, password):
    """Функция для входа пользователя"""
    try:
        response = requests.post(
            f"{API_URL}/users/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Ошибка соединения с сервером: {e}")
        return None

def register(name, email, password):
    """Функция для регистрации нового пользователя"""
    try:
        response = requests.post(
            f"{API_URL}/users/register",
            json={ "name": name, "email": email, "password": password}
        )
        if response.status_code == 201:
            return response.json()
        else:
            if response.status_code == 400:
                st.error(f"Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}")
            return None
    except Exception as e:
        st.error(f"Ошибка соединения с сервером: {e}")
        return None

def get_user_info(token):
    """Получение информации о пользователе"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/users/me", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка получения информации о пользователе: {response.status_code}")
            print(f"Текст ошибки: {response.text}")
            return None
    except Exception as e:
        st.error(f"Ошибка соединения с сервером: {e}")
        return None

def get_models(token):
    """Получение списка доступных моделей"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/models", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        st.error(f"Ошибка соединения с сервером: {e}")
        return []

def get_predictions(token):
    """Получение предсказаний пользователя"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/predictions", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        st.error(f"Ошибка соединения с сервером: {e}")
        return []

def get_prediction(token, prediction_id):
    """Получение конкретного предсказания по ID"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/predictions/{prediction_id}", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Ошибка соединения с сервером: {e}")
        return None

def make_prediction(token, prediction_data):
    """Создание нового предсказания"""
    print(f"Токен при создании предсказания: {token}")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            f"{API_URL}/predictions",
            headers=headers,
            json=prediction_data
        )
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Ошибка: {response.json().get('detail', 'Неизвестная ошибка')}")
            return None
    except Exception as e:
        st.error(f"Ошибка соединения с сервером: {e}")
        return None

def add_funds(token, amount):
    """Пополнение баланса пользователя"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(
            f"{API_URL}/users/add-funds?amount={amount}",
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Ошибка соединения с сервером: {e}")
        return None

def create_model(token, model_data):
    """Создание новой модели"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(
            f"{API_URL}/models",
            headers=headers,
            json=model_data
        )
        if response.status_code == 201:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Ошибка соединения с сервером: {e}")
        return None

# Вспомогательные функции для интерфейса
def display_prediction_results(result, player1_name, player2_name):
    """Отображение результатов предсказания с визуализацией"""
    st.subheader("Результаты предсказания")
    
    p1_prob = result["results"]["player1_win_probability"] * 100
    p2_prob = result["results"]["player2_win_probability"] * 100
    
    # Метрики
    cols = st.columns([2, 1, 2])
    with cols[0]:
        st.metric(
            label=f"{player1_name}",
            value=f"{p1_prob:.1f}%",
            delta=f"{p1_prob - 50:.1f}%" if p1_prob > 50 else f"{p1_prob - 50:.1f}%"
        )
    
    with cols[1]:
        st.info(f"VS")
    
    with cols[2]:
        st.metric(
            label=f"{player2_name}",
            value=f"{p2_prob:.1f}%",
            delta=f"{p2_prob - 50:.1f}%" if p2_prob > 50 else f"{p2_prob - 50:.1f}%"
        )
    
    # Визуализация вероятностей
    chart_data = pd.DataFrame({
        "Игрок": [player1_name, player2_name],
        "Вероятность победы (%)": [p1_prob, p2_prob]
    })
    st.bar_chart(chart_data.set_index("Игрок"))
    
    # Итоговый прогноз
    winner_color = "green" if result["results"]["confidence"] > 0.7 else "orange"
    st.markdown(
        f"<div style='padding: 10px; background-color: #f0f8ff; border-radius: 5px;'>"
        f"<h3 style='margin: 0;'>Предполагаемый победитель:</h3>"
        f"<h2 style='margin: 10px 0; color: {winner_color};'>{result['results']['predicted_winner']}</h2>"
        f"<p>с уверенностью {result['results']['confidence']*100:.1f}%</p>"
        f"</div>",
        unsafe_allow_html=True
    )

# Страницы интерфейса
def login_page():
    """Страница входа и регистрации"""
    st.title("🎾 Прогноз теннисных матчей")
    
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])
    
    # Вкладка входа в систему
    with tab1:
        with st.form("login_form"):
            st.subheader("Вход в систему")
            email = st.text_input("Email", placeholder="example@mail.com")
            password = st.text_input("Пароль", type="password")
            submit = st.form_submit_button("Войти")
            
            if submit:
                if email and password:
                    result = login(email, password)
                    if result:
                        st.session_state.token = result["access_token"]
                        print(f"Токен после авторизации: {st.session_state.token}")
                        st.session_state.logged_in = True
                        st.success("Вход выполнен успешно!")
                        st.session_state.current_page = "dashboard"
                        st.experimental_rerun()
                    else:
                        st.error("Неверный email или пароль")
                else:
                    st.error("Пожалуйста, заполните все поля")
    
    # Вкладка регистрации
    with tab2:
        with st.form("register_form"):
            st.subheader("Регистрация нового пользователя")
            name = st.text_input("Имя")
            email = st.text_input("Email", placeholder="example@mail.com", key="reg_email")
            password = st.text_input("Пароль", type="password", key="reg_password")
            password_confirm = st.text_input("Подтвердите пароль", type="password")
            submit = st.form_submit_button("Зарегистрироваться")
            
            if submit:
                if name and email and password and password == password_confirm:
                    result = register(name, email, password)
                    if result:
                        st.success("Регистрация успешна! Теперь вы можете войти.")
                    else:
                        st.error("Ошибка при регистрации. Возможно, пользователь с таким email уже существует.")
                else:
                    if password != password_confirm:
                        st.error("Пароли не совпадают")
                    else:
                        st.error("Пожалуйста, заполните все поля")
    
    st.markdown("---")
    st.info("Есть тестовая учетная запись: \n\n Email: test@example.com \n\n Пароль: password123")

def dashboard_page():
    """Главная страница после входа"""
    st.header("Панель управления")
    
    # Получаем предсказания пользователя
    predictions = get_predictions(st.session_state.token)
    
    # Получаем информацию о пользователе
    user_info = get_user_info(st.session_state.token)
    
    # Карточки с общей статистикой
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"Всего предсказаний: {len(predictions) if predictions else 0}")
    with col2:
        st.info(f"Баланс: {user_info['balance']} ед.")
    with col3:
        recent_preds = len([p for p in predictions if datetime.fromisoformat(p["created_at"].replace("Z", "+00:00")) > (datetime.now() - timedelta(days=7))]) if predictions else 0
        st.info(f"Прогнозов за неделю: {recent_preds}")
    
    # Последние прогнозы
    st.subheader("Последние прогнозы")
    if not predictions:
        st.warning("У вас пока нет предсказаний. Создайте новое предсказание!")
        if st.button("Создать новое предсказание"):
            st.session_state.current_page = "new_prediction"
            st.experimental_rerun()
    else:
        # Сортируем по дате и берем последние 5
        sorted_preds = sorted(predictions, key=lambda p: p["created_at"], reverse=True)[:5]
        
        for pred in sorted_preds:
            match = f"{pred['input_data']['player1_name']} vs {pred['input_data']['player2_name']}"
            winner = pred["results"]["predicted_winner"]
            confidence = pred["results"]["confidence"] * 100
            
            # Форматируем дату
            created_at = datetime.fromisoformat(pred["created_at"].replace("Z", "+00:00"))
            formatted_date = created_at.strftime("%d.%m.%Y %H:%M")
            
            with st.expander(f"{match} ({formatted_date})"):
                st.write(f"**Предсказанный победитель:** {winner}")
                st.write(f"**Уверенность:** {confidence:.1f}%")
                st.write(f"**Покрытие корта:** {pred['input_data']['surface']}")
                
                if st.button("Детали", key=f"details_{pred['id']}"):
                    st.session_state.selected_prediction_id = pred["id"]
                    st.session_state.current_page = "prediction_history"
                    st.experimental_rerun()
    
    # Блок "Быстрое создание прогноза"
    st.subheader("Быстрое создание прогноза")
    if st.button("Создать новый прогноз"):
        st.session_state.current_page = "new_prediction"
        st.experimental_rerun()

def new_prediction_page():
    """Страница создания нового прогноза"""
    st.header("Новое предсказание")
    
    # Получаем доступные модели
    models = get_models(st.session_state.token)
    if not models:
        st.error("Ошибка получения списка моделей")
        return
    
    # Блок с описанием
    with st.expander("Как создать прогноз", expanded=False):
        st.write("""
        1. Выберите модель для предсказания
        2. Введите данные о первом игроке
        3. Введите данные о втором игроке
        4. Укажите информацию о матче
        5. Нажмите кнопку "Создать предсказание"
        """)
    
    # Получаем данные о топ игроках
    player_templates = get_top_players()
    
    # Форма предсказания с вкладками для более удобного заполнения
    tab1, tab2, tab3 = st.tabs(["Модель", "Игроки", "Матч"])
    
    # Вкладка выбора модели
    with tab1:
        # Выбор модели с расширенной информацией
        st.subheader("Выберите модель для предсказания")
        
        model_options = {model["name"]: model["id"] for model in models}
        model_costs = {model["name"]: model["cost"] for model in models}
        
        # Радио-кнопки с описанием модели
        selected_model_name = st.radio(
            "Доступные модели:",
            options=list(model_options.keys())
        )
        
        # Найдем выбранную модель
        selected_model = next((m for m in models if m["name"] == selected_model_name), None)
        
        # Отображаем информацию о выбранной модели
        if selected_model:
            st.info(f"Стоимость использования: {selected_model['cost']} ед.")
            if "description" in selected_model:
                st.write(f"**Описание:** {selected_model['description']}")
            if "accuracy" in selected_model:
                st.write(f"**Точность модели:** {selected_model.get('accuracy', 0.8)*100:.1f}%")
            
            # Добавляем описание моделей если нет собственного описания
            model_descriptions = {
                "Базовая модель": "Использует основные параметры (ранг, рука, покрытие). Точность ~60-65%.",
                "Расширенная модель": "Добавляет физические данные и статистику побед. Точность ~70-75%.",
                "Премиум модель": "Учитывает все возможные параметры включая историю матчей. Точность ~80-85%."
            }
            
            model_type = selected_model_name.split()[0].lower() + " " + selected_model_name.split()[1].lower() 
            if "description" not in selected_model and model_type in model_descriptions:
                st.write(f"**Описание:** {model_descriptions[model_type]}")
    
    # Состояние для хранения данных игроков
    if "player1_data" not in st.session_state:
        # Используем более актуального игрока по умолчанию - Синнер
        default_player1 = "Янник Синнер"
        st.session_state.player1_data = player_templates[default_player1].copy()
        st.session_state.player1_data["name"] = default_player1
    
    if "player2_data" not in st.session_state:
        # Используем более актуального игрока по умолчанию - Алькарас  
        default_player2 = "Карлос Алькарас"
        st.session_state.player2_data = player_templates[default_player2].copy()
        st.session_state.player2_data["name"] = default_player2
    
    # Вкладка ввода данных игроков
    with tab2:
        st.subheader("Данные игроков")
        
        col1, col2 = st.columns(2)
        
        # Первый игрок
        with col1:
            st.markdown("### Первый игрок")
            
            # Поиск игрока
            player1_search = st.text_input("Поиск игрока", key="player1_search")
            
            # Фильтруем игроков по строке поиска
            filtered_players1 = [p for p in player_templates.keys() 
                                if player1_search.lower() in p.lower()] if player1_search else list(player_templates.keys())
            
            # Сортируем по рейтингу (если есть)
            sorted_players1 = sorted(filtered_players1, 
                                    key=lambda p: player_templates[p].get("rank", 1000) if player_templates[p].get("rank") is not None else 1000)
            
            # Добавляем опцию "Ввести вручную" в начало списка
            # player_options1 = ["Ввести вручную"] + sorted_players1[:30]  # Ограничиваем список до 30 игроков
            st.write(f"Всего игроков в шаблонах: {len(player_templates)}")
            st.write(f"Отсортированных игроков: {len(sorted_players1)}")
            player_options1 = ["Ввести вручную"] + sorted_players1
            # Выбор игрока
            player1_template = st.selectbox(
                "Выберите игрока (отсортировано по рейтингу)",
                options=player_options1,
                key="player1_select"
            )
            
            if player1_template != "Ввести вручную":
                temp_data = player_templates[player1_template].copy()
                temp_data["name"] = player1_template
                st.session_state.player1_data = temp_data
                player1_name = player1_template
            else:
                player1_name = st.text_input(
                    "Имя первого игрока", 
                    value=st.session_state.player1_data.get("name", "")
                )
                st.session_state.player1_data["name"] = player1_name
            
            # Форма с данными первого игрока
            player1_rank = st.number_input(
                "Рейтинг", min_value=1, max_value=1000, 
                value=st.session_state.player1_data["rank"]
            )
            player1_age = st.number_input(
                "Возраст", min_value=15.0, max_value=50.0, 
                value=st.session_state.player1_data["age"]
            )
            player1_height = st.number_input(
                "Рост (см)", min_value=150, max_value=220,
                value=st.session_state.player1_data["height"]
            )
            player1_hand = st.selectbox(
                "Игровая рука", options=["right", "left"],
                index=0 if st.session_state.player1_data["hand"] == "right" else 1
            )
            player1_wins = st.number_input(
                "Количество побед за год", min_value=0, max_value=100,
                value=st.session_state.player1_data["wins"]
            )
            player1_losses = st.number_input(
                "Количество поражений за год", min_value=0, max_value=100,
                value=st.session_state.player1_data["losses"]
            )
            
            # Обновляем данные в состоянии
            st.session_state.player1_data.update({
                "rank": player1_rank,
                "age": player1_age,
                "height": player1_height,
                "hand": player1_hand,
                "wins": player1_wins,
                "losses": player1_losses
            })
        
        # Второй игрок - аналогично первому
        with col2:
            st.markdown("### Второй игрок")
            
            # Поиск игрока
            player2_search = st.text_input("Поиск игрока", key="player2_search")
            
            # Фильтруем игроков по строке поиска
            filtered_players2 = [p for p in player_templates.keys() 
                                if player2_search.lower() in p.lower()] if player2_search else list(player_templates.keys())
            
            # Сортируем по рейтингу (если есть)
            sorted_players2 = sorted(filtered_players2, 
                                    key=lambda p: player_templates[p].get("rank", 1000) if player_templates[p].get("rank") is not None else 1000)
            
            # Добавляем опцию "Ввести вручную" в начало списка
            # player_options2 = ["Ввести вручную"] + sorted_players2[:30]
            st.write(f"Всего игроков в шаблонах: {len(player_templates)}")
            st.write(f"Отсортированных игроков: {len(sorted_players1)}")
            player_options2 = ["Ввести вручную"] + sorted_players2
            
            player2_template = st.selectbox(
                "Выберите игрока (отсортировано по рейтингу)",
                options=player_options2,
                key="player2_select"
            )
            
            if player2_template != "Ввести вручную":
                temp_data = player_templates[player2_template].copy()
                temp_data["name"] = player2_template
                st.session_state.player2_data = temp_data
                player2_name = player2_template
            else:
                player2_name = st.text_input(
                    "Имя второго игрока", 
                    value=st.session_state.player2_data.get("name", ""),
                    key="p2_name"
                )
                st.session_state.player2_data["name"] = player2_name
            
            # Форма с данными второго игрока
            player2_rank = st.number_input(
                "Рейтинг", min_value=1, max_value=1000, 
                value=st.session_state.player2_data["rank"],
                key="p2_rank"
            )
            player2_age = st.number_input(
                "Возраст", min_value=15.0, max_value=50.0, 
                value=st.session_state.player2_data["age"],
                key="p2_age"
            )
            player2_height = st.number_input(
                "Рост (см)", min_value=150, max_value=220,
                value=st.session_state.player2_data["height"],
                key="p2_height"
            )
            player2_hand = st.selectbox(
                "Игровая рука", options=["right", "left"],
                index=0 if st.session_state.player2_data["hand"] == "right" else 1,
                key="p2_hand"
            )
            player2_wins = st.number_input(
                "Количество побед за год", min_value=0, max_value=100,
                value=st.session_state.player2_data["wins"],
                key="p2_wins"
            )
            player2_losses = st.number_input(
                "Количество поражений за год", min_value=0, max_value=100,
                value=st.session_state.player2_data["losses"],
                key="p2_losses"
            )
            
            # Обновляем данные в состоянии
            st.session_state.player2_data.update({
                "rank": player2_rank,
                "age": player2_age,
                "height": player2_height,
                "hand": player2_hand,
                "wins": player2_wins,
                "losses": player2_losses
            })
    
    # Вкладка информации о матче
    with tab3:
        st.subheader("Информация о матче")
        
        col1, col2 = st.columns(2)
        with col1:
            surface = st.selectbox(
                "Покрытие корта",
                options=["clay", "hard", "grass", "carpet"],
                index=0
            )
            
            # Добавляем подсказки по покрытиям
            surface_info = {
                "clay": "Грунтовое покрытие, более медленное, высокий отскок мяча",
                "hard": "Твердое покрытие, средняя скорость, средний отскок",
                "grass": "Травяное покрытие, быстрое, низкий отскок",
                "carpet": "Ковровое покрытие, обычно в залах, средней скорости"
            }
            st.info(surface_info[surface])
            
        with col2:
            tournament_level = st.selectbox(
                "Уровень турнира",
                options=["grand_slam", "masters", "atp500", "atp250", "challenger"],
                index=0
            )
            
            # Добавляем подсказки по уровням турниров
            tournament_info = {
                "grand_slam": "Турниры Большого шлема - высший уровень",
                "masters": "Турниры серии Masters - следующие по престижу после Большого шлема",
                "atp500": "Турниры ATP 500 - третий уровень по престижу",
                "atp250": "Турниры ATP 250 - четвертый уровень по престижу",
                "challenger": "Турниры уровня Challenger - более низкий уровень"
            }
            st.info(tournament_info[tournament_level])
    
    # Кнопка создания предсказания (под всеми вкладками)
    if st.button("Создать предсказание", type="primary"):
        # Проверка баланса
        user_info = get_user_info(st.session_state.token)
        if user_info["balance"] < model_costs[selected_model_name]:
            st.error(f"Недостаточно средств на балансе. Требуется {model_costs[selected_model_name]} ед.")
            # Предложение пополнить баланс
            if st.button("Пополнить баланс"):
                st.session_state.current_page = "add_funds"
                st.experimental_rerun()
        else:
            # Подготовка данных для запроса
            prediction_data = {
                "model_id": model_options[selected_model_name],
                "player1_name": player1_name,
                "player2_name": player2_name,
                "player1_rank": player1_rank,
                "player2_rank": player2_rank,
                "player1_age": player1_age,
                "player2_age": player2_age,
                "player1_height_cm": player1_height,
                "player2_height_cm": player2_height,
                "player1_hand": player1_hand,
                "player2_hand": player2_hand,
                "player1_wins_last_year": player1_wins,
                "player2_wins_last_year": player2_wins,
                "player1_losses_last_year": player1_losses,
                "player2_losses_last_year": player2_losses,
                "surface": surface,
                "tournament_level": tournament_level
            }
            
            # При желании можно показать параметры
            if st.checkbox("Показать параметры модели"):
                st.json(prediction_data)
            
            # Отправка запроса и отображение результатов
            with st.spinner("Создаем предсказание..."):
                result = make_prediction(st.session_state.token, prediction_data)
                if result:
                    st.success("Предсказание успешно создано!")
                    
                    # Отображаем результаты с визуализацией
                    display_prediction_results(result, player1_name, player2_name)
                    
                    # Предлагаем быстрый переход к истории
                    if st.button("Перейти к истории предсказаний"):
                        st.session_state.current_page = "prediction_history"
                        st.experimental_rerun()

def prediction_history_page():
    """Страница истории предсказаний"""
    st.header("История предсказаний")
    
    # Получаем предсказания пользователя
    predictions = get_predictions(st.session_state.token)
    
    if not predictions:
        st.info("У вас пока нет предсказаний")
        if st.button("Создать новое предсказание"):
            st.session_state.current_page = "new_prediction"
            st.experimental_rerun()
        return
    
    # Получаем доступные модели для отображения имен
    models = get_models(st.session_state.token)
    
    # Фильтры
    st.subheader("Фильтры")
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_player = st.text_input("Фильтр по игроку")
    with col2:
        surfaces = ["Все"] + list(set(p["input_data"]["surface"] for p in predictions))
        filter_surface = st.selectbox(
            "Фильтр по покрытию",
            options=surfaces
        )
    with col3:
        sort_by = st.selectbox(
            "Сортировать по",
            options=["Дате (новые сначала)", "Дате (старые сначала)", "Уверенности (убывание)", "Уверенности (возрастание)"]
        )
    
    # Создаем таблицу с предсказаниями
    pred_data = []
    for pred in predictions:
        model_name = next((m["name"] for m in models if m["id"] == pred["model_id"]), "Неизвестная модель")
        
        # Форматируем дату
        created_at = datetime.fromisoformat(pred["created_at"].replace("Z", "+00:00"))
        formatted_date = created_at.strftime("%d.%m.%Y %H:%M")
        
        # Определяем победителя
        winner = pred["results"]["predicted_winner"]
        confidence = pred["results"]["confidence"] * 100
        
        # Прогноз матча
        match = f"{pred['input_data']['player1_name']} vs {pred['input_data']['player2_name']}"
        
        # Поверхность корта
        surface = pred['input_data']['surface']
        
        pred_data.append({
            "ID": pred["id"],
            "Матч": match,
            "Модель": model_name,
            "Поверхность": surface,
            "Предсказанный победитель": winner,
            "Уверенность": f"{confidence:.1f}%",
            "Дата создания": formatted_date
        })
    
    # Применяем фильтры
    filtered_data = pred_data
    if filter_player:
        filtered_data = [p for p in filtered_data if filter_player.lower() in p["Матч"].lower()]
    if filter_surface != "Все":
        filtered_data = [p for p in filtered_data if p["Поверхность"] == filter_surface]
    
    # Применяем сортировку
    if sort_by == "Дате (новые сначала)":
        filtered_data.sort(key=lambda x: x["Дата создания"], reverse=True)
    elif sort_by == "Дате (старые сначала)":
        filtered_data.sort(key=lambda x: x["Дата создания"])
    elif sort_by == "Уверенности (убывание)":
        filtered_data.sort(key=lambda x: float(x["Уверенность"].replace("%", "")), reverse=True)
    elif sort_by == "Уверенности (возрастание)":
        filtered_data.sort(key=lambda x: float(x["Уверенность"].replace("%", "")))
    
    # Создаем DataFrame и отображаем его
    if filtered_data:
        df = pd.DataFrame(filtered_data)
        st.dataframe(df, use_container_width=True)
        
        # Выбор предсказания для детального просмотра
        selected_pred_id = st.selectbox(
            "Выберите предсказание для детального просмотра",
            options=df["ID"].tolist(),
            format_func=lambda x: f"Прогноз #{x}: {df[df['ID'] == x]['Матч'].iloc[0]}"
        )
        
        # Отображаем детальную информацию о выбранном предсказании
        if selected_pred_id:
            selected_pred = next((p for p in predictions if p["id"] == selected_pred_id), None)
            if selected_pred:
                st.subheader(f"Детали прогноза #{selected_pred_id}")
                
                # Данные об игроках
                col1, col2 = st.columns(2)
                with col1:
                    p1 = selected_pred["input_data"]
                    st.subheader(f"{p1['player1_name']}")
                    st.write(f"Рейтинг: {p1['player1_rank']}")
                    st.write(f"Возраст: {p1['player1_age']} лет")
                    st.write(f"Рост: {p1['player1_height_cm']} см")
                    st.write(f"Рука: {'Правая' if p1['player1_hand'] == 'right' else 'Левая'}")
                    st.write(f"Побед за год: {p1['player1_wins_last_year']}")
                    st.write(f"Поражений за год: {p1['player1_losses_last_year']}")
                    
                    p1_prob = selected_pred["results"]["player1_win_probability"] * 100
                    st.metric(
                        label="Вероятность победы",
                        value=f"{p1_prob:.1f}%"
                    )
                
                with col2:
                    p2 = selected_pred["input_data"]
                    st.subheader(f"{p2['player2_name']}")
                    st.write(f"Рейтинг: {p2['player2_rank']}")
                    st.write(f"Возраст: {p2['player2_age']} лет")
                    st.write(f"Рост: {p2['player2_height_cm']} см")
                    st.write(f"Рука: {'Правая' if p2['player2_hand'] == 'right' else 'Левая'}")
                    st.write(f"Побед за год: {p2['player2_wins_last_year']}")
                    st.write(f"Поражений за год: {p2['player2_losses_last_year']}")
                    
                    p2_prob = selected_pred["results"]["player2_win_probability"] * 100
                    st.metric(
                        label="Вероятность победы",
                        value=f"{p2_prob:.1f}%"
                    )
                
                # Информация о матче
                st.subheader("Информация о матче")
                st.write(f"Покрытие корта: {selected_pred['input_data']['surface']}")
                st.write(f"Уровень турнира: {selected_pred['input_data']['tournament_level']}")
                
                # Итоговый прогноз с визуализацией
                display_prediction_results(
                    selected_pred, 
                    selected_pred['input_data']['player1_name'],
                    selected_pred['input_data']['player2_name']
                )
    else:
        st.warning("Нет предсказаний, соответствующих фильтрам")

def add_funds_page():
    """Страница пополнения баланса"""
    st.header("Пополнение баланса")
    
    # Получаем текущий баланс пользователя
    user_info = get_user_info(st.session_state.token)
    st.info(f"Текущий баланс: {user_info['balance']} ед.")
    
    with st.form("add_funds_form"):
        st.subheader("Выберите сумму пополнения")
        
        amount_options = [10, 50, 100, 200, 500]
        selected_amount = st.radio(
            "Предлагаемые суммы:",
            options=amount_options,
            format_func=lambda x: f"{x} ед."
        )
        
        # Или ввод произвольной суммы
        custom_amount = st.number_input(
            "Или введите свою сумму:",
            min_value=10.0, 
            value=50.0, 
            step=10.0
        )
        
        # Итоговая сумма
        final_amount = custom_amount if custom_amount != 50.0 else selected_amount
        
        payment_method = st.selectbox(
            "Способ оплаты",
            options=["Банковская карта", "Электронный кошелек", "Банковский перевод"]
        )
        
        # Условные поля в зависимости от способа оплаты
        if payment_method == "Банковская карта":
            st.text_input("Номер карты", placeholder="XXXX XXXX XXXX XXXX")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Срок действия", placeholder="ММ/ГГ")
            with col2:
                st.text_input("CVV", type="password", placeholder="XXX")
        
        elif payment_method == "Электронный кошелек":
            st.selectbox(
                "Выберите кошелек",
                options=["ЮMoney", "WebMoney", "QIWI"]
            )
            st.text_input("Номер кошелька или телефон")
        
        elif payment_method == "Банковский перевод":
            st.info("""
            Реквизиты для перевода:
            - Получатель: ООО "Теннис ML"
            - ИНН: 1234567890
            - Счет: 40702810123456789012
            - Банк: АО "Прогноз-Банк"
            - БИК: 044525111
            - Назначение платежа: Пополнение баланса пользователя
            """)
        
        # Подтверждение
        agree = st.checkbox("Я согласен с условиями оплаты")
        submit = st.form_submit_button("Оплатить")
        
        if submit:
            if agree:
                # В реальном приложении здесь был бы код для обработки платежа
                # Пока просто добавляем деньги напрямую через API
                result = add_funds(st.session_state.token, final_amount)
                if result:
                    st.success(f"Баланс успешно пополнен. Новый баланс: {result['balance']} ед.")
                    # Предлагаем вернуться к прогнозам
                    if st.button("Перейти к созданию прогноза"):
                        st.session_state.current_page = "new_prediction"
                        st.experimental_rerun()
            else:
                st.error("Необходимо согласиться с условиями оплаты")

def admin_page():
    """Административная панель"""
    st.title("Административная панель")
    
    tab1, tab2 = st.tabs(["Управление моделями", "Статистика пользователей"])
    
    # Вкладка управления моделями
    with tab1:
        st.header("Доступные модели")
        models = get_models(st.session_state.token)
        
        if models:
            for model in models:
                with st.expander(f"{model['name']} (Стоимость: {model['cost']} ед.)"):
                    st.write(f"ID: {model['id']}")
                    st.write(f"Описание: {model.get('description', 'Нет описания')}")
                    st.write(f"Точность: {model.get('accuracy', 0.8)*100:.1f}%")
                    st.write(f"Создана: {model.get('created_at', 'Нет данных')}")
                    
                    # Кнопки управления моделью (заглушки)
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Редактировать", key=f"edit_{model['id']}"):
                            st.info("Функция редактирования модели в разработке")
                    with col2:
                        if st.button("Удалить", key=f"delete_{model['id']}"):
                            st.warning("Функция удаления модели в разработке")
        
        st.header("Создать новую модель")
        with st.form("create_model_form"):
            model_name = st.text_input("Название модели")
            model_description = st.text_area("Описание")
            model_cost = st.number_input("Стоимость использования", min_value=1.0, value=10.0)
            model_file = st.file_uploader("Файл модели", type=["pkl", "h5", "joblib"])
            
            # Дополнительные параметры модели
            st.subheader("Дополнительные параметры")
            col1, col2 = st.columns(2)
            with col1:
                model_accuracy = st.slider("Точность модели", min_value=0.5, max_value=1.0, value=0.8, step=0.01)
            with col2:
                model_type = st.selectbox(
                    "Тип модели",
                    options=["classification", "regression", "ensemble"]
                )
            
            submit = st.form_submit_button("Создать модель")
            
            if submit and model_name and model_cost:
                if not model_file:
                    st.warning("Файл модели не выбран. В демо-режиме это не обязательно.")
                
                # Подготовка данных модели
                model_data = {
                    "name": model_name,
                    "description": model_description,
                    "cost": model_cost,
                    "accuracy": model_accuracy,
                    "type": model_type,
                }
                
                # В реальном приложении здесь был бы код для загрузки файла модели
                # Сейчас просто вызовем API для создания модели
                result = create_model(st.session_state.token, model_data)
                if result:
                    st.success("Модель успешно создана!")
                    st.experimental_rerun()
                else:
                    st.error("Ошибка при создании модели")
    
    # Вкладка статистики пользователей (заглушка)
    with tab2:
        st.info("Эта функция находится в разработке")
        
        # Макет будущей статистики
        st.subheader("Общая статистика")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Всего пользователей", "42")
        with col2:
            st.metric("Активных за месяц", "28", "+5")
        with col3:
            st.metric("Всего предсказаний", "156", "+12")
        
        # Заглушка для графика
        st.subheader("Активность пользователей")
        chart_data = pd.DataFrame({
            "Дата": pd.date_range(start="2023-01-01", periods=30),
            "Новые пользователи": [2, 1, 3, 0, 1, 2, 0, 1, 0, 1, 0, 2, 1, 3, 1, 0, 2, 1, 0, 1, 2, 3, 1, 1, 0, 2, 1, 0, 1, 2],
            "Предсказания": [5, 8, 12, 7, 9, 11, 6, 8, 7, 10, 5, 9, 8, 15, 12, 7, 9, 8, 6, 10, 11, 14, 9, 8, 7, 12, 10, 8, 9, 11]
        })
        chart_data = chart_data.set_index("Дата")
        st.line_chart(chart_data)
        
        st.subheader("Список пользователей")
        st.info("В разработке")

# Главная функция
def main():
    # Инициализация состояния сессии
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "token" not in st.session_state:
        st.session_state.token = None
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login" if not st.session_state.logged_in else "dashboard"
    
    # Если пользователь авторизован - показываем боковую панель
    if st.session_state.logged_in:
        with st.sidebar:
            # Получаем информацию о пользователе
            user_info = get_user_info(st.session_state.token)
            if not user_info:
                st.error("Ошибка получения данных пользователя. Пожалуйста, войдите снова.")
                st.session_state.logged_in = False
                st.session_state.token = None
                st.session_state.current_page = "login"
                st.experimental_rerun()
                return
            
            # Информация о пользователе
            st.image("https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y", width=100)
            st.subheader(f"Привет, {user_info['name']}!")
            st.write(f"**Email:** {user_info['email']}")
            
            # Показываем баланс с цветовой индикацией
            balance_color = "green" if user_info['balance'] > 50 else "orange" if user_info['balance'] > 20 else "red"
            st.markdown(
                f"<div style='padding: 10px; background-color: #f0f8ff; border-radius: 5px;'>"
                f"<p style='margin: 0;'>Баланс:</p>"
                f"<h3 style='margin: 0; color: {balance_color};'>{user_info['balance']} ед.</h3>"
                f"</div>",
                unsafe_allow_html=True
            )
            
            # Навигационное меню
            st.subheader("Навигация")
            if st.button("🏠 Главная", key="nav_home"):
                st.session_state.current_page = "dashboard"
                st.experimental_rerun()
            
            if st.button("🧮 Новое предсказание", key="nav_predict"):
                st.session_state.current_page = "new_prediction"
                st.experimental_rerun()
            
            if st.button("📊 История предсказаний", key="nav_history"):
                st.session_state.current_page = "prediction_history"
                st.experimental_rerun()
            
            if st.button("💰 Пополнить баланс", key="nav_funds"):
                st.session_state.current_page = "add_funds"
                st.experimental_rerun()
            
            # Если пользователь администратор - показываем дополнительные кнопки
            if user_info.get("is_admin", False):
                st.subheader("Администрирование")
                if st.button("⚙️ Управление моделями", key="nav_admin"):
                    st.session_state.current_page = "admin"
                    st.experimental_rerun()
            
            # Кнопка выхода внизу сайдбара
            st.markdown("---")
            if st.button("🚪 Выйти", key="nav_logout"):
                st.session_state.logged_in = False
                st.session_state.token = None
                st.session_state.current_page = "login"
                st.experimental_rerun()
    
    # Отображение соответствующей страницы
    if not st.session_state.logged_in:
        login_page()
    else:
        # Шапка страницы
        st.title("🎾 Система прогнозирования теннисных матчей")
        
        # Отображение текущей страницы
        if st.session_state.current_page == "dashboard":
            dashboard_page()
        elif st.session_state.current_page == "new_prediction":
            new_prediction_page()
        elif st.session_state.current_page == "prediction_history":
            prediction_history_page()
        elif st.session_state.current_page == "add_funds":
            add_funds_page()
        elif st.session_state.current_page == "admin" and user_info.get("is_admin", False):
            admin_page()
        else:
            st.session_state.current_page = "dashboard"
            st.experimental_rerun()

if __name__ == "__main__":
    main()