from abc import ABC, abstractmethod

from todo_app.domain.models import Status, Todo


class TodoRepository(ABC):
    """Abstract base class defining the todo storage contract."""

    @abstractmethod
    def add(self, title: str) -> Todo:
        """Create a new todo with the given title."""

    @abstractmethod
    def get(self, todo_id: int) -> Todo | None:
        """Get a todo by ID, or None if not found."""

    @abstractmethod
    def get_all(self) -> list[Todo]:
        """Get all todos ordered by ID."""

    @abstractmethod
    def update(self, todo_id: int, title: str) -> Todo | None:
        """Update a todo's title. Returns None if not found."""

    @abstractmethod
    def delete(self, todo_id: int) -> bool:
        """Delete a todo by ID. Returns True if deleted."""


class InMemoryTodoRepository(TodoRepository):
    """In-memory dictionary-based todo repository."""

    def __init__(self) -> None:
        self._todos: dict[int, Todo] = {}
        self._counter: int = 0

    def add(self, title: str) -> Todo:
        self._counter += 1
        todo = Todo(id=self._counter, title=title, status=Status.PENDING)
        self._todos[self._counter] = todo
        return todo

    def get(self, todo_id: int) -> Todo | None:
        return self._todos.get(todo_id)

    def get_all(self) -> list[Todo]:
        return sorted(self._todos.values(), key=lambda t: t.id)

    def update(self, todo_id: int, title: str) -> Todo | None:
        todo = self._todos.get(todo_id)
        if todo is None:
            return None
        todo.title = title
        return todo

    def delete(self, todo_id: int) -> bool:
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False
