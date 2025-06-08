import streamlit as st
import sidebar
import content
from pathlib import Path
from typing import Optional

current_path = "pages/category_page.py"
chosen_path = sidebar.render(current_path)
if chosen_path != current_path:
    st.switch_page(chosen_path)

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
st.title("Категории статей")
cat_names = {c["key"]: c["name"] for c in content.CATEGORIES}

cat_key = st.selectbox(
    "Выберите раздел",
    list(cat_names.keys()),
    format_func=lambda k: cat_names[k],
)

st.header(cat_names[cat_key])

for art in content.get_articles_by_category(cat_key):
    st.markdown(f"### {art['title']}")
    img = _resolve_image(art["image"])
    if img:
        st.image(img, use_container_width=True)
    st.markdown(art["body"])
    st.markdown("---")
