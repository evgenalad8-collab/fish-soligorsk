import streamlit as st
import re

# Настройка страницы
st.set_page_config(page_title="Fish Soligorsk — Витрина", page_icon="🐟", layout="wide")

# Инициализация корзины в сессии
if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- БАЗА ДАННЫХ ТОВАРОВ (Шаг 2) ---
PRODUCTS = [
    {"id": "ikra_kej", "name": "Икра КЕЖУЧА (100 г, премиум деликатес, стекло)", "price": 98.0, "weight": "100 г"},
    {"id": "ikra_gorb", "name": "Икра ГОРБУШИ (100 г, классический стандарт, стекло)", "price": 98.0, "weight": "100 г"},
    {"id": "skumbriya", "name": "Скумбрия атлантическая х/к (без головы)", "price": 25.0, "weight": "за 1 кг"}
]

# Функция для имитации умного ИИ-парсинга текста заказа
def parse_order_with_ai(text):
    text_lower = text.lower()
    detected_items = []
    
    # Ключевые слова для поиска товаров в тексте
    keywords = {
        "ikra_kej": ["кежуч", "кежуча", "кижуч"],
        "ikra_gorb": ["горбуш", "горбуши", "горбушу"],
        "skumbriya": ["скумбр", "скумбрию", "скумбрия"]
    }
    
    for p_id, keys in keywords.items():
        for key in keys:
            if key in text_lower:
                # Пытаемся найти цифру перед или после ключевого слова для определения количества
                match = re.search(r'(\d+)\s*' + key + r'|' + key + r'\s*(\d+)', text_lower)
                count = 1
                if match:
                    count_str = match.group(1) or match.group(2)
                    if count_str:
                        count = int(count_str)
                
                product = next((p for p in PRODUCTS if p["id"] == p_id), None)
                if product:
                    detected_items.append({"product": product, "count": count})
                break
                
    # Ищем телефон в тексте
    phone_match = re.search(r'(\+?375\s*\(?\d{2}\)?\s*\d{3}-?\d{2}-?\d{2}|\b\d{9}\b)', text)
    phone = phone_match.group(0) if phone_match else "Не указан"
    
    # Ищем адрес (простой поиск по ключевым словам)
    address = "Самовывоз"
    if "доставка" in text_lower or "на ул" in text_lower or "ул." in text_lower or "судиловского" in text_lower:
        # Пытаемся вырезать кусок текста после слова 'доставка' или 'на'
        addr_match = re.search(r'(?:доставка на|доставка:|адрес:)\s*([^,\n.]+)', text, re.IGNORECASE)
        if addr_match:
            address = addr_match.group(1).strip()
        elif "судиловского" in text_lower:
            address = "ул. Судиловского"
            
    return detected_items, phone, address


# --- ШАПКА САЙТА (Шаг 3) ---
st.title("✨ Искусство Вкуса и Качества")
st.caption("Элитная рыба и морепродукты в Солигорске напрямую со склада")
st.info("📞 Viber: +375 (29) 111-22-33 | 📍 Пункт выдачи: Таборы / Солигорск")

st.markdown("### 🟢 Прямо сейчас в наличии на складе:")

# Создаем две колонки: слева товары, справа — корзина
col_products, col_cart = st.columns([2, 1])

# --- ВЫВОД ТОВАРОВ (Шаг 3) ---
with col_products:
    for p in PRODUCTS:
        with st.container(border=True):
            st.markdown(f"#### 🐟 {p['name']}")
            st.markdown(f"**Цена:** {p['price']} руб. ({p['weight']})")
            if st.button(f"Добавить в корзину", key=f"add_{p['id']}"):
                if p['id'] in st.session_state.cart:
                    st.session_state.cart[p['id']] += 1
                else:
                    st.session_state.cart[p['id']] = 1
                st.toast(f"Добавлено: {p['name']}")
                st.rerun()

