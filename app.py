import streamlit as st
import pandas as pd
import urllib.parse

# 1. Настройка премиальной темы и иконки вкладки
st.set_page_config(
    page_title="Fish Soligorsk — Элитные Морепродукты",
    page_icon="🐟",
    layout="wide"
)

# Инициализация калькулятора в памяти сессии
if "cart" not in st.session_state:
    st.session_state.cart = {}

# Реальные инвайт-ссылки на ваши Вайбер-группы продаж
VIBER_VITRINA_URL = "https://viber.com"  # Ссылка на Рыбу
VIBER_SKLAD_URL = "https://invite.viber.com/?g2=AQBzfd3YM5GHQFHi%2BfK6Csdh%2FDBHkPRlZRqXWCo8McjyuDhZwwNr%2FBumSb9e56qT"    # Ссылка на Склад

# ==============================================================================
# ПОДКЛЮЧЕНИЕ GOOGLE ТАБЛИЦЫ (Автоматизация ассортимента)
# ==============================================================================
# ВПИШИ СЮДА СКОПИРОВАННЫЙ ID СВОЕЙ ТАБЛИЦЫ МЕЖДУ КАВЫЧКАМИ:
SHEET_ID = "1E_PRr6DJm7ccAyAaKbDaKcFoTcr3ith1AamTJduq6fs"
GOOGLE_SHEET_URL = f"https://google.com{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=300)  # Скрипт обновляет кэш из таблицы раз в 5 минут
def load_products():
    try:
        df = pd.read_csv(GOOGLE_SHEET_URL)
        df = df.dropna(subset=['Name', 'Price'])
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0.0)
        return df.to_dict(orient='records')
    except Exception as e:
        # Резервный товар на случай, если ссылка еще не настроена или пустая
        return [{
            "Category": "👑 Премиум Икра",
            "Name": "Икра КЕТЫ «Охотоморье» (Стеклянная банка)",
            "Price": 98.00,
            "Status": "ПРЕДЗАКАЗ",
            "Desc": "🥇 Элитная коллекция, крупное зерно. Цельные глянцевые икринки.",
            "Image": "https://placeholder.co"
        }]

PRODUCTS = load_products()

# ==============================================================================
# КАСТОМНЫЙ CSS (ВАША ПРЕМИАЛЬНАЯ ТЕМА: ГАЛАКТИКА И НЕОН)
# ==============================================================================
st.markdown("""
<style>
    /* Глубокий темно-синий и черный фон всей страницы с эффектом звездного неба */
    .stApp {
        background: linear-gradient(135deg, #030611 0%, #070B19 50%, #0F172E 100%);
        color: #F0F2F6;
    }
    
    /* Золотые премиальные заголовки */
    .gold-header {
        color: #D4AF37 !important;
        font-family: 'Georgia', serif;
        font-weight: bold;
        text-align: center;
        text-shadow: 0px 2px 12px rgba(212, 175, 55, 0.4);
        margin-bottom: 5px;
    }
    
    /* Неоновое фиолетово-голубое описание */
    .sub-header {
        color: #9D4EDD !important;
        text-align: center;
        font-style: italic;
        margin-bottom: 30px;
        text-shadow: 0px 0px 8px rgba(157, 78, 221, 0.3);
    }
    
    /* Стилизация элитных карточек товаров / кнопок */
    .product-box {
        background: rgba(11, 17, 37, 0.7);
        border: 2px solid rgba(157, 78, 221, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(6px);
        transition: all 0.4s ease-in-out;
    }
    
    /* Эффект яркого неонового свечения (Галактический голубой при наведении) */
    .product-box:hover {
        border-color: #00BFFF;
        box-shadow: 0px 0px 25px rgba(0, 191, 255, 0.5);
    }

    .link-card {
        text-decoration: none !important;
        display: block;
    }
    .link-card:hover {
        transform: translateY(-4px);
    }
    
    /* Золотые плашки статуса (В наличии / Предзаказ) */
    .gold-badge {
        background-color: rgba(212, 175, 55, 0.1);
        color: #D4AF37;
        padding: 6px 14px;
        border-radius: 12px;
        border: 1px solid #D4AF37;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 12px;
        font-size: 0.85rem;
        letter-spacing: 1px;
    }

    .card-title-text { font-size: 20px; font-weight: bold; color: #FFFFFF; margin-bottom: 10px; }
    .card-desc-text { color: #A0AABF; font-size: 14px; line-height: 1.5; }
    
    /* Контейнер калькулятора */
    .calc-box {
        background: rgba(0, 191, 255, 0.05);
        border: 1px solid #00BFFF;
        border-radius: 20px;
        padding: 25px;
        margin-top: 40px;
        box-shadow: 0px 0px 20px rgba(0, 191, 255, 0.2);
    }

    /* Подвал сайта */
    .galaxy-footer {
        margin-top: 60px;
        padding: 25px;
        background: rgba(3, 6, 17, 0.9);
        border-top: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 20px;
        text-align: center;
        font-size: 0.9rem;
        color: #A0AABF;
        box-shadow: 0px -5px 20px rgba(0,0,0,0.4);
    }
    
    .dev-badge {
        color: #00BFFF !important;
        font-weight: bold;
        text-shadow: 0px 0px 8px rgba(0, 191, 255, 0.7);
    }
</style>
""", unsafe_allow_html=True)

