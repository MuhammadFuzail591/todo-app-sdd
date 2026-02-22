from todo_app.domain.models import Status, Todo
from todo_app.domain.repository import TodoRepository


class TodoService:
    """Business logic for todo operations."""

    def __init__(self, repository: TodoRepository) -> None:
        self._repository = repository

    def _validate_title(self, title: str) -> str:
        stripped = title.strip()
        if not stripped:
            raise ValueError("Title cannot be empty")
        return stripped

    def add_todo(self, title: str) -> Todo:
        """Create a new todo with the given title. Raises ValueError if empty."""
        validated_title = self._validate_title(title)
        return self._repository.add(validated_title)

    def get_all_todos(self) -> list[Todo]:
        """Return all todos ordered by ID."""
        return self._repository.get_all()

    def mark_complete(self, todo_id: int) -> Todo:
        """Mark a todo as completed by ID."""
        todo = self._repository.get(todo_id)
        if todo is None:
            raise KeyError(f"Todo with ID {todo_id} not found")
        if todo.status == Status.COMPLETED:
            raise ValueError("Todo is already completed.")
        updated = self._repository.set_status(todo_id, Status.COMPLETED)
        assert updated is not None  # guaranteed since we just fetched it
        return updated

    def update_todo(self, todo_id: int, title: str) -> Todo:
        """Update a todo's title. Raises KeyError if not found, ValueError if empty."""
        validated_title = self._validate_title(title)
        todo = self._repository.update(todo_id, validated_title)
        if todo is None:
            raise KeyError(f"Todo with ID {todo_id} not found")
        return todo

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo by ID. Raises KeyError if not found."""
        result = self._repository.delete(todo_id)
        if not result:
            raise KeyError(f"Todo with ID {todo_id} not found")
        return result
