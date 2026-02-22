from todo_app.services.todo_service import TodoService

MENU = """
=== Todo App ===
1. Add Todo
2. View Todos
3. Mark Complete
4. Update Todo
5. Delete Todo
6. Exit
"""


class TodoApp:
    """Interactive CLI for the todo application."""

    def __init__(self, service: TodoService) -> None:
        self._service = service

    def run(self) -> None:
        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self._add_todo()
            elif choice == "2":
                self._view_todos()
            elif choice == "3":
                self._mark_complete()
            elif choice == "4":
                self._update_todo()
            elif choice == "5":
                self._delete_todo()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

    def _add_todo(self) -> None:
        title = input("Enter todo title: ")
        try:
            todo = self._service.add_todo(title)
            print(f"Todo added: [{todo.id}] {todo.title} ({todo.status.value})")
        except ValueError as e:
            print(str(e))

    def _view_todos(self) -> None:
        todos = self._service.get_all_todos()
        if not todos:
            print("No todos found.")
            return
        for todo in todos:
            print(f"[{todo.id}] {todo.title} - {todo.status.value}")

    def _mark_complete(self) -> None:
        raw_id = input("Enter todo ID: ")
        try:
            todo_id = int(raw_id)
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return
        try:
            todo = self._service.mark_complete(todo_id)
            print(f"Todo marked as completed: [{todo.id}] {todo.title}")
        except KeyError:
            print("Todo not found.")
        except ValueError as e:
            print(str(e))

    def _update_todo(self) -> None:
        raw_id = input("Enter todo ID: ")
        try:
            todo_id = int(raw_id)
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return
        title = input("Enter new title: ")
        try:
            todo = self._service.update_todo(todo_id, title)
            print(f"Todo updated: [{todo.id}] {todo.title} ({todo.status.value})")
        except KeyError:
            print("Todo not found.")
        except ValueError as e:
            print(str(e))

    def _delete_todo(self) -> None:
        raw_id = input("Enter todo ID: ")
        try:
            todo_id = int(raw_id)
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return
        try:
            self._service.delete_todo(todo_id)
            print("Todo deleted.")
        except KeyError:
            print("Todo not found.")
