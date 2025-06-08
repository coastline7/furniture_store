"""
Единый сайдбар: авторизация, поиск, меню
и переключатель «Версия для слабовидящих».
После успешного входа/выхода автоматически перезагружает страницу через JS.
Работает на Python ≥3.7 и Streamlit без experimental_rerun.
"""

import streamlit as st
import auth
import search
import config
from pathlib import Path
from typing import Optional

# ------- маршруты страниц -------
MENU = {
    "🏠 Главная":       "main.py",
    "📰 Лента новостей": "pages/news.py",
    "📚 Категории":     "pages/category_page.py",
    "💬 Сообщения":     "pages/messages_board.py",
    "📞 Контакты":      "pages/contact.py",
    "🗺️ Карта сайта":   "pages/sitemap_page.py",
}

# ------------------------------------------------------------------ AUTH ---
def _login_block() -> None:
    st.sidebar.subheader("Вход")
    uname = st.sidebar.text_input("Имя пользователя", key="login_user")
    pwd   = st.sidebar.text_input("Пароль", type="password", key="login_pwd")
    if st.sidebar.button("Войти"):
        ok, role = auth.authenticate(uname, pwd)
        if ok:
            st.session_state["user"] = uname
            st.session_state["role"] = role
            st.sidebar.success("Успешный вход!")
            # Перезагрузить страницу
            st.sidebar.markdown(
                "<script>window.location.reload()</script>",
                unsafe_allow_html=True,
            )
        else:
            st.sidebar.error("Неверные учётные данные")

def _signup_block() -> None:
    st.sidebar.subheader("Регистрация")
    uname = st.sidebar.text_input("Новое имя пользователя", key="reg_user")
    pwd1  = st.sidebar.text_input("Пароль", type="password", key="reg_pwd1")
    pwd2  = st.sidebar.text_input("Повторите пароль", type="password", key="reg_pwd2")
    if st.sidebar.button("Создать аккаунт"):
        if pwd1 != pwd2 or not pwd1:
            st.sidebar.error("Пароли не совпадают или пустые")
        else:
            ok, msg = auth.create_user(uname, pwd1)
            if ok:
                st.sidebar.success(msg)
                st.sidebar.markdown(
                    "<script>window.location.reload()</script>",
                    unsafe_allow_html=True,
                )
            else:
                st.sidebar.error(msg)

def _auth_section() -> None:
    if st.session_state.get("user"):
        st.sidebar.success(
            f"Вы вошли как **{st.session_state['user']}** "
            f"({st.session_state['role']})"
        )
        if st.sidebar.button("Выйти"):
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.sidebar.success("Вы вышли")
            st.sidebar.markdown(
                "<script>window.location.reload()</script>",
                unsafe_allow_html=True,
            )
    else:
        tab = st.sidebar.radio("Авторизация", ["Войти", "Регистрация"])
        if tab == "Войти":
            _login_block()
        else:
            _signup_block()

# ------------------------------------------------------------- RENDER ---
def render(active_path: Optional[str]) -> str:
    """
    Рисуем сайдбар и возвращаем путь *.py выбранной страницы.
    active_path — текущий файл (например 'pages/news.py') или None.
    """
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "role" not in st.session_state:
        st.session_state["role"] = None
    if "a11y" not in st.session_state:
        st.session_state["a11y"] = False

    _auth_section()
    st.sidebar.markdown("---")

    # ------- поиск -------
    query = st.sidebar.text_input("🔍 Поиск по статьям")
    if query:
        results = search.search(query)
        st.sidebar.markdown(f"**Найдено: {len(results)}**")
        for art in results[:10]:
            st.sidebar.markdown(f"- {art['title']}")
    st.sidebar.markdown("---")

    # ------- меню -------
    menu_keys = list(MENU.keys())
    default_idx = 0
    if active_path and active_path in MENU.values():
        default_idx = list(MENU.values()).index(active_path)
    selection = st.sidebar.radio("Меню", menu_keys, index=default_idx)
    selected_path = MENU[selection]

    # ------- версия для слабовидящих -------
    st.sidebar.markdown("---")
    st.session_state["a11y"] = st.sidebar.checkbox(
        "Версия для слабовидящих",
        value=st.session_state["a11y"],
    )
    if st.session_state["a11y"]:
        st.markdown(config.ACCESSIBLE_CSS, unsafe_allow_html=True)

    return selected_path
