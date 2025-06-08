import streamlit as st
import sidebar
import content  # только чтобы импортить, при необходимости
from pathlib import Path
from typing import Optional
import base64
import mimetypes

# ------------------------------------------------------------------------
#   Сайдбар и роутинг
# ------------------------------------------------------------------------
current_path = "pages/contact.py"
chosen_path = sidebar.render(current_path)
if chosen_path != current_path:
    st.switch_page(chosen_path)

# ------------------------------------------------------------------------
#   Утилиты для работы с изображениями
# ------------------------------------------------------------------------
MEDIA_DIRS = (
    Path("media/product_images"),
    Path("media/blog_images"),
    Path("media"),
)


def _resolve_image(img_name: str) -> Optional[Path]:
    """
    Ищем файл по имени в каталоге media/... и возвращаем Path,
    или None, если не найден.
    """
    # если пользователь передал полный путь
    p = Path(img_name)
    if p.exists():
        return p
    # иначе пробуем каждый подкаталог
    for folder in MEDIA_DIRS:
        cand = folder / img_name
        if cand.exists():
            return cand
    return None


def _make_data_url(img_path: Path) -> str:
    """
    Читаем файл и кодируем в base64 data-url.
    """
    mime, _ = mimetypes.guess_type(str(img_path))
    mime = mime or "image/jpeg"
    data = img_path.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def _embed_image(img_path: Path, max_height: str = "40vh") -> None:
    """
    Вставляем изображение через HTML <img> с object-fit:contain.
    max_height — любая CSS-единица (px, vh и т.д.).
    """
    url = _make_data_url(img_path)
    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:center;
            align-items:center;
            max-height:{max_height};
            overflow:hidden;
            margin-bottom:1rem;
        ">
          <img
            src="{url}"
            style="
              max-width:100%;
              max-height:100%;
              object-fit:contain;
              border-radius:12px;
            "
            alt="showroom"
          />
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------------
#   UI страницы Contact
# ------------------------------------------------------------------------
st.title("Связаться с нами")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Офис шоу-рума")
    st.markdown(
        """
**Адрес:** ул. Мебельная, 15, Москва  
**Телефон:** +7 (495) 123-45-67  
**E-mail:** info@example.com
"""
    )
    # Внедряем showroom.jpg, вписав в блок
    showroom = _resolve_image("showroom.jpg")
    if showroom:
        _embed_image(showroom, max_height="50vh")

with col2:
    with st.form("msg"):
        st.subheader("Напишите нам")
        email = st.text_input("Ваш e-mail")
        message = st.text_area("Сообщение")
        sent = st.form_submit_button("Отправить")
    if sent:
        st.success("Сообщение отправлено! Мы свяжемся с вами.")
