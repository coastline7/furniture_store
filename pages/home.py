"""
Прокси-страница, чтобы адрес /home работал так же,
как корневой / (логика содержится в main.main()).
"""

import streamlit as st
import sidebar
import main as main_app            # импорт основного модуля

current_path = "pages/home.py"

# Отрисовываем сайдбар. Если пользователь выбрал другую страницу — переходим.
chosen = sidebar.render(current_path)
if chosen != current_path:
    st.switch_page(chosen)
else:
    # Показываем главную через функцию из main.py
    main_app.main()
