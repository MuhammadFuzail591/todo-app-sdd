# Service Contract: TodoService

**Branch**: `001-todo-console-app` | **Date**: 2026-02-19

Phase I does not expose a REST API. The service layer is the internal
contract between the CLI layer and the repository. This contract
defines the public interface of TodoService.

## TodoService Interface

### add_todo(title: str) → Todo

Creates a new todo with the given title.

- **Preconditions**: title is a non-empty, non-whitespace string.
- **Postconditions**: Todo created with auto-incremented ID, status
  PENDING.
- **Errors**: Raises ValueError if title is empty or whitespace-only.

### get_all_todos() → list[Todo]

Returns all todos ordered by ID.

- **Preconditions**: None.
- **Postconditions**: Returns list (possibly empty).
- **Errors**: None.

### mark_complete(todo_id: int) → Todo

Marks a todo as completed.

- **Preconditions**: todo_id refers to an existing todo.
- **Postconditions**: Todo status set to COMPLETED.
- **Errors**: Raises KeyError if todo not found. Raises ValueError
  if todo is already completed.

### update_todo(todo_id: int, title: str) → Todo

Updates the title of an existing todo.

- **Preconditions**: todo_id refers to an existing todo; title is
  non-empty, non-whitespace.
- **Postconditions**: Todo title updated.
- **Errors**: Raises KeyError if todo not found. Raises ValueError
  if title is empty or whitespace-only.

### delete_todo(todo_id: int) → bool

Deletes a todo by ID.

- **Preconditions**: todo_id refers to an existing todo.
- **Postconditions**: Todo removed from repository.
- **Errors**: Raises KeyError if todo not found.

## Error Taxonomy

| Error Type   | Meaning                        | CLI Display                     |
|-------------|--------------------------------|---------------------------------|
| ValueError  | Invalid input (empty title,    | Display error message, return   |
|             | already completed)             | to menu                         |
| KeyError    | Todo not found by ID           | "Todo not found."               |
