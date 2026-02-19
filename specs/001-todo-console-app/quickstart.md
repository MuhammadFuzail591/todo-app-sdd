# Quickstart: Todo In-Memory Python Console App (Phase I)

**Branch**: `001-todo-console-app` | **Date**: 2026-02-19

## Prerequisites

- Python 3.13+
- UV package manager

## Setup

```bash
# Clone and navigate to project
cd phase-I

# Install dependencies (including dev)
uv sync

# Verify installation
uv run python --version
```

## Running the Application

```bash
uv run todo-app
```

This launches the interactive menu:

```text
=== Todo App ===
1. Add Todo
2. View Todos
3. Mark Complete
4. Update Todo
5. Delete Todo
6. Exit
Choose an option:
```

## Example Session

```text
Choose an option: 1
Enter todo title: Buy groceries
Todo added: [1] Buy groceries (pending)

Choose an option: 1
Enter todo title: Read a book
Todo added: [2] Read a book (pending)

Choose an option: 2
[1] Buy groceries - pending
[2] Read a book - pending

Choose an option: 3
Enter todo ID: 1
Todo marked as completed: [1] Buy groceries

Choose an option: 4
Enter todo ID: 2
Enter new title: Read two books
Todo updated: [2] Read two books (pending)

Choose an option: 5
Enter todo ID: 1
Todo deleted: [1] Buy groceries

Choose an option: 6
Goodbye!
```

## Running Tests

```bash
uv run pytest
```

## Project Structure

```text
phase-I/
├── pyproject.toml
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── __main__.py       # Entry point
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── models.py     # Todo, Status
│       │   └── repository.py # Abstract repository
│       ├── services/
│       │   ├── __init__.py
│       │   └── todo_service.py
│       └── cli/
│           ├── __init__.py
│           └── app.py        # Menu loop, I/O
└── tests/
    └── unit/
        ├── __init__.py
        ├── test_models.py
        ├── test_repository.py
        └── test_service.py
```
