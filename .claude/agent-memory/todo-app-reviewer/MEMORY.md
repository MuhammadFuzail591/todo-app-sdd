# Todo App Reviewer - Agent Memory

## Project Structure (Confirmed)
- Source: `src/todo_app/` with 3 layers: `domain/`, `services/`, `cli/`
- Tests: `tests/unit/` with 4 test files: test_models.py, test_repository.py, test_service.py, test_main.py
- Entry point: `src/todo_app/__main__.py` with `if __name__ == "__main__"` guard
- Specs: `specs/001-todo-console-app/` with spec.md, plan.md, tasks.md, data-model.md, contracts/service-contract.md

## Architecture Patterns
- Domain layer: `models.py` (Status enum + Todo dataclass), `repository.py` (ABC + InMemoryTodoRepository)
- Service layer: `todo_service.py` - TodoService with dependency injection of TodoRepository
- CLI layer: `app.py` - TodoApp with dependency injection of TodoService
- Dependency flow: CLI -> Service -> Domain (correct, no violations)
- No `input()`/`print()` in domain or service layers (clean separation confirmed)

## Recurring Review Findings
- **KeyboardInterrupt/EOFError**: Not handled in CLI `run()` method or `__main__.py`. Ctrl+C/Ctrl+D will crash with traceback.
- **mark_complete mutates directly**: `todo.status = Status.COMPLETED` in service layer bypasses repository - works due to shared reference in dict but is architecturally impure.
- **No docstrings on service methods**: `_validate_title`, `add_todo`, `get_all_todos`, `mark_complete`, `update_todo`, `delete_todo` all lack docstrings.
- **CLI has no test for "already completed"**: test_main.py does not test the already-completed scenario through CLI.
- See [review-findings.md](review-findings.md) for full details.
