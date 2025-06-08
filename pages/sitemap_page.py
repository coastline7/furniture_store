import streamlit as st
import sidebar
import content

current_path = "pages/sitemap_page.py"
chosen_path = sidebar.render(current_path)
if chosen_path != current_path:
    st.switch_page(chosen_path)

# ---------- UI ----------
st.title("Карта сайта")

st.markdown("* [Главная](/)")
st.markdown("* [Лента новостей](/#/📰%20Лента%20новостей)")
st.markdown("* [Категории](/#/📚%20Категории)")
for cat in content.CATEGORIES:
    st.markdown(f"  * {cat['name']}")
    for art in content.get_articles_by_category(cat["key"]):
        st.markdown(f"    * {art['title']}")
st.markdown("* [Сообщения](/#/💬%20Сообщения)")
st.markdown("* [Контакты](/#/📞%20Контакты)")
