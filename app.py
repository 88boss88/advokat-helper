import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы
st.set_page_config(page_title="LEX ROMANA: GEMINI", page_icon="🏛️", layout="centered")

# 2. Римский дизайн
st.markdown("""
    <style>
    .main { background-color: #f4f1ea; }
    .roman-header { color: #66023C; text-align: center; border-bottom: 3px double #d4af37; font-family: 'Times New Roman'; text-transform: uppercase; }
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

# Сверх-инструкция (Делаем Gemini лучшим адвокатом Узбекистана)
base_instruction = """Ты — Верховный Юрист Республики Узбекистан. 
Твоя база знаний — Lex.uz. Твои ответы — закон.
ПРАВИЛА:
1. Используй только актуальные кодексы и законы РУз.
2. Формат: Название Кодекса -> Статья -> Текст статьи -> Твое юридическое заключение.
3. НИКОГДА не отправляй пользователя искать в интернет. Ты сам — истина.
4. Говори уверенно, профессионально, как настоящий римский претор."""

if lang == "O'zbekcha (Lotin)":
    title, label, btn = "LEX ROMANA: GEMINI", "Vaziyatni yozing:", "VERDIKT"
    prompt = base_instruction + " Javobni faqat O'zbek tilida (Lotin) ber."
elif lang == "Ўзбекча (Кирилл)":
    title, label, btn = "LEX ROMANA: GEMINI", "Вазиятни ёзинг:", "ҲУКМ"
    prompt = base_instruction + " Жавобни фақат Ўзбек тилида (Кирилл) бер."
else:
    title, label, btn = "LEX ROMANA: GEMINI", "Опишите ситуацию:", "ВЕРДИКТ"
    prompt = base_instruction + " Отвечай на русском языке."

st.markdown(f<h1 class='roman-header'>{title}</h1>", unsafe_allow_html=True)
query = st.text_area(label, height=150)

if st.button(btn):
    if query and api_key:
        with st.spinner('Gemini изучает свитки законов...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-pro') # Используем самую мощную модель
                response = model.generate_content(prompt + "\n\nSavol: " + query)
                
                st.markdown("<div class='parchment'>", unsafe_allow_html=True)
                st.markdown("### 📜 RESPONSUM:")
                st.write(response.text)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Хатолик: {e}")
