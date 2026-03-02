import streamlit as st
from groq import Groq

# 1. Настройки страницы
st.set_page_config(page_title="Юрист Помощник", layout="centered")

# 2. Красивое оформление
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 22px; }
    .stButton>button { width: 100%; height: 3em; background-color: #28a745; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Работа с ключом (берем из Secrets или вводим вручную)
api_key = st.secrets.get("GROQ_API_KEY") or st.sidebar.text_input("Введите Groq API Key:", type="password")

# 4. Выбор языка
lang = st.sidebar.selectbox("Тилни танланг / Язык", ("Русский", "O'zbekcha"))

# 5. Настройка текстов (исправляем ту самую ошибку с 'title')
if lang == "Русский":
    app_title = "⚖️ Помощник Адвоката"
    input_label = "Опишите ситуацию или номер статьи:"
    button_label = "Найти и объяснить"
    sys_prompt = "Ты профессиональный юрист из Узбекистана. Найди статьи в базе Lex.uz и объясни их просто на русском языке: "
else:
    app_title = "⚖️ Адвокат Ёрдамчиси"
    input_label = "Вазиятни ёзинг ёки модда рақамини:"
    button_label = "Топиш ва тушунтириш"
    sys_prompt = "Сен Ўзбекистонлик профессионал ҳуқуқшуноссан. Lex.uz базасидан моддаларни топ ва ўзбек тилида оддий тушунтириб бер: "

st.title(app_title)

# 6. Поле ввода
user_query = st.text_area(input_label, height=150, placeholder="...")

# 7. Логика работы ИИ
if st.button(button_label):
    if not api_key:
        st.error("Ошибка: Введите API ключ в меню слева! / Хато: Калитни киритинг!")
    elif user_query:
        with st.spinner('🔄 Қидирилмоқда / Поиск...'):
            try:
                client = Groq(api_key=api_key)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": sys_prompt + user_query}]
                )
                st.markdown("### 📄 Натижа / Результат:")
                st.write(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Произошла ошибка / Хатолик юз берди: {e}")
