import streamlit as st
import json
import pandas as pd

# ==========================================
# 1. РОЗШИРЕНА ТА АКТУАЛІЗОВАНА БАЗА ДАНИХ
# ==========================================
phones_json = """
[
    {"brand": "Apple", "model": "iPhone 16 Pro Max", "price": 1300, "camera": 99, "battery": 88, "performance": 99, "display": 98, "design": 99},
    {"brand": "Apple", "model": "iPhone 15", "price": 750, "camera": 86, "battery": 78, "performance": 88, "display": 85, "design": 92},
    {"brand": "Apple", "model": "iPhone 13", "price": 550, "camera": 80, "battery": 72, "performance": 78, "display": 80, "design": 86},
    {"brand": "Samsung", "model": "Galaxy S26 Ultra", "price": 1350, "camera": 98, "battery": 93, "performance": 98, "display": 100, "design": 97},
    {"brand": "Samsung", "model": "Galaxy S25+", "price": 950, "camera": 91, "battery": 87, "performance": 94, "display": 96, "design": 93},
    {"brand": "Samsung", "model": "Galaxy A55", "price": 360, "camera": 74, "battery": 89, "performance": 70, "display": 86, "design": 82},
    {"brand": "Samsung", "model": "Galaxy A16 5G", "price": 180, "camera": 48, "battery": 86, "performance": 45, "display": 72, "design": 60},
    {"brand": "Google", "model": "Pixel 9 Pro XL", "price": 1050, "camera": 100, "battery": 84, "performance": 89, "display": 97, "design": 94},
    {"brand": "Google", "model": "Pixel 8a", "price": 470, "camera": 91, "battery": 79, "performance": 81, "display": 89, "design": 83},
    {"brand": "Xiaomi", "14 Ultra": "14 Ultra", "brand": "Xiaomi", "model": "14 Ultra", "price": 1050, "camera": 97, "battery": 86, "performance": 96, "display": 96, "design": 92},
    {"brand": "Xiaomi", "model": "POCO F6 Pro", "price": 480, "camera": 75, "battery": 88, "performance": 94, "display": 93, "design": 81},
    {"brand": "Xiaomi", "model": "Redmi Note 13 Pro+", "price": 330, "camera": 79, "battery": 87, "performance": 68, "display": 88, "design": 84},
    {"brand": "OnePlus", "model": "13", "price": 800, "camera": 93, "battery": 96, "performance": 97, "display": 97, "design": 91},
    {"brand": "OnePlus", "model": "Nord 4", "price": 420, "camera": 76, "battery": 92, "performance": 83, "display": 88, "design": 87},
    {"brand": "Asus", "model": "ROG Phone 9", "price": 1100, "camera": 76, "battery": 95, "performance": 100, "display": 96, "design": 90},
    {"brand": "Nothing", "model": "Phone (2)", "price": 550, "camera": 82, "battery": 81, "performance": 85, "display": 90, "design": 99}
]
"""
phones_db = json.loads(phones_json)

# ==========================================
# 2. НАЛАШТУВАННЯ СТОРІНКИ ТА ЕКСКЛЮЗИВНИЙ CSS
# ==========================================
st.set_page_config(page_title="Smart Phone Picker Pro", page_icon="⚡", layout="wide")

# Ін'єкція стилів для покращення дизайну інтерфейсу
st.markdown("""
<style>
    /* Стилізація карток пристроїв */
    .phone-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .phone-card:hover {
        transform: translateY(-4px);
        border-color: #ff4b4b;
    }
    /* Кастомні бейджі */
    .badge {
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-top { background-color: #ffe0b2; color: #b78103; }
    .badge-value { background-color: #e8f5e9; color: #2e7d32; }
    .badge-camera { background-color: #e1f5fe; color: #0288d1; }
    .badge-gaming { background-color: #f3e5f5; color: #7b1fa2; }
</style>
""", unsafe_allow_html=True)

# Головний заголовок системи
st.title("⚡ Професійна екосистема аналізу та підбору смартфонів")
st.markdown("Складні алгоритми зваженого скорингу, упаковані в інтуїтивно зрозумілий інтерфейс розробника.")
st.write("---")

# ==========================================
# 3. БІЧНА ПАНЕЛЬ (КЕРУВАННЯ ТА ФІЛЬТРАЦІЯ)
# ==========================================
st.sidebar.header("🎛️ Панель керування")

# Основні фільтри
budget = st.sidebar.slider("💰 Граничний бюджет ($)", min_value=100, max_value=1500, value=800, step=50)

