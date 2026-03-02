import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы
st.set_page_config(page_title="LEX ROMANA: GEMINI", page_icon="🏛️", layout="centered")

# 2. Римский дизайн (Золото и Пурпур)
st.markdown("""
    <style>
    .main { background-color: #f4f1ea; }
    .roman-header { color: #66023C; text-align: center; border-bottom: 3px double #d4af37; font-family: 'Times New Roman', serif; text-transform: uppercase; }
    .parchment { background-color: #fcf5e5; border-left: 10px solid #66023C; padding: 25px; font-size: 20px; color: #1a1a1a; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #66023C 0%, #d4af37 100%); color: white; font-weight: bold; height: 4em; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 3. Подключение Gemini
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Выбор языка
lang = st.sidebar.selectbox("Linguam elige / Тил", ("O'zbekcha (Lotin)", "Ўзбекча (Кирилл)", "Русский"))

# Строгая инструкция
base_instruction = "Ты — Верховный Юрист Узбекистана. Отвечай СТРОГО по статьям Lex.uz. Не отправляй пользователя искать в интернете."

if lang == "O'zbekcha (Lotin)":
    title, label, btn = "LEX ROMANA: ADVOKAT", "Vaziyatni yozing:", "VERDIKT"
    prompt = base_instruction + " Javobni Lotin alifbosida yoz."
elif lang == "Ўзбекча (Кирилл)":
    title, label, btn = "LEX ROMANA: АДВОКАТ", "Вазиятни ёзинг:", "ҲУКМ"
    prompt = base_instruction + " Жавобни Кирилл алифбосида ёз."
else:
    title, label, btn = "LEX ROMANA: АДВОКАТ", "Опишите ситуацию:", "ВЕРДИКТ"
    prompt = base_instruction + " Отвечай на русском языке."

st.markdown(f"<h1 class='roman-header'>{title}</h1>", unsafe_allow_html=True)
query = st.text_area(label, height=150)

if st.button(btn):
    if query and api_key:
        with st.spinner('Iustitia...'):
            try:
                # ВАЖНО: Используем 'gemini-1.5-flash' БЕЗ префикса models/
                # Это должно решить ошибку 404
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt + "\n\nSavol: " + query)
                
                st.markdown("<div class='parchment'>", unsafe_allow_html=True)
                st.write(response.text)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                # Если 1.5-flash не сработал, пробуем базовую версию
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt + "\n\nSavol: " + query)
                    st.markdown("<div class='parchment'>", unsafe_allow_html=True)
                    st.write(response.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                except:
                    st.error(f"Хатолик: {e}")

st.caption("Dura lex, sed lex — Закон суров, но это закон.")
