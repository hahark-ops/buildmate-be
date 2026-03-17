from models import comment_model


class DummyCursor:
    def __init__(self):
        self.executed = []

    def execute(self, sql, params):
        self.executed.append((sql, params))

    def fetchall(self):
        return []


class DummyContextManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def __enter__(self):
        return None, self.cursor

    def __exit__(self, exc_type, exc, tb):
        return False


def test_fetch_comments_query_is_compatible_with_comments_schema(monkeypatch):
    cursor = DummyCursor()
    monkeypatch.setattr(
        "models.comment_model.get_cursor",
        lambda: DummyContextManager(cursor),
    )

    comment_model.fetch_comments(7)

    assert cursor.executed
    sql, params = cursor.executed[0]
    assert params == (7,)
    assert "c.updatedAt" not in sql
    assert "NULL as updatedAt" in sql
