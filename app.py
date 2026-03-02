import streamlit as st
from groq import Groq

# 1. Настройки страницы (делаем удобно для смартфона)
st.set_page_config(page_title="Юрист Помощник UZ", layout="centered")

# 2. Оформление (крупные кнопки и шрифт)
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 22px; }
    .stButton>button { width: 100%; height: 3.5em; background-color: #28a745; color: white; font-weight: bold; border-radius: 12px; }
    .stTextArea>div>div>textarea { font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 3. ПОЛУЧЕНИЕ КЛЮЧА (программа сама возьмет его из Secrets)
api_key = st.secrets.get("GROQ_API_KEY")

# 4. Выбор языка
lang = st.sidebar.selectbox("Тилни танланг / Выберите язык", ("Русский", "O'zbekcha"))

if lang == "Русский":
    app_title = "⚖️ Помощник Адвоката"
    input_label = "Опишите ситуацию или номер статьи:"
    placeholder = "Например: Статья 100 Семейного кодекса"
    button_label = "Найти и объяснить"
    sys_prompt = "Ты профессиональный юрист из Узбекистана. Найди статьи в базе Lex.uz и объясни их смысл максимально просто и понятно на русском языке: "
else:
    app_title = "⚖️ Адвокат Ёрдамчиси"
    input_label = "Вазиятни ёзинг ёки модда рақамини:"
    placeholder = "Масалан: Оила кодекси 100-модда"
    button_label = "Топиш ва тушунтириш"
    sys_prompt = "Сен Ўзбекистонлик профессионал ҳуқуқшуноссан. Lex.uz базасидан моддаларни топ ва уларнинг мазмунини ўзбек тилида жуда оддий ва тушунарли қилиб тушунтириб бер: "

st.title(app_title)

# 5. Интерфейс
user_query = st.text_area(input_label, height=150, placeholder=placeholder)

if st.button(button_label):
    if not api_key:
        st.error("Ошибка: Ключ ИИ не настроен в Secrets! / Хато: ИИ калити созланмаган!")
    elif user_query:
        with st.spinner('🔄 Қидирилмоқда / Поиск...'):
            try:
                client = Groq(api_key=api_key)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": sys_prompt + user_query}]
                )
                st.markdown("---")
                st.markdown("### 📄 Натижа / Результат:")
                st.write(completion.choices[0].message.content)
                st.caption("Манба: Lex.uz асосида ИИ томонидан тайёрланди")
            except Exception as e:
                st.error(f"Хатолик / Ошибка: {e}")
