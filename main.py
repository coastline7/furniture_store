import sys
import base64
import mimetypes
from pathlib import Path
from typing import Optional

from streamlit.web import cli as stcli
from streamlit import runtime
import streamlit as st

import config
import sidebar
import content

# ------------------------------------------------------------------------
#   Настройки страницы (эти команды выполняются один раз при импорте)
# ------------------------------------------------------------------------
st.set_page_config(
    page_title=config.SITE_NAME,
    page_icon="🛋️",
    layout="wide",
)

st.markdown(
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">',
    unsafe_allow_html=True,
)
st.markdown(config.COLOR_SCHEME_CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------------
#   Утилиты
# ------------------------------------------------------------------------
MEDIA_DIRS = (
    Path("media/blog_images"),
    Path("media/product_images"),
    Path("media"),
)


def _find_banner() -> Optional[Path]:
    EXT = (".jpg", ".jpeg", ".png", ".webp")
    for folder in MEDIA_DIRS:
        if folder.exists():
            for img in sorted(folder.iterdir()):
                if img.suffix.lower() in EXT:
                    return img
    return None


def _make_data_url(img_path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(img_path))
    mime = mime or "image/jpeg"
    data = img_path.read_bytes()
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def _resolve_image(name: str) -> Optional[Path]:
    if not name:
        return None
    p = Path(name)
    if p.exists():
        return p
    for folder in MEDIA_DIRS:
        cand = folder / p.name
        if cand.exists():
            return cand
    return None


# ------------------------------------------------------------------------
#   Логика главной страницы
# ------------------------------------------------------------------------
def main():
    # --- Сайдбар и навигация ---
    chosen_path = sidebar.render("main.py")
    if chosen_path != "main.py":
        st.switch_page(chosen_path)
        return                      # не рендерим остальное на редиректе

    # --- Баннер ---
    banner = _find_banner()
    if banner:
        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:center;
                align-items:center;
                max-height:70vh;
                overflow:hidden;
                margin-bottom:1.5rem;
            ">
              <img src="{_make_data_url(banner)}"
                   style="max-width:100%;max-height:100%;
                          object-fit:contain;border-radius:12px;">
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- Последние статьи ---
    st.header("Последние статьи")
    cols = st.columns(3)
    for idx, art in enumerate(content.latest(6)):
        with cols[idx % 3]:
            st.markdown(f"#### {art['title']}")
            img_path = _resolve_image(art.get("image"))
            if img_path:
                st.image(str(img_path), use_container_width=False, width=300)
            st.markdown(art["body"][:180] + " …")
            if st.button("Читать далее", key=art["id"]):
                st.switch_page("pages/news.py")

    # --- О проекте ---
    st.markdown("---")
    st.subheader("О проекте")
    st.markdown(
        """
Furniture Hub — демонстрационный сайт на **Streamlit**, посвящённый современному
мебельному дизайну. Он объединяет статьи, ленту новостей, поиск, систему сообщений
и авторизацию, показывая, как Python-стек способен заменить классический CMS
для небольших контент-проектов.
"""
    )


# ------------------------------------------------------------------------
#   Поддержка запуска «python main.py»
# ------------------------------------------------------------------------
if __name__ == "__main__":
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
