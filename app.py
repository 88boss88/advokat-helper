import streamlit as st
from groq import Groq

# 1. Настройки страницы
st.set_page_config(page_title="LEX ROMANA: Codex Magnus", page_icon="🏛️", layout="centered")

# 2. Элитный Римский дизайн
st.markdown("""
    <style>
    .main { background-color: #f4f1ea; }
    .roman-header { 
        color: #66023C; 
        font-family: 'Times New Roman', serif; 
        text-align: center; 
        font-weight: bold;
        text-transform: uppercase;
        border-bottom: 3px double #d4af37;
        padding-bottom: 15px;
        margin-bottom: 35px;
    }
    .parchment {
        background-color: #fcf5e5;
        border: 2px solid #d4af37;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 8px 8px 20px rgba(0,0,0,0.15);
        color: #1a1a1a;
        font-family: 'Georgia', serif;
        font-size: 19px;
    }
    .stButton>button {
        width: 100%;
        height: 4em;
        background: linear-gradient(135deg, #66023C 0%, #800020 100%);
        color: #d4af37;
        font-weight: bold;
        border: 1px solid #d4af37;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background: #d4af37;
        color: #66023C;
        border: 1px solid #66023C;
    }
    [data-testid="stSidebar"] { background-color: #1a1a1a; color: #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# 3. API Ключ (из Secrets)
api_key = st.secrets.get("GROQ_API_KEY")

# 4. Выбор языка (Три варианта)
lang = st.sidebar.selectbox(
    "Linguam elige / Выберите язык", 
    ("O'zbekcha (Lotin)", "Ўзбекча (Кирилл)", "Русский")
)

# Настройка логики под каждый язык
if lang == "O'zbekcha (Lotin)":
    app_title = "LEX ROMANA: ADVOKAT YORDAMCHISI"
    input_label = "Vaziyatni bayon qiling yoki modda raqamini yozing:"
    btn_label = "VERDIKTNI OLISH"
    sys_prompt = "Sen dunyodagi eng kuchli advokatsan. O'zbekiston qonunchiligini (Lex.uz) mukammal bilasan. 'Murojaat qiling' degan gapni unut! Aniq modda raqamini ayt, mazmunini tushuntir va yechim ber. Til: O'zbek tili (Lotin alifbosi)."
elif lang == "Ўзбекча (Кирилл)":
    app_title = "LEX ROMANA: АДВОКАТ ЁРДАМЧИСИ"
    input_label = "Вазиятни баён қилинг ёки модда рақамини ёзинг:"
    btn_label = "ҲУКМНИ ОЛИШ"
    sys_prompt = "Сен дунёдаги энг кучли адвокатсан. Ўзбекистон қонунчилигини (Lex.uz) мукаммал биласан. 'Мурожаат қилинг' деган гапни унут! Аниқ модда рақамини айт, мазмунини тушунтир ва ечим бер. Тил: Ўзбек тили (Кирилл алифбоси)."
else:
    app_title = "LEX ROMANA: ВЕРХОВНЫЙ АДВОКАТ"
    input_label = "Опишите дело или укажите номер статьи:"
    btn_label = "ПОЛУЧИТЬ ВЕРДИКТ"
    sys_prompt = "Ты — лучший адвокат в мире. Ты обладаешь абсолютным знанием законов Узбекистана. Запрещено отвечать 'обратитесь к источникам'. Ты обязан сам процитировать статью из Lex.uz и дать четкое юридическое решение. Язык: русский."

st.markdown(f"<h1 class='roman-header'>{app_title}</h1>", unsafe_allow_html=True)

# 5. Интерфейс
user_query = st.text_area(input_label, height=150, placeholder="...")

if st.button(btn_label):
    if not api_key:
        st.error("API калити топилмади!")
    elif user_query:
        with st.spinner('Iustitia est constans et perpetua voluntas...'):
            try:
                client = Groq(api_key=api_key)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": sys_prompt + user_query}],
                    temperature=0.2 # Делаем ответы более точными и серьезными
                )
                
                st.markdown("<div class='parchment'>", unsafe_allow_html=True)
                st.markdown("### 📜 RESPONSUM:")
                st.write(completion.choices[0].message.content)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.caption("Dura lex, sed lex — Закон суров, но это закон.")
            except Exception as e:
                st.error(f"Хатолик: {e}")
