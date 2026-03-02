import streamlit as st
from groq import Groq

# 1. Настройки страницы с римской иконкой
st.set_page_config(page_title="Lex Romana UZ", page_icon="🏛️", layout="centered")

# 2. "Римский" дизайн (CSS)
st.markdown("""
    <style>
    /* Фон под мрамор и основные цвета */
    .main { background-color: #f4f1ea; }
    
    /* Стиль заголовка - Имперский Пурпур */
    .roman-title { 
        color: #66023C; 
        font-family: 'Times New Roman', serif; 
        text-align: center; 
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 2px solid #d4af37;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }

    /* Свиток для вывода результата */
    .parchment {
        background-color: #fcf5e5;
        border: 1px solid #d4af37;
        padding: 30px;
        border-radius: 5px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        position: relative;
        color: #2c1e1e;
        line-height: 1.6;
        font-family: 'Georgia', serif;
    }

    /* Золотая кнопка */
    .stButton>button {
        width: 100%;
        height: 3.5em;
        background: linear-gradient(135deg, #d4af37 0%, #aa8a2e 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 0px; /* Квадратные классические формы */
        letter-spacing: 1px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        background: #66023C;
        color: #d4af37;
    }

    /* Сайдбар */
    [data-testid="stSidebar"] {
        background-color: #2c1e1e;
        color: #d4af37;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Ключ API (автоматически берется из Secrets)
api_key = st.secrets.get("GROQ_API_KEY")

# 4. Выбор языка
lang = st.sidebar.selectbox("Linguam elige / Выберите язык", ("O'zbekcha", "Русский"))

if lang == "Русский":
    app_title = "LEX ROMANA: ПОМОЩНИК ЮРИСТА"
    input_label = "Изложите дело или укажите номер статьи:"
    placeholder = "Например: Статья о наследовании..."
    button_label = "ПОЛУЧИТЬ ВЕРДИКТ"
    # Инструкция для ИИ быть как римский юрист
    sys_prompt = "Ты — мудрый римский юрист (претор), консультирующий по современным законам Узбекистана. Пиши официально, уверенно, используй юридические термины. Ссылайся на статьи Lex.uz. Язык: русский. Текст: "
else:
    app_title = "LEX ROMANA: ҲУҚУҚИЙ ЁРДАМЧИ"
    input_label = "Вазиятни баён қилинг ёки модда рақамини ёзинг:"
    placeholder = "Масалан: Мерос ҳақидаги моддалар..."
    button_label = "ҲУКМНИ ОЛИШ"
    sys_prompt = "Сен Ўзбекистон қонунчилиги бўйича донишманд ҳуқуқшуноссан (претор). Lex.uz базасига асосланиб, расмий ва аниқ жавоб бер. Тил: ўзбекча. Матн: "

# Вывод римского заголовка
st.markdown(f"<h1 class='roman-title'>{app_title}</h1>", unsafe_allow_html=True)

# 5. Поле ввода
user_query = st.text_area(input_label, height=150, placeholder=placeholder)

if st.button(button_label):
    if not api_key:
        st.error("Ашибка: Калит топилмади! (API Key missing)")
    elif user_query:
        with st.spinner('Справедливость требует времени...'):
            try:
                client = Groq(api_key=api_key)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": sys_prompt + user_query}]
                )
                
                # Результат в стиле свитка
                st.markdown("<div class='parchment'>", unsafe_allow_html=True)
                st.markdown("### 📜 RESPONSUM (ОТВЕТ):")
                st.write(completion.choices[0].message.content)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.caption("Dura lex, sed lex — Закон суров, но это закон.")
            except Exception as e:
                st.error(f"Ошибка в претории: {e}")