available_brands = sorted(list(set(phone['brand'] for phone in phones_db)))
selected_brands = st.sidebar.multiselect("🏷️ Вибір брендів (усі, якщо порожньо)", available_brands)

sort_option = st.sidebar.selectbox(
    "📊 Сортування результатів", 
    ["За релевантністю (Матч %)", "Ціна: від найдешевших", "Ціна: від найдорожчих", "Коефіцієнт вигоди (Ціна/Якість)"]
)

st.sidebar.write("---")
st.sidebar.subheader("⚖️ Вага критеріїв оцінки")
st.sidebar.caption("Змінюй пріоритети, щоб миттєво перебудувати математичну модель")

# Повзунки критеріїв
w_cam = st.sidebar.slider("📸 Фото та відео можливості", 1, 5, 3)
w_bat = st.sidebar.slider("🔋 Автономність та енергоефективність", 1, 5, 3)
w_perf = st.sidebar.slider("🚀 Обчислювальна потужність (чипсет)", 1, 5, 3)
w_disp = st.sidebar.slider("📺 Технологічність дисплея", 1, 5, 3)
w_design = st.sidebar.slider("💎 Преміальність матеріалів та дизайн", 1, 5, 2)

# ==========================================
# 4. ОБЧИСЛЮВАЛЬНЕ ЯДРО (МАТЕМАТИЧНА МОДЕЛЬ)
# ==========================================
processed_phones = []

for phone in phones_db:
    # Жорсткі критерії фільтрації
    if phone['price'] > budget:
        continue
    if selected_brands and phone['brand'] not in selected_brands:
        continue
        
    # Формула розрахунку зваженого рейтингу
    total_weighted_score = (
        (w_cam * phone['camera']) +
        (w_bat * phone['battery']) +
        (w_perf * phone['performance']) +
        (w_disp * phone['display']) +
        (w_design * phone['design'])
    )
    
    max_possible_score = (w_cam + w_bat + w_perf + w_disp + w_design) * 100
    match_percentage = round((total_weighted_score / max_possible_score) * 100, 1)
    
    # Складний індекс ціна/якість
    value_index = round((total_weighted_score / phone['price']) * 10, 2)
    
    # Створення розширеного об'єкта даних
    phone_entry = phone.copy()
    phone_entry['match'] = match_percentage
    phone_entry['value_index'] = value_index
    processed_phones.append(phone_entry)

# Застосування обраного користувачем типу сортування
if sort_option == "За релевантністю (Матч %)":
    processed_phones.sort(key=lambda x: x['match'], reverse=True)
elif sort_option == "Ціна: від найдешевших":
    processed_phones.sort(key=lambda x: x['price'])
elif sort_option == "Ціна: від найдорожчих":
    processed_phones.sort(key=lambda x: x['price'], reverse=True)
elif sort_option == "Коефіцієнт вигоди (Ціна/Якість)":
    processed_phones.sort(key=lambda x: x['value_index'], reverse=True)


# ==========================================
# 5. СТВОРЕННЯ ВКЛАДОК (TABS) ДЛЯ UX/UI
# ==========================================
tab_recommendations, tab_analytics, tab_comparison = st.tabs([
    "🎯 Ідеальні рекомендації", 
    "📊 Аналітика ринку", 
    "⚔️ Модуль порівняння"
])

