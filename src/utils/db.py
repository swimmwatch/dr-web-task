import abc
import typing


class BaseDatabase(abc.ABC):
    """Base class for database implementations."""

    @abc.abstractmethod
    def set(self, key: str, value: typing.Any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, key: str) -> typing.Any | None:
        raise NotImplementedError

    @abc.abstractmethod
    def counts(self, value: typing.Any) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def find(self, key: str) -> typing.Sequence[typing.Any]:
        raise NotImplementedError

    @abc.abstractmethod
    def begin(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def unset(self, key: str) -> None:
        raise NotImplementedError


class InMemoryDatabase(BaseDatabase):
    """In-memory database implementation with support for transactions."""

    def __init__(self):
        self.db_stack: typing.List[typing.Dict[str, typing.Any]] = [{}]
        self.value_counts_stack: typing.List[typing.Dict[str, typing.Any]] = [{}]

    def _current_db(self):
        return self.db_stack[-1]

    def _current_counts(self):
        return self.value_counts_stack[-1]

    def _get_from_stack(self, key):
        for db in reversed(self.db_stack):
            if key in db:
                return db[key]
        return None

    def _count_values(self, value: typing.Any) -> int:
        count = 0
        seen_keys = set()
        for db in self.db_stack:
            for k, v in db.items():
                if k not in seen_keys:
                    if v == value:
                        count += 1
                    seen_keys.add(k)
        return count

    def _find_keys(self, value: typing.Any) -> typing.Sequence[typing.Any]:
        found = {}
        for db in self.db_stack:
            for k, v in db.items():
                if k not in found and v == value:
                    found[k] = True

        return list(found.keys())

    def set(self, key, value):
        cur_db = self._current_db()
        cur_db[key] = value

    def get(self, key: str) -> typing.Any | None:
        return self._get_from_stack(key)

    def unset(self, key: str) -> None:
        cur_db = self._current_db()
        cur_db[key] = None

    def counts(self, value: typing.Any) -> int:
        return self._count_values(value)

    def find(self, value: typing.Any) -> typing.Sequence[typing.Any]:
        return self._find_keys(value)

    def begin(self):
        self.db_stack.append(self._current_db().copy())
        self.value_counts_stack.append(self._current_counts().copy())

    def rollback(self):
        if len(self.db_stack) > 1:
            self.db_stack.pop()
            self.value_counts_stack.pop()

    def commit(self):
        if len(self.db_stack) > 1:
            parent = self.db_stack[-2]
            parent.update(self.db_stack.pop())
            self.value_counts_stack.pop()
