
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