# ------------------------------------------
# ВКЛАДКА 1: КАРТКИ РЕКОМЕНДАЦІЙ
# ------------------------------------------
with tab_recommendations:
    if not processed_phones:
        st.info("💡 Немає пристроїв, що задовольняють умови встановлених фільтрів бюджету чи брендів.")
    else:
        st.subheader(f"🔍 Знайдено та проаналізовано моделей: {len(processed_phones)}")
        
        for idx, phone in enumerate(processed_phones, start=1):
            
            # Генерація тегів/бейджів на основі математичних аномалій у залізі
            badges_html = ""
            if idx == 1 and sort_option == "За релевантністю (Матч %)":
                badges_html += '<span class="badge badge-top">🥇 НАЙКРАЩИЙ ВИБІР</span>'
            if phone['value_index'] > 1.8 and phone['price'] < 600:
                badges_html += '<span class="badge badge-value">💎 ТОП ЗА СВОЇ ГРОШІ</span>'
            if phone['camera'] >= 95:
                badges_html += '<span class="badge badge-camera">📸 КАМЕРОФОН</span>'
            if phone['performance'] >= 96:
                badges_html += '<span class="badge badge-gaming">🎮 ЕКСТРЕМАЛЬНА ПОТУЖНІСТЬ</span>'

            # Візуальний контейнер HTML/CSS для картки
            st.markdown(f"""
            <div class="phone-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <h3 style="margin: 0 0 8px 0; color: #ffffff;">{phone['brand']} {phone['model']}</h3>
                        <div style="margin-bottom: 12px;">{badges_html}</div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 24px; font-weight: bold; color: #ff4b4b;">${phone['price']}</span><br>
                        <span style="font-size: 12px; color: #aaa;">Коефіцієнт вигоди: {phone['value_index']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Внутрішні нативні віджети Streamlit для відображення прогресу
            col_progress, col_metrics = st.columns([5, 5])
            with col_progress:
                st.write(f"Загальний збіг з твоїм кастомним профілем: **{phone['match']}%**")
                st.progress(int(phone['match']))
            
            with col_metrics:
                # Візуальні мікро-метрики
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("📸 Камера", f"{phone['camera']}/100")
                m2.metric("🔋 Батарея", f"{phone['battery']}/100")
                m3.metric("🚀 Швидкість", f"{phone['performance']}/100")
                m4.metric("📺 Екран", f"{phone['display']}/100")
                m5.metric("💎 Корпус", f"{phone['design']}/100")
            
            st.markdown('<div style="margin-bottom: 25px;"></div>', unsafe_allow_html=True)

# ------------------------------------------
# ВКЛАДКА 2: ІНТЕРАКТИВНА АНАЛІТИКА ТА ГРАФІКИ
# ------------------------------------------
with tab_analytics:
    st.subheader("📊 Порівняльний аналіз розподілу ціни та якості")
    st.markdown("Ця матриця допомагає візуально виявити аутсайдерів та пристрої з аномально високою вигодою.")
    
    if processed_phones:
        # Перетворюємо поточний набір даних у Pandas DataFrame для побудови графіків
        df = pd.DataFrame(processed_phones)
        
        # Перейменування стовпчиків для гарного відображення на осях графіків
        df_chart = df.rename(columns={
            'price': 'Ціна ($)',
            'match': 'Рейтинг відповідності (%)',
            'value_index': 'Індекс Ціна/Якість',
            'model': 'Модель'
        })
        
        # Будуємо інтерактивний графік розсіювання (Scatter Chart)
        st.scatter_chart(
            df_chart,
            x='Ціна ($)',
            y='Рейтинг відповідності (%)',
            color='brand',
            size='Індекс Ціна/Якість'
        )
        st.caption("ℹ️ Розмір кожної точки на графіку відображає її загальний індекс вигоди (Ціна/Якість). Що вища і лівіша точка — то вигідніший пристрій.")
    else:
        st.warning("Немає даних для побудови графіків аналітики.")

# ------------------------------------------
# ВКЛАДКА 3: МОДУЛЬ ЛОБОВОГО ПОРІВНЯННЯ СМАРТФОНІВ
# ------------------------------------------
with tab_comparison:
    st.subheader("⚔️ Табличне порівняння обраних моделей")
    st.markdown("Познач прапорцями пристрої, які тебе зацікавили, щоб звести їх характеристики в єдину порівняльну таблицю.")
    
    # Користувач самостійно обирає пристрої для порівняння з повної бази
    all_names = [f"{p['brand']} {p['model']}" for p in phones_db]
    selected_for_comp = st.multiselect("Обери моделі для детального порівняння:", all_names, default=all_names[:3] if len(all_names) >= 3 else all_names)
    
    if selected_for_comp:
        comparison_list = []
        for p in phones_db:
            full_name = f"{p['brand']} {p['model']}"
            if full_name in selected_for_comp:
                comparison_list.append({
                    "Смартфон": full_name,
                    "Ціна ($)": p['price'],
                    "📸 Камера (/100)": p['camera'],
                    "🔋 Батарея (/100)": p['battery'],
                    "🚀 Потужність (/100)": p['performance'],
                    "📺 Дисплей (/100)": p['display'],
                    "💎 Дизайн (/100)": p['design']
                })
        
        # Формуємо DataFrame та красиво транспонуємо матрицю для класичного вигляду порівняння
        comp_df = pd.DataFrame(comparison_list).set_index("Смартфон")
        st.dataframe(comp_df.T, use_container_width=True)
    else:
        st.info("Будь ласка, обери хоча б один або два смартфони у полі вище.")
