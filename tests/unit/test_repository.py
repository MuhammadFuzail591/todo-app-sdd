import pytest

from todo_app.domain.models import Status, Todo
from todo_app.domain.repository import InMemoryTodoRepository


@pytest.fixture
def repo() -> InMemoryTodoRepository:
    return InMemoryTodoRepository()


class TestAdd:
    def test_add_returns_todo(self, repo: InMemoryTodoRepository) -> None:
        todo = repo.add("Buy groceries")
        assert isinstance(todo, Todo)
        assert todo.title == "Buy groceries"
        assert todo.status == Status.PENDING

    def test_add_assigns_id_starting_from_1(self, repo: InMemoryTodoRepository) -> None:
        todo = repo.add("First")
        assert todo.id == 1

    def test_add_auto_increments_id(self, repo: InMemoryTodoRepository) -> None:
        todo1 = repo.add("First")
        todo2 = repo.add("Second")
        assert todo1.id == 1
        assert todo2.id == 2


class TestGet:
    def test_get_existing(self, repo: InMemoryTodoRepository) -> None:
        added = repo.add("Test")
        found = repo.get(added.id)
        assert found is not None
        assert found.id == added.id
        assert found.title == "Test"

    def test_get_missing_returns_none(self, repo: InMemoryTodoRepository) -> None:
        assert repo.get(999) is None


class TestGetAll:
    def test_empty_repo(self, repo: InMemoryTodoRepository) -> None:
        assert repo.get_all() == []

    def test_returns_all_ordered_by_id(self, repo: InMemoryTodoRepository) -> None:
        repo.add("Second")
        repo.add("Third")
        todos = repo.get_all()
        assert len(todos) == 2
        assert todos[0].id < todos[1].id


class TestUpdate:
    def test_update_existing(self, repo: InMemoryTodoRepository) -> None:
        todo = repo.add("Old title")
        updated = repo.update(todo.id, "New title")
        assert updated is not None
        assert updated.title == "New title"

    def test_update_missing_returns_none(self, repo: InMemoryTodoRepository) -> None:
        assert repo.update(999, "Nothing") is None


class TestDelete:
    def test_delete_existing(self, repo: InMemoryTodoRepository) -> None:
        todo = repo.add("To delete")
        assert repo.delete(todo.id) is True
        assert repo.get(todo.id) is None

    def test_delete_missing_returns_false(self, repo: InMemoryTodoRepository) -> None:
        assert repo.delete(999) is False

    def test_deleted_id_not_reused(self, repo: InMemoryTodoRepository) -> None:
        todo1 = repo.add("First")
        repo.delete(todo1.id)
        todo2 = repo.add("Second")
        assert todo2.id == 2
        assert todo2.id != todo1.id
