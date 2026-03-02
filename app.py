import streamlit as st
import google.generativeai as genai

# --- НАСТРОЙКИ ---
st.set_page_config(page_title="Юрист Помощник UZ", layout="centered")

# Крупный шрифт для папы
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 20px; }
    .stButton>button { width: 100%; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Ввод ключа (папа введет его один раз или ты сам вставишь в настройки Streamlit)
api_key = st.sidebar.text_input("Введите API Key (Google Gemini):", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

# Выбор языка
lang = st.sidebar.selectbox("Тилни танланг / Выберите язык", ("Русский", "O'zbekcha"))

if lang == "Русский":
    title = "⚖️ Помощник Адвоката (Узбекистан)"
    label = "Опишите ситуацию или введите номер статьи:"
    placeholder = "Например: Какое наказание за мошенничество по УК РУз?"
    btn_text = "Найти и объяснить"
    prompt_prefix = "Ты профессиональный юрист из Узбекистана. Используй базу Lex.uz. Ответь на русском языке. Найди нужные статьи и объясни их просто: "
else:
    title = "⚖️ Адвокат Ёрдамчиси (Ўзбекистон)"
    label = "Вазиятни ёзинг ёки модда рақамини киритинг:"
    placeholder = "Масалан: Фирибгарлик учун қандай жазо бор?"
    btn_text = "Топиш ва тушунтириш"
    prompt_prefix = "Сен Ўзбекистонлик профессионал ҳуқуқшуноссан. Lex.uz базасидан фойдалан. Ўзбек тилида жавоб бер. Керакли моддаларни топ ва уларни оддий тилда тушунтириб бер: "

st.title(title)

query = st.text_area(label, placeholder=placeholder, height=150)

if st.button(btn_text):
    if not api_key:
        st.error("Пожалуйста, введите API Key в боковом меню! / Илтимос, боковой менюга API Key киритинг!")
    elif query:
        with st.spinner('🔄 Ищу в базе законодательства РУз...'):
            try:
                full_prompt = f"{prompt_prefix} {query}"
                response = model.generate_content(full_prompt)
                
                st.markdown("### 📄 Результат / Натижа:")
                st.write(response.text)
                st.info("ℹ️ Информация подготовлена ИИ на основе данных законодательства РУз.")
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
