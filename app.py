import streamlit as st
import json
import pandas as pd

# ==========================================
# 1. МУЛЬТИМОВНА СИСТЕМА ЛОКАЛІЗАЦІЇ
# ==========================================
LANGUAGES = {
    "UA": {
        "title": "⚡ Професійна екосистема аналізу та підбору смартфонів",
        "subtitle": "Величезний інтерактивний каталог пристроїв з розумним алгоритмом скорингу.",
        "sidebar_header": "🎛️ Панель керування",
        "budget": "💰 Граничний бюджет ($)",
        "brands": "🏷️ Вибір брендів (усі, якщо порожньо)",
        "sorting": "📊 Сортування результатів",
        "sort_options": ["За релевантністю (Матч %)", "Ціна: від найдешевших", "Ціна: від найдорожчих", "Коефіцієнт вигоди"],
        "weights_title": "⚖️ Вага критеріїв оцінки",
        "weights_caption": "Змінюй пріоритети, щоб миттєво перебудувати математичну модель",
        "w_cam": "📸 Фото та відео можливості",
        "w_bat": "🔋 Автономність та енергоефективність",
        "w_perf": "🚀 Обчислювальна потужність (чипсет)",
        "w_disp": "📺 Технологічність дисплея",
        "w_design": "💎 Преміальність матеріалів та дизайн",
        "tab_rec": "🎯 Ідеальні рекомендації",
        "tab_an": "📊 Аналітика ринку",
        "tab_comp": "⚔️ Модуль порівняння",
        "no_results": "💡 Немає пристроїв, що задовольняють умови встановлених фільтрів бюджету чи брендів.",
        "found_models": "🔍 Знайдено та проаналізовано моделей: ",
        "match_profile": "Загальний збіг: ",
        "value_idx": "Коефіцієнт вигоди",
        "chart_title": "📊 Порівняльний аналіз розподілу ціни та якості",
        "chart_desc": "Ця матриця допомагає візуально виявити аутсайдерів та пристрої з аномально високою вигодою.",
        "chart_caption": "ℹ️ Розмір точки відображає її індекс вигоди (Ціна/Якість). Що вища і лівіша точка — то вигідніший пристрій.",
        "comp_title": "⚔️ Табличне порівняння обраних моделей",
        "comp_desc": "Познач пристрої, які тебе зацікавили, щоб звести їх характеристики в єдину порівняльну таблицю.",
        "comp_select": "Обери моделі для детального порівняння:",
        "comp_empty": "Будь ласка, обери хоча б один або два смартфони у полі вище.",
        "m_cam": "📸 Камера", "m_bat": "🔋 Батарея", "m_perf": "🚀 Швидкість", "m_disp": "📺 Екран", "m_design": "💎 Корпус",
        "chart_x": "Ціна ($)", "chart_y": "Рейтинг відповідності (%)", "chart_size": "Індекс Ціна/Якість", "chart_model": "Модель",
        "t_phone": "Смартфон", "t_price": "Ціна ($)"
    },
    "EN": {
        "title": "⚡ Professional Smartphone Analyzer & Picker",
        "subtitle": "Massive device catalog driven by smart weighted scoring algorithms.",
        "sidebar_header": "🎛️ Control Panel",
        "budget": "💰 Maximum Budget ($)",
        "brands": "🏷️ Brand Selection (all if empty)",
        "sorting": "📊 Sort Results By",
        "sort_options": ["By Relevance (Match %)", "Price: Low to High", "Price: High to Low", "Value for Money Index"],
        "weights_title": "⚖️ Criteria Evaluation Weights",
        "weights_caption": "Modify priorities to instantly rebuild the mathematical model",
        "w_cam": "📸 Photo & Video Capabilities",
        "w_bat": "🔋 Battery Life & Efficiency",
        "w_perf": "🚀 Computing Power (Chipset)",
        "w_disp": "📺 Display Technology",
        "w_design": "💎 Premium Materials & Design",
        "tab_rec": "🎯 Top Recommendations",
        "tab_an": "📊 Market Analytics",
        "tab_comp": "⚔️ Comparison Module",
        "no_results": "💡 No devices match the specified budget or brand filters.",
        "found_models": "🔍 Models found and analyzed: ",
        "match_profile": "Total match: ",
        "value_idx": "Value Index",
        "chart_title": "📊 Price vs. Quality Distribution Analysis",
        "chart_desc": "This matrix helps visually identify market outsiders and devices with anomaly-high value.",
        "chart_caption": "ℹ️ Dot size represents Value for Money. The higher and further left, the better the deal.",
        "comp_title": "⚔️ Tabular Comparison of Selected Models",
        "comp_desc": "Select the devices you are interested in to generate a unified comparison matrix.",
        "comp_select": "Select models for deep comparison:",
        "comp_empty": "Please select at least one or two smartphones in the field above.",
        "m_cam": "📸 Camera", "m_bat": "🔋 Battery", "m_perf": "🚀 Speed", "m_disp": "📺 Display", "m_design": "💎 Design",
        "chart_x": "Price ($)", "chart_y": "Match Rating (%)", "chart_size": "Value for Money Index", "chart_model": "Model",
        "t_phone": "Smartphone", "t_price": "Price ($)"
    },
    "CZ": {
        "title": "⚡ Profesionální ekosystém analýzy a výběru smartphonů",
        "subtitle": "Masivní katalog reálných zařízení s inteligentním algoritmem skórování.",
        "sidebar_header": "🎛️ Ovládací panel",
        "budget": "💰 Maximální rozpočet ($)",
        "brands": "🏷️ Výběr značek (všechny pokud prázdné)",
        "sorting": "📊 Seřadit výsledky podle",
        "sort_options": ["Podle relevance (Shoda %)", "Cena: od nejlevnějších", "Cena: od nejdražších", "Index cena/výkon"],
        "weights_title": "⚖️ Váha hodnotících kritérií",
        "weights_caption": "Změňte priority pro okamžité přepočítání matematického modelu",
        "w_cam": "📸 Foto a video schopnosti",
        "w_bat": "🔋 Výdrž baterie a efektivita",
        "w_perf": "🚀 Výpočetní výkon (Čipset)",
        "w_disp": "📺 Technologie displeje",
        "w_design": "💎 Prémiové materiály a design",
        "tab_rec": "🎯 Ideální doporučení",
        "tab_an": "📊 Tržní analýza",
        "tab_comp": "⚔️ Srovnávací modul",
        "no_results": "💡 Žádná zařízení nevyhovují stanoveným filtrům rozpočtu nebo značek.",
        "found_models": "🔍 Nalezené a analyzované modely: ",
        "match_profile": "Celková shoda: ",
        "value_idx": "Index výhodnosti",
        "chart_title": "📊 Analýza distribuce ceny a kvality",
        "chart_desc": "Tato matice pomáhá vizuálně identifikovat outsidery a zařízení s anomálně vysokou hodnotou.",
        "chart_caption": "ℹ️ Velikost bodu představuje index cena/výkon. Čím vyšší a více vlevo bod je, tím je výhodnější.",
        "comp_title": "⚔️ Tabulkové srovnání vybraných modelů",
        "comp_desc": "Zaškrtněte zařízení, která vás zajímají, abyste sestavili jednotnou srovnávací tabulku.",
        "comp_select": "Vyberte modely pro detailní srovnání:",
        "comp_empty": "Vyberte prosím alespoň jeden nebo dva smartphony v poli výše.",
        "m_cam": "📸 Fotoaparát", "m_bat": "🔋 Baterie", "m_perf": "🚀 Výkon", "m_disp": "📺 Displej", "m_design": "💎 Design",
        "chart_x": "Cena ($)", "chart_y": "Shoda (%)", "chart_size": "Index Cena/Kvalita", "chart_model": "Model",
        "t_phone": "Smartphone", "t_price": "Cena ($)"
    }
}

