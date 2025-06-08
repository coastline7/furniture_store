from content import ARTICLES


def search(query: str):
    """Простой полнотекстовый поиск по названию и телу статьи."""
    q = query.lower()
    return [
        a for a in ARTICLES
        if q in a["title"].lower() or q in a["body"].lower()
    ]