# --- ХЕДЕР ВИТРИНЫ ---
st.markdown("<h1 class='gold-header'>✨ FISH SOLIGORSK ✨</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>🎄 Открываем предзаказ на новогоднюю премиум-линейку «Охотоморье»! 🎄</p>", unsafe_allow_html=True)

# --- КНОПКИ БЫСТРОГО ПЕРЕХОДА В ГРУППЫ ВАЙБЕР ---
col_l1, col_l2 = st.columns(2)
with col_l1:
    st.markdown(f'<a href="{VIBER_VITRINA_URL}" target="_blank" class="link-card"><div class="product-box"><span class="gold-badge">В НАЛИЧИИ</span><div class="card-title-text">🐬 Рыба и Морепродукты</div><div class="card-desc-text">Свежий розничный ассортимент. Открыть витрину в Viber.</div></div></a>', unsafe_allow_html=True)
with col_l2:
    st.markdown(f'<a href="{VIBER_SKLAD_URL}" target="_blank" class="link-card"><div class="product-box"><span class="gold-badge">ОБНОВЛЕНО</span><div class="card-title-text">📦 Склад / Доставка</div><div class="card-desc-text">Информация о наличии на складе и условиях доставки.</div></div></a>', unsafe_allow_html=True)

st.markdown("<hr style='border-color: rgba(157, 78, 221, 0.2);'>", unsafe_allow_html=True)

# ==============================================================================
# АВТОМАТИЧЕСКАЯ ГЕНЕРАЦИЯ ВКЛАДОК НА ОСНОВЕ КАТЕГОРИЙ ИЗ ТАБЛИЦЫ
# ==============================================================================
unique_categories = sorted(list(set([p['Category'] for p in PRODUCTS if str(p['Category']) != 'nan'])))

if unique_categories:
    tabs = st.tabs(unique_categories)
    
    for tab, cat_name in zip(tabs, unique_categories):
        with tab:
            # Отображаем только активные товары (скрываем статус "ЗАКОНЧИЛСЯ")
            cat_products = [p for p in PRODUCTS if p['Category'] == cat_name and p['Status'] != 'ЗАКОНЧИЛСЯ']
            
            if not cat_products:
                st.info("В данном разделе товары временно распроданы. Ожидаем новое поступление!")
            else:
                for p in cat_products:
                    st.markdown("<div class='product-box'>", unsafe_allow_html=True)
                    col_img, col_desc = st.columns([1, 1.5])
