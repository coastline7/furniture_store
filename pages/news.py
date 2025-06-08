import streamlit as st
import sidebar
import content
from pathlib import Path
from typing import Optional

current_path = "pages/news.py"
chosen_path = sidebar.render(current_path)
if chosen_path != current_path:
    st.switch_page(chosen_path)

# ---------- utils ----------
MEDIA_DIRS = (
    Path("media/blog_images"),
    Path("media/product_images"),
    Path("media"),
)


def _resolve_image(img_path: Optional[str]) -> Optional[str]:
    if not img_path:
        return None
    p = Path(img_path)
    if p.exists():
        return str(p)
    for folder in MEDIA_DIRS:
        cand = folder / p.name
        if cand.exists():
            return str(cand)
    return None


# ---------- UI ----------
st.title("Лента новостей")

for art in sorted(content.ARTICLES, key=lambda a: a["date"], reverse=True):
    st.markdown(f"## {art['title']}  —  {art['date']}")
    img = _resolve_image(art["image"])
    if img:
        st.image(img, use_container_width=True)
    st.markdown(art["body"])
    st.markdown("---")
