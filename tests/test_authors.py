import pytest


def test_create_author(client, db_session):
    payload = {
        "first_name": "Mark",
        "last_name": "Twain",
        "birth_year": 1835,
    }
    resp = client.post("/authors/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] > 0
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["birth_year"] == payload["birth_year"]


def test_get_all_authors(client, author_factory):
    # пусто
    resp = client.get("/authors/")
    assert resp.status_code == 200
    assert resp.json() == []

    # создаем стартовые данные через фикстуру
    author_factory(first_name="Leo", last_name="Tolstoy", birth_year=1828)
    author_factory(first_name="Fyodor", last_name="Dostoevsky", birth_year=1821)

    resp = client.get("/authors/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert {author["last_name"] for author in data} == {"Tolstoy", "Dostoevsky"}


def test_get_author_by_id_and_404(client, author_factory):
    # 404 при отсутствии
    resp = client.get("/authors/999")
    assert resp.status_code == 404

    # создаем стартовые данные через фикстуру
    created = author_factory(first_name="Anton", last_name="Chekhov", birth_year=1860)

    resp = client.get(f"/authors/{created.id}")
    assert resp.status_code == 200
    assert resp.json()["last_name"] == "Chekhov"


def test_update_author(client, author_factory):
    created = author_factory(first_name="George", last_name="Orwell", birth_year=1903)

    update_payload = {"first_name": "Eric", "last_name": "Blair", "birth_year": 1903}
    resp = client.put(f"/authors/{created.id}", json=update_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["first_name"] == "Eric"
    assert data["last_name"] == "Blair"


# @pytest.mark.skip(reason="Не реализован")
def test_delete_author_and_404(client, author_factory):
    # Создаем автора
    author = author_factory(first_name="John", last_name="Smith", birth_year=2000)
    resp = client.delete(f"/authors/{author.id}")
    # Удаление должно вернуть -> code: 204
    assert resp.status_code == 204
    # повторное удаление -> code: 404
    resp = client.delete(f"/authors/{author.id}")
    assert resp.status_code == 404


def test_delete_author_cascades_quotes(client, author_factory, quote_factory):
    author = author_factory(first_name="Test", last_name="Author", birth_year=2000)
    q1 = quote_factory(text="Q1", author_id=author.id)
    q2 = quote_factory(text="Q2", author_id=author.id)

    # убедимся, что цитаты доступны
    resp = client.get("/quotes/")
    assert resp.status_code == 200
    texts = {q["text"] for q in resp.json()}
    assert {"Q1", "Q2"}.issubset(texts)

    # удаляем автора
    resp = client.delete(f"/authors/{author.id}")
    assert resp.status_code == 204

    # цитаты должны исчезнуть
    resp = client.get("/quotes/")
    assert resp.status_code == 200
    texts = {q["text"] for q in resp.json()}
    assert "Q1" not in texts and "Q2" not in texts


def test_get_author_quotes(client, author_factory, quote_factory):
    author1 = author_factory(first_name="A1", last_name="L1", birth_year=1901)
    author2 = author_factory(first_name="A2", last_name="L2", birth_year=1902)

    quote_factory(text="A1-Q1", author_id=author1.id)
    quote_factory(text="A1-Q2", author_id=author1.id)
    quote_factory(text="A2-Q1", author_id=author2.id)

    resp = client.get(f"/authors/{author1.id}/quotes")
    assert resp.status_code == 200
    texts = {q["text"] for q in resp.json()}
    assert texts == {"A1-Q1", "A1-Q2"}

    resp = client.get(f"/authors/{author2.id}/quotes")
    assert resp.status_code == 200
    texts = {q["text"] for q in resp.json()}
    assert texts == {"A2-Q1"}

    # 404 для несуществующего автора
    resp = client.get("/authors/999/quotes")
    assert resp.status_code == 404