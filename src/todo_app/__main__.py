from todo_app.cli.app import TodoApp
from todo_app.domain.repository import InMemoryTodoRepository
from todo_app.services.todo_service import TodoService


def main() -> None:
    repository = InMemoryTodoRepository()
    service = TodoService(repository)
    app = TodoApp(service)
    app.run()


if __name__ == "__main__":
    main()
