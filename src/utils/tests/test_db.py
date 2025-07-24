from utils.db import InMemoryDatabase


def test_set_and_get():
    db = InMemoryDatabase()
    db.set("a", 1)
    assert db.get("a") == 1


def test_unset():
    db = InMemoryDatabase()
    db.set("a", 1)
    db.unset("a")
    assert db.get("a") is None


def test_counts():
    db = InMemoryDatabase()
    db.set("a", 1)
    db.set("b", 1)
    db.set("c", 2)
    assert db.counts(1) == 2
    assert db.counts(2) == 1


def test_find():
    db = InMemoryDatabase()
    db.set("a", 1)
    db.set("b", 1)
    db.set("c", 2)
    keys = db.find(1)
    assert set(keys) == {"a", "b"}


def test_transactions_begin_rollback():
    db = InMemoryDatabase()
    db.set("a", 1)
    db.begin()
    db.set("a", 2)
    assert db.get("a") == 2
    db.rollback()
    assert db.get("a") == 1


def test_transactions_begin_commit():
    db = InMemoryDatabase()
    db.set("a", 1)
    db.begin()
    db.set("a", 2)
    db.commit()
    assert db.get("a") == 2


def test_multiple_transactions():
    db = InMemoryDatabase()
    db.set("a", 1)
    db.begin()
    db.set("b", 2)
    db.begin()
    db.set("c", 3)

    assert db.get("c") == 3

    db.rollback()

    assert db.get("c") is None
    assert db.get("b") == 2

    db.commit()

    assert db.get("b") == 2
