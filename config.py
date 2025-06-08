"""
Цветовые схемы и CSS-стили для обеих версий сайта.
"""

SITE_NAME = "Furniture Hub"

# ——— Стандартная тема ———
COLOR_SCHEME_CSS = """
<style>
body           { font-family:'Inter',sans-serif; color:#333; background:#F2F5FC; }
h1,h2,h3,h4,h5 { color:#4E7AC7; font-weight:600; }
a              { color:#4E7AC7; text-decoration:none; }
blockquote     { border-left:4px solid #4E7AC7; padding-left:10px; color:#555; }
.banner        { width:100%; border-radius:12px; }
.article-img   { width:100%; border-radius:8px; margin-bottom:1rem; }
.card          { background:#fff; border-radius:12px; padding:1.2rem;
                 box-shadow:0 3px 8px rgba(0,0,0,.05); margin-bottom:1.5rem; }
.msg           { padding:.6rem .8rem; border-radius:8px; background:#fff;
                 box-shadow:0 2px 4px rgba(0,0,0,.06); margin-bottom:.8rem; }
.msg-author    { font-weight:600; color:#4E7AC7; }
.msg-timestamp { font-size:.8rem; color:#777; }
button[kind="primary"]{ border-radius:8px !important; font-weight:600 !important; }
</style>
"""

# config.py

# ——— Контрастная версия (для слабовидящих) ———
ACCESSIBLE_CSS = """
<style>
/* фон делаем чёрным, текст – белым */
body {
    background-color: #000 !important;
    color: #fff !important;
    font-size: 22px !important;
}
/* Заголовки – ярко-жёлтые для контраста */
h1, h2, h3, h4, h5 {
    color: #ff0 !important;
}
/* Ссылки – небесно-голубые */
a {
    color: #0ff !important;
}
/* Карточки и сообщения – очень тёмный фон */
.card, .msg {
    background-color: #111 !important;
    color: #fff !important;
}
/* Кнопки – жёлтые с чёрным текстом */
button[kind="primary"] {
    background-color: #ff0 !important;
    color: #000 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
/* Блок-цитаты – бирюзовая граница */
blockquote {
    border-left: 4px solid #0ff !important;
    padding-left: 10px;
    color: #ddd !important;
}
</style>
"""

