from todo_app.domain.models import Status, Todo


class TestStatus:
    def test_pending_value(self) -> None:
        assert Status.PENDING.value == "pending"

    def test_completed_value(self) -> None:
        assert Status.COMPLETED.value == "completed"

    def test_enum_members(self) -> None:
        assert set(Status) == {Status.PENDING, Status.COMPLETED}


class TestTodo:
    def test_create_with_defaults(self) -> None:
        todo = Todo(id=1, title="Buy groceries")
        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.status == Status.PENDING

    def test_create_with_explicit_status(self) -> None:
        todo = Todo(id=2, title="Read a book", status=Status.COMPLETED)
        assert todo.status == Status.COMPLETED

    def test_title_is_mutable(self) -> None:
        todo = Todo(id=1, title="Old title")
        todo.title = "New title"
        assert todo.title == "New title"

    def test_status_is_mutable(self) -> None:
        todo = Todo(id=1, title="Test")
        todo.status = Status.COMPLETED
        assert todo.status == Status.COMPLETED
