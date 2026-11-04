# ДОЛЖНО БЫТЬ ВОТ ТАК:
@st.cache_data(ttl=10)
def load_products_from_sheets(url):
    try:
        df = pd.read_csv(url)
        return df.to_dict(orient="records")
    except Exception as e:
        # Если таблица не подключилась, покажем старые товары как запасные:
        return [
            {"id": "ikra_kej", "name": "Икра КЕЖУЧА (100 г, премиум деликатес, стекло)", "price": 98.0, "weight": "100 г", "status": "В наличии", "keywords": "кежуч"},
            {"id": "ikra_gorb", "name": "Икра ГОРБУШИ (100 г, классический стандарт, стекло)", "price": 98.0, "weight": "100 г", "status": "В наличии", "keywords": "горбуш"},
            {"id": "skumbriya", "name": "Скумбрия атлантическая х/к (без головы)", "price": 25.0, "weight": "за 1 кг", "status": "В наличии", "keywords": "скумбр"}
        ]

# Вставь сюда вашу реальную ссылку из Шага 2 (с export?format=csv на конце)
GOOGLE_SHEET_CSV_URL = "ВАША_ССЫЛКА" 

PRODUCTS = load_products_from_sheets(GOOGLE_SHEET_CSV_URL)
