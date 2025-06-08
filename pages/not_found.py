import streamlit as st
import sidebar

# Для 404 мы не хотим редиректить обратно: просто показываем меню.
chosen_path = sidebar.render(None)
# Если пользователь кликнул другой пункт меню — переходим:
if chosen_path and chosen_path != "pages/not_found.py":
    st.switch_page(chosen_path)

st.title("404 — страница не найдена")
st.markdown(
    "К сожалению, запрошенная страница отсутствует. "
    "Используйте меню слева, чтобы вернуться к доступным разделам."
)
