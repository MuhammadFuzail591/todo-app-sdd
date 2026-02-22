# Detailed Review Findings - Phase I Todo App

## Critical: KeyboardInterrupt/EOFError
- File: `src/todo_app/cli/app.py` line 21 (`run()` method)
- File: `src/todo_app/__main__.py` line 10 (`app.run()` call)
- Neither location wraps the main loop in try/except for KeyboardInterrupt or EOFError
- Result: Ctrl+C or Ctrl+D produces ugly traceback instead of graceful exit

## Warning: mark_complete Bypasses Repository
- File: `src/todo_app/services/todo_service.py` lines 25-31
- Service directly mutates `todo.status = Status.COMPLETED` after calling `repository.get()`
- This works because InMemoryTodoRepository returns the actual object (shared reference)
- But it means the repository's `update()` method is not used for status changes
- This couples the service to the implementation detail that repository returns mutable references

## Warning: Missing Docstrings on Public Service Methods
- File: `src/todo_app/services/todo_service.py`
- Methods without docstrings: add_todo, get_all_todos, mark_complete, update_todo, delete_todo
- Contract docs exist in service-contract.md but code should be self-documenting

## Test Coverage Gaps
- No CLI-level test for "already completed" scenario (test_main.py)
- No CLI-level test for update with empty title through full flow
- No CLI-level test for delete of non-existent todo
- No test for negative/zero ID at CLI level
- No test for whitespace-only menu input
