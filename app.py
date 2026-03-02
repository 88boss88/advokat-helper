import streamlit as st

# Настройки страницы для удобства папы
st.set_page_config(page_title="Юрист Помощник UZ", layout="centered")

# Стилизация (крупный текст)
st.markdown("""<style> .stButton>button { width: 100%; height: 3em; font-size: 20px; } </style>""", unsafe_allow_html=True)

# Выбор языка
lang = st.sidebar.selectbox("Тилни танланг / Выберите язык", ("Русский", "O'zbekcha"))

if lang == "Русский":
    st.title("⚖️ Помощник Адвоката")
    query_label = "Введите ваш вопрос или номер статьи:"
    btn_text = "Найти и объяснить"
else:
    st.title("⚖️ Адвокат Ёрдамчиси")
    query_label = "Саволингизни ёки модда рақамини киритинг:"
    btn_text = "Топиш ва тушунтириш"

query = st.text_input(query_label, placeholder="Например: ст 159 УК РУз")

if st.button(btn_text):
    if query:
        st.info("🔄 Ищу информацию...")
        # Скоро здесь появится связь с ИИ
        st.success(f"Результаты по запросу: {query}")
        st.write("Текст статьи из Lex.uz и понятное объяснение появятся здесь после подключения 'мозга' приложения.")