# --- УМНАЯ КОРЗИНА (Шаг 5) ---
with col_cart:
    st.markdown("### 🛒 Ваша Корзина")
    total_goods_price = 0.0
    
    if not st.session_state.cart:
        st.write("Корзина пока пуста.")
    else:
        for p_id, count in list(st.session_state.cart.items()):
            product = next((p for p in PRODUCTS if p["id"] == p_id), None)
            if product:
                item_total = product["price"] * count
                total_goods_price += item_total
                
                col_item_name, col_item_count = st.columns([4, 1])
                with col_item_name:
                    st.write(f"{product['name']} x{count}")
                with col_item_count:
                    if st.button("❌", key=f"del_{p_id}"):
                        del st.session_state.cart[p_id]
                        st.rerun()
        
        st.markdown("---")
        st.write(f"**Сумма товаров:** {total_goods_price:.2f} руб.")
        
        if total_goods_price < 120.0:
            delivery_price = 10.0
            st.error(f"🚚 Доставка: {delivery_price} руб. (Добавьте еще на {120.0 - total_goods_price:.2f} руб. до БЕСПЛАТНОЙ)")
        else:
            delivery_price = 0.0
            st.success("🚚 Доставка: Бесплатно!")
            
        total_order_price = total_goods_price + delivery_price
        st.markdown(f"### 🔥 Итого: {total_order_price:.2f} руб.")
        
        if st.button("Очистить корзину"):
            st.session_state.cart = {}
            st.rerun()

st.markdown("---")

# ==========================================
# ШАГ 6. ИНТЕГРАЦИЯ ФОРМЫ ЗАКАЗА И ИИ-ЧЕКА
# ==========================================
st.markdown("### 🧠 Умное оформление заказа за 1 секунду")
st.write("Просто скопируйте сюда сообщение клиента из Viber чата. Нейросеть сама поймет, какие это товары, найдет телефон и адрес.")

# Поле для ввода сырого текста
user_raw_text = st.text_area(
    "Вставьте текст заказа или сообщение из чата сюда:", 
    value="мне плиз 2 банки горбуши и одну скумбрию. Доставка на Судиловского 5 кв 12 т +375291112233",
    height=100
)

if st.button("🔮 Сформировать красивый чек с помощью ИИ"):
    if user_raw_text.strip() == "":
        st.warning("Пожалуйста, введите текст сообщения.")
    else:
        # Запускаем наш ИИ-парсер
        items, phone, address = parse_order_with_ai(user_raw_text)
        
        if not items:
            st.error("🤖 ИИ не смог распознать товары в тексте. Проверьте правильность написания названий (икра, скумбрия).")
        else:
            st.success("🤖 Текст успешно распознан нейросетью!")
            
            # Начинаем формировать идеальный текстовый чек
            receipt = []
            receipt.append("🧾 ------ ФИРМЕННЫЙ ЧЕК FISH SOLIGORSK ------")
            
            total_ai_price = 0.0
            for item in items:
                p = item["product"]
                c = item["count"]
                cost = p["price"] * c
                total_ai_price += cost
                receipt.append(f"🔹 {p['name']} х{c} = {cost:.2f} руб.")
            
            receipt.append("------------------------------------------")
            receipt.append(f"💰 Сумма товаров: {total_ai_price:.2f} руб.")
            
            # Считаем доставку для ИИ-чека
            if total_ai_price < 120.0:
                ai_delivery = 10.0
                receipt.append(f"🚚 Доставка: {ai_delivery}.00 руб.")
            else:
                ai_delivery = 0.0
                receipt.append("🚚 Доставка: БЕСПЛАТНО")
            receipt.append(f"💵 ИТОГО К ОПЛАТЕ: {total_ai_price + ai_delivery:.2f} руб.")
            receipt.append("------------------------------------------")
            receipt.append(f"📞 Телефон клиента: {phone}")
            receipt.append(f"🏠 Адрес/Способ получения: {address}")
            receipt.append("------------------------------------------")
            receipt.append("🙏 Спасибо за заказ! Ждем вас снова!")
            final_receipt_text = "\n".join(receipt)
            st.markdown("#### ✅ Сгенерированный чек (можно скопировать одной кнопкой):")
            st.code(final_receipt_text, language="text")
            
            st.info("💡 Теперь этот аккуратный чек Женя может вставить обратно в чат клиенту или переслать в закрытый Телеграм-канал для сборщика заказов!")