# ==========================================
# 2. ОНОВЛЕНА РЕАЛЬНА БАЗА ДАНИХ (ТОЧНІ КАРТИНКИ)
# ==========================================
phones_db = [
    # APPLE
    {"brand": "Apple", "model": "iPhone 16 Pro Max", "price": 1250, "camera": 98, "battery": 90, "performance": 98, "display": 99, "design": 98, "img": "https://images.officialrenders.com/smartphones/apple/iphone-16-pro-max.png"},
    {"brand": "Apple", "model": "iPhone 16 Pro", "price": 1050, "camera": 97, "battery": 85, "performance": 98, "display": 98, "design": 98, "img": "https://images.officialrenders.com/smartphones/apple/iphone-16-pro.png"},
    {"brand": "Apple", "model": "iPhone 16", "price": 820, "camera": 87, "battery": 80, "performance": 89, "display": 85, "design": 93, "img": "https://images.officialrenders.com/smartphones/apple/iphone-16.png"},
    {"brand": "Apple", "model": "iPhone 15", "price": 680, "camera": 84, "battery": 78, "performance": 83, "display": 84, "design": 90, "img": "https://images.officialrenders.com/smartphones/apple/iphone-15.png"},
    
    # SAMSUNG
    {"brand": "Samsung", "model": "Galaxy S26 Ultra", "price": 1350, "camera": 99, "battery": 94, "performance": 99, "display": 100, "design": 97, "img": "https://images.officialrenders.com/smartphones/samsung/galaxy-s26-ultra.png"},
    {"brand": "Samsung", "model": "Galaxy S26+", "price": 1000, "camera": 92, "battery": 89, "performance": 95, "display": 97, "design": 94, "img": "https://images.officialrenders.com/smartphones/samsung/galaxy-s26-plus.png"},
    {"brand": "Samsung", "model": "Galaxy S25", "price": 750, "camera": 89, "battery": 82, "performance": 93, "display": 95, "design": 92, "img": "https://images.officialrenders.com/smartphones/samsung/galaxy-s25.png"},
    {"brand": "Samsung", "model": "Galaxy A55 5G", "price": 370, "camera": 75, "battery": 89, "performance": 71, "display": 86, "design": 83, "img": "https://images.officialrenders.com/smartphones/samsung/galaxy-a55.png"},
    {"brand": "Samsung", "model": "Galaxy A35 5G", "price": 270, "camera": 66, "battery": 88, "performance": 62, "display": 81, "design": 78, "img": "https://images.officialrenders.com/smartphones/samsung/galaxy-a35.png"},
    {"brand": "Samsung", "model": "Galaxy A16 5G", "price": 180, "camera": 48, "battery": 86, "performance": 45, "display": 72, "design": 60, "img": "https://images.officialrenders.com/smartphones/samsung/galaxy-a16.png"},
    
    # MOTOROLA (Суттєво розширено)
    {"brand": "Motorola", "model": "Edge 50 Ultra", "price": 890, "camera": 93, "battery": 86, "performance": 94, "display": 97, "design": 99, "img": "https://images.officialrenders.com/smartphones/motorola/edge-50-ultra.png"},
    {"brand": "Motorola", "model": "Edge 50 Pro", "price": 550, "camera": 87, "battery": 85, "performance": 85, "display": 95, "design": 96, "img": "https://images.officialrenders.com/smartphones/motorola/edge-50-pro.png"},
    {"brand": "Motorola", "model": "Edge 50 Fusion", "price": 340, "camera": 81, "battery": 90, "performance": 73, "display": 91, "design": 92, "img": "https://images.officialrenders.com/smartphones/motorola/edge-50-fusion.png"},
    {"brand": "Motorola", "model": "Moto G85 5G", "price": 250, "camera": 73, "battery": 92, "performance": 66, "display": 88, "design": 86, "img": "https://images.officialrenders.com/smartphones/motorola/moto-g85.png"},
    {"brand": "Motorola", "model": "Moto G55 5G", "price": 190, "camera": 68, "battery": 93, "performance": 60, "display": 79, "design": 78, "img": "https://images.officialrenders.com/smartphones/motorola/moto-g55.png"},
    {"brand": "Motorola", "model": "Moto G35 5G", "price": 140, "camera": 50, "battery": 91, "performance": 51, "display": 74, "design": 72, "img": "https://images.officialrenders.com/smartphones/motorola/moto-g35.png"},
    
    # ONEPLUS (Реальні актуальні моделі)
    {"brand": "OnePlus", "model": "13", "price": 820, "camera": 94, "battery": 97, "performance": 99, "display": 98, "design": 93, "img": "https://images.officialrenders.com/smartphones/oneplus/oneplus-13.png"},
    {"brand": "OnePlus", "model": "12", "price": 680, "camera": 91, "battery": 93, "performance": 94, "display": 97, "design": 91, "img": "https://images.officialrenders.com/smartphones/oneplus/oneplus-12.png"},
    {"brand": "OnePlus", "model": "12R", "price": 490, "camera": 78, "battery": 96, "performance": 92, "display": 94, "design": 88, "img": "https://images.officialrenders.com/smartphones/oneplus/oneplus-12r.png"},
    {"brand": "OnePlus", "model": "Nord 4", "price": 410, "camera": 77, "battery": 94, "performance": 85, "display": 89, "design": 92, "img": "https://images.officialrenders.com/smartphones/oneplus/nord-4.png"},
    
    # GOOGLE
    {"brand": "Google", "model": "Pixel 9 Pro XL", "price": 1050, "camera": 100, "battery": 86, "performance": 90, "display": 98, "design": 95, "img": "https://images.officialrenders.com/smartphones/google/pixel-9-pro-xl.png"},
    {"brand": "Google", "model": "Pixel 9 Pro", "price": 950, "camera": 99, "battery": 84, "performance": 90, "display": 96, "design": 95, "img": "https://images.officialrenders.com/smartphones/google/pixel-9-pro.png"},
    {"brand": "Google", "model": "Pixel 9", "price": 750, "camera": 93, "battery": 83, "performance": 88, "display": 91, "design": 92, "img": "https://images.officialrenders.com/smartphones/google/pixel-9.png"},
    {"brand": "Google", "model": "Pixel 8a", "price": 460, "camera": 90, "battery": 80, "performance": 83, "display": 88, "design": 84, "img": "https://images.officialrenders.com/smartphones/google/pixel-8a.png"},
    
    # XIAOMI & POCO
    {"brand": "Xiaomi", "model": "14 Ultra", "price": 1090, "camera": 98, "battery": 88, "performance": 96, "display": 97, "design": 94, "img": "https://images.officialrenders.com/smartphones/xiaomi/xiaomi-14-ultra.png"},
    {"brand": "Xiaomi", "model": "14T Pro", "price": 680, "camera": 91, "battery": 89, "performance": 95, "display": 95, "design": 89, "img": "https://images.officialrenders.com/smartphones/xiaomi/xiaomi-14t-pro.png"},
    {"brand": "Xiaomi", "model": "POCO F6 Pro", "price": 470, "camera": 76, "battery": 88, "performance": 94, "display": 94, "design": 82, "img": "https://images.officialrenders.com/smartphones/xiaomi/poco-f6-pro.png"},
    {"brand": "Xiaomi", "model": "POCO X6 Pro 5G", "price": 290, "camera": 68, "battery": 90, "performance": 86, "display": 90, "design": 79, "img": "https://images.officialrenders.com/smartphones/xiaomi/poco-x6-pro.png"},
    {"brand": "Xiaomi", "model": "Redmi Note 13 Pro+ 5G", "price": 330, "camera": 80, "battery": 87, "performance": 70, "display": 89, "design": 85, "img": "https://images.officialrenders.com/smartphones/xiaomi/redmi-note-13-pro-plus.png"},
    
    # REALME
    {"brand": "Realme", "model": "GT 6", "price": 530, "camera": 84, "battery": 96, "performance": 93, "display": 95, "design": 88, "img": "https://images.officialrenders.com/smartphones/realme/realme-gt-6.png"},
    {"brand": "Realme", "model": "13 Pro+", "price": 390, "camera": 83, "battery": 91, "performance": 75, "display": 90, "design": 91, "img": "https://images.officialrenders.com/smartphones/realme/realme-13-pro-plus.png"},
    {"brand": "Realme", "model": "C67", "price": 160, "camera": 51, "battery": 91, "performance": 48, "display": 74, "design": 76, "img": "https://images.officialrenders.com/smartphones/realme/realme-c67.png"},
    
    # HONOR, NOTHING, ASUS
    {"brand": "Honor", "model": "Magic6 Pro", "price": 880, "camera": 97, "battery": 95, "performance": 96, "display": 97, "design": 94, "img": "https://images.officialrenders.com/smartphones/honor/magic6-pro.png"},
    {"brand": "Nothing", "model": "Phone (2a)", "price": 320, "camera": 76, "battery": 90, "performance": 74, "display": 88, "design": 96, "img": "https://images.officialrenders.com/smartphones/nothing/phone-2a.png"},
    {"brand": "Asus", "model": "ROG Phone 8 Pro", "price": 1050, "camera": 79, "battery": 94, "performance": 100, "display": 96, "design": 91, "img": "https://images.officialrenders.com/smartphones/asus/rog-phone-8-pro.png"}
]

