import json
import os
import datetime

MSG_FILE = os.path.join(os.path.dirname(__file__), "messages.json")


def _load():
    if not os.path.exists(MSG_FILE):
        return []
    with open(MSG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(msgs):
    with open(MSG_FILE, "w", encoding="utf-8") as f:
        json.dump(msgs, f, ensure_ascii=False, indent=2)


def post(user: str, text: str):
    msgs = _load()
    msgs.append(
        {
            "user":      user,
            "text":      text,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )
    _save(msgs)


def all():
    """Возвращаем сообщения в обратном порядке (новые сверху)."""
    return _load()[::-1]
