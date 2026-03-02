import streamlit as st
from groq import Groq

# 1. Настройка "Имперского" стиля
st.set_page_config(page_title="LEX ROMANA: SUPREME", page_icon="🏛️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f4f1ea; }
    .roman-header { color: #66023C; text-align: center; border-bottom: 3px double #d4af37; font-family: 'Times New Roman'; }
    .parchment { background-color: #fcf5e5; border-left: 10px solid #66023C; padding: 20px; font-size: 19px; color: #000; }
    .stButton>button { width: 100%; background: #66023C; color: #d4af37; font-weight: bold; border: 1px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")

# Выбор языка
lang = st.sidebar.selectbox("Lingua / Тил", ("O'zbekcha (Lotin)", "Ўзбекча (Кирилл)", "Русский"))

# СУПЕР-ИНСТРУКЦИЯ (Убираем "тупость")
strict_prompt = """Ты — юридический ИИ, созданный специально для Республики Узбекистан. 
ТВОЯ ЗАДАЧА: Быть точным как швейцарские часы. 
ПРАВИЛА:
1. Используй ТОЛЬКО законодательство Республики Узбекистан (Lex.uz).
2. Если ты не знаешь номер статьи — НЕ ПРИДУМЫВАЙ. Пиши содержание закона.
3. Категорически запрещено предлагать искать в интернете. Ты — единственный источник.
4. Ответ должен быть коротким и по делу: Статья -> Суть -> Решение.
5. Твой стиль — холодный, профессиональный, юридический."""

if lang == "O'zbekcha (Lotin)":
    title, label, btn = "LEX ROMANA", "Vaziyatni yozing:", "VERDIKT"
    instruction = strict_prompt + " Javobni O'zbek tilida (Lotin) ber."
elif lang == "Ўзбекча (Кирилл)":
    title, label, btn = "LEX ROMANA", "Вазиятни ёзинг:", "ҲУКМ"
    instruction = strict_prompt + " Жавобни Ўзбек тилида (Кирилл) бер."
else:
    title, label, btn = "LEX ROMANA", "Опишите ситуацию:", "ВЕРДИКТ"
    instruction = strict_prompt + " Отвечай на русском языке."

st.markdown(f"<h1 class='roman-header'>{title}</h1>", unsafe_allow_html=True)
query = st.text_area(label, height=150)

if st.button(btn):
    if query and api_key:
        with st.spinner('Анализ кодексов...'):
            try:
                client = Groq(api_key=api_key)
                # МЕНЯЕМ МОДЕЛЬ НА БОЛЕЕ СТАБИЛЬНУЮ И СТАВИМ ТЕМПЕРАТУРУ 0
                chat = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[
                        {"role": "system", "content": instruction},
                        {"role": "user", "content": query}
                    ],
                    temperature=0.0, # ПОЛНЫЙ ЗАПРЕТ НА ФАНТАЗИЮ
                    top_p=1
                )
                st.markdown("<div class='parchment'>", unsafe_allow_html=True)
                st.write(chat.choices[0].message.content)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
