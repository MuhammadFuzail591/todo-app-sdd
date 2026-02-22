import pytest

from todo_app.domain.models import Status
from todo_app.domain.repository import InMemoryTodoRepository
from todo_app.services.todo_service import TodoService


@pytest.fixture
def service() -> TodoService:
    repo = InMemoryTodoRepository()
    return TodoService(repo)


class TestAddTodo:
    def test_add_valid_title(self, service: TodoService) -> None:
        todo = service.add_todo("Buy groceries")
        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.status == Status.PENDING

    def test_add_strips_whitespace(self, service: TodoService) -> None:
        todo = service.add_todo("  Buy groceries  ")
        assert todo.title == "Buy groceries"

    def test_add_empty_title_raises(self, service: TodoService) -> None:
        with pytest.raises(ValueError, match="Title cannot be empty"):
            service.add_todo("")

    def test_add_whitespace_only_raises(self, service: TodoService) -> None:
        with pytest.raises(ValueError, match="Title cannot be empty"):
            service.add_todo("   ")

    def test_add_multiple_increments_id(self, service: TodoService) -> None:
        todo1 = service.add_todo("First")
        todo2 = service.add_todo("Second")
        assert todo1.id == 1
        assert todo2.id == 2


class TestGetAllTodos:
    def test_empty_returns_empty_list(self, service: TodoService) -> None:
        assert service.get_all_todos() == []

    def test_returns_all_ordered_by_id(self, service: TodoService) -> None:
        service.add_todo("First")
        service.add_todo("Second")
        service.add_todo("Third")
        todos = service.get_all_todos()
        assert len(todos) == 3
        assert [t.id for t in todos] == [1, 2, 3]


class TestMarkComplete:
    def test_mark_pending_todo(self, service: TodoService) -> None:
        todo = service.add_todo("Test")
        completed = service.mark_complete(todo.id)
        assert completed.status == Status.COMPLETED

    def test_mark_already_completed_raises(self, service: TodoService) -> None:
        todo = service.add_todo("Test")
        service.mark_complete(todo.id)
        with pytest.raises(ValueError, match="Todo is already completed."):
            service.mark_complete(todo.id)

    def test_mark_missing_id_raises(self, service: TodoService) -> None:
        with pytest.raises(KeyError):
            service.mark_complete(999)


class TestUpdateTodo:
    def test_update_valid(self, service: TodoService) -> None:
        todo = service.add_todo("Old title")
        updated = service.update_todo(todo.id, "New title")
        assert updated.title == "New title"

    def test_update_strips_whitespace(self, service: TodoService) -> None:
        todo = service.add_todo("Old")
        updated = service.update_todo(todo.id, "  New  ")
        assert updated.title == "New"

    def test_update_empty_title_raises(self, service: TodoService) -> None:
        todo = service.add_todo("Test")
        with pytest.raises(ValueError, match="Title cannot be empty"):
            service.update_todo(todo.id, "")

    def test_update_whitespace_title_raises(self, service: TodoService) -> None:
        todo = service.add_todo("Test")
        with pytest.raises(ValueError, match="Title cannot be empty"):
            service.update_todo(todo.id, "   ")

    def test_update_missing_id_raises(self, service: TodoService) -> None:
        with pytest.raises(KeyError):
            service.update_todo(999, "New")


class TestDeleteTodo:
    def test_delete_existing(self, service: TodoService) -> None:
        todo = service.add_todo("To delete")
        result = service.delete_todo(todo.id)
        assert result is True
        assert service.get_all_todos() == []

    def test_delete_missing_id_raises(self, service: TodoService) -> None:
        with pytest.raises(KeyError):
            service.delete_todo(999)
