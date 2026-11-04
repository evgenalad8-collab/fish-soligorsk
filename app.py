import streamlit as st
import re

st.set_page_config(page_title="Fish Soligorsk — Панель заказов", page_icon="🐟", layout="wide")

# =========================================================================
# ВАШ СПИСОК ТОВАРОВ (Вы можете сами добавлять сюда строки по аналогии)
# =========================================================================
PRODUCTS = [
    {"id": "ikra_kej", "name": "Икра КЕЖУЧА (100 г, премиум деликатес, стекло)", "price": 98.0, "weight": "100 г", "status": "В наличии", "keywords": "кежуч, кежуча, кижуч"},
    {"id": "ikra_gorb", "name": "Икра ГОРБУШИ (100 г, классический стандарт, стекло)", "price": 98.0, "weight": "100 г", "status": "В наличии", "keywords": "горбуша, горбуши, горбушу"},
    {"id": "skumbriya", "name": "Скумбрия атлантическая х/к (без головы)", "price": 25.0, "weight": "за 1 кг", "status": "В наличии", "keywords": "скумбрия, скумбрию"},
    {"id": "shrimp_king", "name": "Креветки КОРОЛЕВСКИЕ варено-мороженые VICI (50/70)", "price": 26.21, "weight": "за 1 кг", "status": "В наличии", "keywords": "королевские, вичи, креветки"},
    {"id": "seld_matje", "name": "Сельдь Матье слабосоленая (Норвегия)", "price": 18.72, "weight": "за 1 кг", "status": "В наличии", "keywords": "сельд, селедка, матье"},
    {"id": "file_tunca", "name": "Филе ТУНЦА (Лоины) премиум (Вьетнам)", "price": 45.0, "weight": "за 1 кг", "status": "В наличии", "keywords": "тунец, тунца, лоины"}
]

# Инициализация корзины
if "cart" not in st.session_state:
    st.session_state.cart = {}

# Умная функция ИИ-парсинга
def parse_order_with_ai(text):
    text_lower = text.lower()
    detected_items = []
    
    for product in PRODUCTS:
        keys = [k.strip() for k in product['keywords'].split(',')]
        for key in keys:
            if key and key in text_lower:
                match = re.search(r'(\d+)\s*' + key + r'|' + key + r'\s*(\d+)', text_lower)
                count = 1
                if match:
                    count_str = match.group(1) or match.group(2)
                    if count_str:
                        count = int(count_str)
                
                detected_items.append({"product": product, "count": count})
                break
                
    phone_match = re.search(r'(\+?375\s*\(?\d{2}\)?\s*\d{3}-?\d{2}-?\d{2}|\b\d{9}\b)', text)
    phone = phone_match.group(0) if phone_match else "Не указан"
    
    address = "Самовывоз"
    if any(word in text_lower for word in ["доставка", "на ул", "ул.", "судиловского"]):
        addr_match = re.search(r'(?:доставка на|доставка:|адрес:)\s*([^,\n.]+)', text, re.IGNORECASE)
        if addr_match:
            address = addr_match.group(1).strip()
            
    return detected_items, phone, address

# --- ИНТЕРФЕЙС ПРИЛОЖЕНИЯ ---
st.title("✨ Автоматическая панель Fish Soligorsk")
st.caption("Мини-сайт для быстрой сборки заказов из Viber")

col_products, col_cart = st.columns()

with col_products:
    st.markdown("### 📦 Товары в наличии:")
    available_products = [p for p in PRODUCTS if p['status'] == "В наличии"]
    
    for p in available_products:
        with st.container(border=True):
            st.markdown(f"#### 🐟 {p['name']}")
            st.markdown(f"**Цена:** {p['price']} руб. ({p['weight']})")
            if st.button(f"Добавить в корзину", key=f"add_{p['id']}"):
                if p['id'] in st.session_state.cart:
                    st.session_state.cart[p['id']] += 1
                else:
                    st.session_state.cart[p['id']] = 1
                st.toast(f"Добавлено!")
                st.rerun()

with col_cart:
    st.markdown("### 🛒 Ваша Корзина")
    total_goods_price = 0.0
    
    if not st.session_state.cart:
        st.write("Корзина пуста.")
    else:
        for p_id, count in list(st.session_state.cart.items()):
            product = next((p for p in PRODUCTS if p["id"] == p_id), None)
            if product:
                item_total = product["price"] * count
                total_goods_price += item_total
                
                col_item_name, col_item_count = st.columns()
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
            st.error(f"🚚 Доставка: {delivery_price} руб. (До БЕСПЛАТНОЙ осталось {120.0 - total_goods_price:.2f} руб.)")
        else:
            delivery_price = 0.0
            st.success("🚚 Доставка: Бесплатно!")
            
        st.markdown(f"### 🔥 Итого: {total_goods_price + delivery_price:.2f} руб.")

st.markdown("---")
st.markdown("### 🧠 Умное оформление заказа за 1 секунду")
user_raw_text = st.text_area("Вставьте текст из Viber чата сюда:", height=100)

if st.button("🔮 Сформировать красивый чек"):
    if user_raw_text.strip() == "":
        st.warning("Введите текст заказа.")
    else:
        items, phone, address = parse_order_with_ai(user_raw_text)
        if not items:
            st.error("🤖 Товары в тексте не найдены.")
        else:
            receipt = ["🧾 ------ ФИРМЕННЫЙ ЧЕК FISH SOLIGORSK ------"]
            total_ai_price = 0.0
            for item in items:
                p = item["product"]
                c = item["count"]
                cost = p["price"] * c
                total_ai_price += cost
                receipt.append(f"🔹 {p['name']} х{c} = {cost:.2f} руб.")
            
            receipt.append("------------------------------------------")
            receipt.append(f"💰 Сумма товаров: {total_ai_price:.2f} руб.")
            ai_delivery = 10.0 if total_ai_price < 120.0 else 0.0
            receipt.append(f"🚚 Доставка: {'БЕСПЛАТНО' if ai_delivery == 0 else f'{ai_delivery:.2f} руб.'}")
            receipt.append(f"💵 ИТОГО К ОПЛАТЕ: {total_ai_price + ai_delivery:.2f} руб.")
            receipt.append("------------------------------------------")
            receipt.append(f"📞 Телефон: {phone}\n🏠 Адрес: {address}")
            receipt.append("------------------------------------------\n🙏 Спасибо за заказ!")
            
            st.code("\n".join(receipt), language="text")
