import streamlit as st
from groq import Groq

# 1. Настройка страницы в имперском стиле
st.set_page_config(page_title="LEX ROMANA: ADVOCATUS", page_icon="🏛️", layout="centered")

# 2. Дизайн "Римский Мрамор и Золото"
st.markdown("""
    <style>
    .main { background-color: #f4f1ea; }
    .stTextArea>div>div>textarea { background-color: #ffffff; border: 2px solid #d4af37; font-size: 18px; }
    .roman-header { 
        color: #66023C; 
        font-family: 'Times New Roman', serif; 
        text-align: center; 
        text-transform: uppercase;
        border-bottom: 3px double #d4af37;
        padding-bottom: 10px;
    }
    .parchment {
        background-color: #fcf5e5;
        border-left: 10px solid #66023C;
        padding: 25px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        font-family: 'Georgia', serif;
        font-size: 19px;
        color: #1a1a1a;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #66023C 0%, #d4af37 100%);
        color: white;
        font-weight: bold;
        height: 3.5em;
        border-radius: 0;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Подключение ключа (из Secrets)
api_key = st.secrets.get("GROQ_API_KEY")

# 4. Выбор языка (Три варианта по твоему запросу)
lang = st.sidebar.selectbox(
    "Lingua / Тил", 
    ("O'zbekcha (Lotin)", "Ўзбекча (Кирилл)", "Русский")
)

# Формируем сверх-строгую инструкцию для "Умного Адвоката"
base_instruction = """Сен Ўзбекистон Республикасининг энг билимдон бош адвокатисан. 
Сен фақат Ўзбекистон қонунлари (Lex.uz) асосида жавоб берасан. 
Сенга 'билмайман' ёки 'манбага мурожаат қилинг' дейиш ТАҚИҚЛАНАДИ.
Жавоб стандарти:
1. Қонун ҳужжати номи (масалан: Жиноят Кодекси).
2. Модда рақами ва унинг аниқ мазмуни.
3. Ушбу вазият учун ҳуқуқий ечим.
Агар модда рақамини аниқ эслай олмасанг, 'Тахминимча' дема, балки қонун мазмунини тушунтир.
ФАҚАТ Ўзбекистон қонунчилигини ишлат!"""

if lang == "O'zbekcha (Lotin)":
    app_title = "LEX ROMANA: ADVOKAT"
    label = "Vaziyatni yozing:"
    btn = "VERDIKT"
    prompt = base_instruction + " Javobni Lotin alifbosida yoz."
elif lang == "Ўзбекча (Кирилл)":
    app_title = "LEX ROMANA: АДВОКАТ"
    label = "Вазиятни ёзинг:"
    btn = "ҲУКМ"
    prompt = base_instruction + " Жавобни Кирилл алифбосида ёз."
else:
    app_title = "LEX ROMANA: АДВОКАТ"
    label = "Опишите ситуацию:"
    btn = "ВЕРДИКТ"
    prompt = "Ты Верховный Адвокат Узбекистана. Отвечай строго по законам РУз (Lex.uz). НИКОГДА не отправляй пользователя искать в гугле. Дай конкретную статью и решение на русском языке."

st.markdown(f"<h1 class='roman-header'>{app_title}</h1>", unsafe_allow_html=True)

# 5. Ввод данных
query = st.text_area(label, height=150, placeholder="Масалан: Меросхўрлик тартиби қандай?")

if st.button(btn):
    if not api_key:
        st.error("API Key missing in Secrets!")
    elif query:
        with st.spinner('Iustitia...'):
            try:
                client = Groq(api_key=api_key)
                # УСТАНОВКА TEMPERATURE 0.0 ДЛЯ МАКСИМАЛЬНОЙ ТОЧНОСТИ
                chat = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt + "\nSavol: " + query}],
                    temperature=0.0 
                )
                
                st.markdown("<div class='parchment'>", unsafe_allow_html=True)
                st.markdown("### 📜 RESPONSUM:")
                st.write(chat.choices[0].message.content)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

st.caption("Dura lex, sed lex.")
