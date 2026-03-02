import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы
st.set_page_config(page_title="LEX ROMANA: GEMINI", page_icon="🏛️", layout="centered")

# 2. Римский дизайн (Золото и Пурпур)
st.markdown("""
    <style>
    .main { background-color: #f4f1ea; }
    .roman-header { 
        color: #66023C; 
        text-align: center; 
        border-bottom: 3px double #d4af37; 
        font-family: 'Times New Roman', serif; 
        text-transform: uppercase;
        padding-bottom: 10px;
    }
    .parchment { 
        background-color: #fcf5e5; 
        border-left: 10px solid #66023C; 
        padding: 25px; 
        font-size: 20px; 
        color: #1a1a1a; 
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        font-family: 'Georgia', serif;
    }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(135deg, #66023C 0%, #d4af37 100%); 
        color: white; 
        font-weight: bold; 
        height: 4em; 
        border: none; 
        font-size: 18px;
    }
    .stTextArea>div>div>textarea {
        background-color: #ffffff;
        border: 2px solid #d4af37;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Подключение Gemini через Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# 4. Выбор языка (Три варианта: Лотин, Кирилл, Русский)
lang = st.sidebar.selectbox(
    "Linguam elige / Тилни танланг", 
    ("O'zbekcha (Lotin)", "Ўзбекча (Кирилл)", "Русский")
)

# Инструкция для ИИ (Чтобы не "тупил" и знал Lex.uz)
base_instruction = """Сен Ўзбекистон Республикасининг Олий Адвокатисан. 
Сен фақат Ўзбекистон қонунлари (Lex.uz) асосида жавоб берасан. 
Сенга 'билмайман' ёки 'манбага мурожаат қилинг' дейиш ТАҚИҚЛАНАДИ.
Жавоб стандарти:
1. Қонун ҳужжати номи (масалан: Жиноят Кодекси).
2. Модда рақами ва унинг аниқ мазмуни.
3. Ушбу вазият учун ҳуқуқий ечим.
ФАҚАТ Ўзбекистон қонунчилигини ишлат!"""

if lang == "O'zbekcha (Lotin)":
    title, label, btn = "LEX ROMANA: ADVOKAT", "Vaziyatni yozing:", "VERDIKT"
    prompt = base_instruction + " Javobni faqat O'zbek tilida (Lotin alifbosida) ber."
elif lang == "Ўзбекча (Кирилл)":
    title, label, btn = "LEX ROMANA: АДВОКАТ", "Вазиятни ёзинг:", "ҲУКМ"
    prompt = base_instruction + " Жавобни фақат Ўзбек тилида (Кирилл алифбосида) бер."
else:
    title, label, btn = "LEX ROMANA: АДВОКАТ", "Опишите ситуацию:", "ВЕРДИКТ"
    prompt = "Ты Верховный Адвокат Узбекистана. Отвечай строго по законам РУз (Lex.uz). НИКОГДА не отправляй пользователя искать в гугле. Дай конкретную статью и решение на русском языке."

# Исправленный заголовок (Ошибка 11068 исправлена)
st.markdown(f"<h1 class='roman-header'>{title}</h1>", unsafe_allow_html=True)

# 5. Поле ввода
query = st.text_area(label, height=150, placeholder="Масалан: 232-модда ҳақида маълумот беринг")

if st.button(btn):
    if not api_key:
        st.error("API Key (GOOGLE_API_KEY) missing in Secrets!")
    elif query:
        with st.spinner('Iustitia est constans...'):
            try:
                # Исправленное название модели (Ошибка 11069 исправлена)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt + "\n\nSavol: " + query)
                
                st.markdown("<div class='parchment'>", unsafe_allow_html=True)
                st.markdown("### 📜 RESPONSUM:")
                st.write(response.text)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Хатолик юз берди: {e}")

st.caption("Dura lex, sed lex — Закон суров, но это закон.")
 
