"""
Импортируем модули страниц «лениво» и кладём их в namespace,
чтобы main.py мог вызывать page.run() без прямого импорта в каждом месте.
"""
from importlib import import_module, reload


def _load(name: str):
    module = import_module(f"pages.{name}")
    # При hot-reload в Streamlit удобно принудительно перечитывать файл
    # (работает только в режиме dev, но не мешает на проде).
    reload(module)
    return module


home            = _load("home")
news            = _load("news")
category_page   = _load("category_page")
messages_board  = _load("messages_board")
contact         = _load("contact")
sitemap_page    = _load("sitemap_page")
not_found       = _load("not_found")