# ==========================================
# 3. НАЛАШТУВАННЯ СТОРІНКИ ТА CSS СТИЛІ
# ==========================================
st.set_page_config(page_title="Smart Phone Picker Pro", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .phone-card {
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    .badge {
        padding: 5px 11px;
        border-radius: 8px;
        font-size: 11px;
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

# ==========================================
# 4. СЕЛЕКТОР МОВИ ТА ДИНАМІЧНИЙ ІНТЕРФЕЙС
# ==========================================
lang_code = st.sidebar.selectbox("🌐 Language / Мова / Jazyk", ["UA", "EN", "CZ"])
t = LANGUAGES[lang_code]

st.title(t["title"])
st.markdown(t["subtitle"])
st.write("---")

# Бічна панель
st.sidebar.header(t["sidebar_header"])
budget = st.sidebar.slider(t["budget"], min_value=100, max_value=1500, value=800, step=50)

available_brands = sorted(list(set(phone['brand'] for phone in phones_db)))
selected_brands = st.sidebar.multiselect(t["brands"], available_brands)

sort_option = st.sidebar.selectbox(t["sorting"], t["sort_options"])

st.sidebar.write("---")
st.sidebar.subheader(t["weights_title"])
st.sidebar.caption(t["weights_caption"])

w_cam = st.sidebar.slider(t["w_cam"], 1, 5, 3)
w_bat = st.sidebar.slider(t["w_bat"], 1, 5, 3)
w_perf = st.sidebar.slider(t["w_perf"], 1, 5, 3)
w_disp = st.sidebar.slider(t["w_disp"], 1, 5, 3)
w_design = st.sidebar.slider(t["w_design"], 1, 5, 2)

# ==========================================
# 5. МАТЕМАТИЧНЕ ОБЧИСЛЮВАЛЬНЕ ЯДРО
# ==========================================
processed_phones = []

for phone in phones_db:
    if phone['price'] > budget:
        continue
    if selected_brands and phone['brand'] not in selected_brands:
        continue
        
    total_weighted_score = (
        (w_cam * phone['camera']) +
        (w_bat * phone['battery']) +
        (w_perf * phone['performance']) +
        (w_disp * phone['display']) +
        (w_design * phone['design'])
    )
    
    max_possible_score = (w_cam + w_bat + w_perf + w_disp + w_design) * 100
    match_percentage = round((total_weighted_score / max_possible_score) * 100, 1)
    value_index = round((total_weighted_score / phone['price']) * 10, 2)
    
    phone_entry = phone.copy()
    phone_entry['match'] = match_percentage
    phone_entry['value_index'] = value_index
    processed_phones.append(phone_entry)

# Сортування
if sort_option == t["sort_options"][0]:
    processed_phones.sort(key=lambda x: x['match'], reverse=True)
elif sort_option == t["sort_options"][1]:
    processed_phones.sort(key=lambda x: x['price'])
elif sort_option == t["sort_options"][2]:
    processed_phones.sort(key=lambda x: x['price'], reverse=True)
elif sort_option == t["sort_options"][3]:
    processed_phones.sort(key=lambda x: x['value_index'], reverse=True)

# ==========================================
# 6. ВІДОБРАЖЕННЯ ІНТЕРФЕЙСУ (ВКЛАДКИ)
# ==========================================
tab_recommendations, tab_analytics, tab_comparison = st.tabs([
    t["tab_rec"], t["tab_an"], t["tab_comp"]
])

# Вкладка 1: Картки рекомендацій з точними фото
with tab_recommendations:
    if not processed_phones:
        st.info(t["no_results"])
    else:
        st.subheader(f"{t['found_models']}{len(processed_phones)}")
        
        for idx, phone in enumerate(processed_phones, start=1):
            badges_html = ""
            if idx == 1 and sort_option == t["sort_options"][0]:
                badges_html += f'<span class="badge badge-top">🥇 {"НАЙКРАЩИЙ ВИБІР" if lang_code=="UA" else "TOP CHOICE" if lang_code=="EN" else "NEJLEPŠÍ VOLBA"}</span>'
            if phone['value_index'] > 2.2 and phone['price'] < 500:
                badges_html += f'<span class="badge badge-value">💎 {"ТОП ЗА СВОЇ ГРОШІ" if lang_code=="UA" else "BEST VALUE" if lang_code=="EN" else "TOP ZA TY PENÍZE"}</span>'
            if phone['camera'] >= 95:
                badges_html += f'<span class="badge badge-camera">📸 {"КАМЕРОФОН" if lang_code=="UA" else "CAMERAPHONE" if lang_code=="EN" else "FOTOMOBIL"}</span>'
            if phone['performance'] >= 95:
                badges_html += f'<span class="badge badge-gaming">🎮 {"ЕКСТРЕМАЛЬНА ПОТУЖНІСТЬ" if lang_code=="UA" else "EXTREME POWER" if lang_code=="EN" else "EXTRÉMNÍ VÝKON"}</span>'

            st.markdown(f"""
            <div class="phone-card">
                <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center;">
                    <div style="flex: 1; min-width: 100px; max-width: 130px; text-align: center;">
                        <img src="{phone['img']}" style="max-width: 100%; height: auto; border-radius: 8px;" onerror="this.src='https://images.officialrenders.com/smartphones/generic-phone.png'">
                    </div>
                    <div style="flex: 4; min-width: 250px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                            <div>
                                <h3 style="margin: 0 0 8px 0;">{phone['brand']} {phone['model']}</h3>
                                <div style="margin-bottom: 12px;">{badges_html}</div>
                            </div>
                            <div style="text-align: right;">
                                <span style="font-size: 26px; font-weight: bold; color: #ff4b4b;">${phone['price']}</span><br>
                                <span style="font-size: 11px; opacity: 0.7;">{t['value_idx']}: {phone['value_index']}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_progress, col_metrics = st.columns([4, 6])
            with col_progress:
                st.write(f"{t['match_profile']}**{phone['match']}%**")
                st.progress(int(phone['match']))
            
            with col_metrics:
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric(t["m_cam"], f"{phone['camera']}")
                m2.metric(t["m_bat"], f"{phone['battery']}")
                m3.metric(t["m_perf"], f"{phone['performance']}")
                m4.metric(t["m_disp"], f"{phone['display']}")
                m5.metric(t["m_design"], f"{phone['design']}")
            
            st.markdown('<hr style="margin: 20px 0; border-style: dashed; opacity: 0.3;">', unsafe_allow_html=True)

# Вкладка 2: Інтерактивна аналітика
with tab_analytics:
    st.subheader(t["chart_title"])
    st.markdown(t["chart_desc"])
    
    if processed_phones:
        df = pd.DataFrame(processed_phones)
        df_chart = df.rename(columns={
            'price': t['chart_x'],
            'match': t['chart_y'],
            'value_index': t['chart_size'],
            'model': t['chart_model']
        })
        
        st.scatter_chart(
            df_chart,
            x=t['chart_x'],
            y=t['chart_y'],
            color='brand',
            size=t['chart_size']
        )
        st.caption(t["chart_caption"])
    else:
        st.warning(t["no_results"])

# Вкладка 3: Модуль порівняння
with tab_comparison:
    st.subheader(t["comp_title"])
    st.markdown(t["comp_desc"])
    
    all_names = [f"{p['brand']} {p['model']}" for p in phones_db]
    selected_for_comp = st.multiselect(t["comp_select"], all_names, default=all_names[:3] if len(all_names) >= 3 else all_names)
    
    if selected_for_comp:
        comparison_list = []
        for p in phones_db:
            full_name = f"{p['brand']} {p['model']}"
            if full_name in selected_for_comp:
                comparison_list.append({
                    t["t_phone"]: full_name,
                    t["t_price"]: p['price'],
                    f"{t['m_cam']} (/100)": p['camera'],
                    f"{t['m_bat']} (/100)": p['battery'],
                    f"{t['m_perf']} (/100)": p['performance'],
                    f"{t['m_disp']} (/100)": p['display'],
                    f"{t['m_design']} (/100)": p['design']
                })
        
        comp_df = pd.DataFrame(comparison_list).set_index(t["t_phone"])
        st.dataframe(comp_df.T, use_container_width=True)
    else:
        st.info(t["comp_empty"])
