import pytest


def _create_author(author_factory):
    return author_factory(first_name="Alan", last_name="Moore", birth_year=1953)


def test_create_quote(client, author_factory):
    author = _create_author(author_factory)
    payload = {"text": "Knowledge, like air, is vital.", "author_id": author.id}
    resp = client.post("/quotes/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] > 0
    assert data["text"] == payload["text"]
    # при создании возвращаемая модель содержит author_id, author может быть None
    assert data["author_id"] == author.id


def test_get_all_quotes(client, author_factory, quote_factory):
    # пусто
    resp = client.get("/quotes/")
    assert resp.status_code == 200
    assert resp.json() == []

    author = _create_author(author_factory)
    quote_factory(text="Quote A", author_id=author.id)
    quote_factory(text="Quote B", author_id=author.id)

    # без expand — автор не вложен
    resp = client.get("/quotes/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert {q["text"] for q in data} == {"Quote A", "Quote B"}
    assert all(q.get("author") is None for q in data)

    # с expand=author — автор вложен
    resp = client.get("/quotes/?expand=author")
    assert resp.status_code == 200
    data = resp.json()
    assert all(q.get("author") is not None for q in data)
    assert all(q["author"]["id"] == author.id for q in data)


def test_get_quote_by_id_and_404(client, author_factory, quote_factory):
    # 404 при отсутствии
    resp = client.get("/quotes/999")
    assert resp.status_code == 404

    author = _create_author(author_factory)
    created = quote_factory(text="Once", author_id=author.id)

    # без expand
    resp = client.get(f"/quotes/{created.id}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["text"] == "Once"
    assert body.get("author") is None


def test_get_quote_expand_by_id(client, author_factory, quote_factory):
    author = author_factory(first_name="A", last_name="B", birth_year=1990)
    created = quote_factory(text="Expanded", author_id=author.id)

    resp = client.get(f"/quotes/{created.id}?expand=author")
    assert resp.status_code == 200
    body = resp.json()
    assert body["text"] == "Expanded"
    assert body["author"]["id"] == author.id


# @pytest.mark.skip(reason="Не реализован")
def test_update_quote(client, author_factory, quote_factory):
    # Создаем автора и цитату
    author = author_factory(first_name="Ivan", last_name="Ivanov", birth_year= 2000)
    quote = quote_factory(text="Test quote", author_id=author.id)
    # Отправляем PUT запрос, изменив текст цитаты
    payload = {"text": "Update quote",
               "author_id": author.id}
    update = client.put(f"/quotes/{quote.id}", json=payload)
    assert update.status_code == 200
    # Провекряем, что текст в БД изменился
    data = update.json()
    assert data["id"] == quote.id
    assert data["text"] == "Update quote"
    assert data["author"]["id"] == author.id
    ...


# @pytest.mark.skip(reason="Не реализован")
def test_delete_quote_and_404(client, author_factory, quote_factory):
    author = author_factory(first_name="Anna", last_name="Petrova", birth_year=2000)
    quote = quote_factory(text="This will be deleted", author_id=author.id)

    resp = client.delete(f"/quotes/{quote.id}")
    assert resp.status_code == 204

    resp = client.delete(f"/quotes/{quote.id}")
    assert resp.status_code == 404