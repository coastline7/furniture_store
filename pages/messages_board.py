import streamlit as st
import sidebar
import messages
from typing import Optional

current_path = "pages/messages_board.py"
chosen_path = sidebar.render(current_path)
if chosen_path != current_path:
    st.switch_page(chosen_path)

# ---------- UI ----------
st.title("Общая лента сообщений")

# Форма отправки
if st.session_state.get("user"):
    txt = st.text_area("Ваше сообщение")
    if st.button("Отправить"):
        if txt.strip():
            messages.post(st.session_state["user"], txt)
            st.success("Сообщение отправлено")
            # Перезагрузить, чтобы отобразить сразу новое
            st.markdown(
                "<script>window.location.reload()</script>",
                unsafe_allow_html=True,
            )
else:
    st.info("Войдите, чтобы оставлять сообщения")

# Отображаем все сообщения
for msg in messages.all():
    st.markdown(
        f"""
<div class="msg">
  <span class="msg-author">{msg['user']}</span>
  <span class="msg-timestamp">— {msg['timestamp']}</span><br/>
  {msg['text']}
</div>
""",
        unsafe_allow_html=True,
    )
