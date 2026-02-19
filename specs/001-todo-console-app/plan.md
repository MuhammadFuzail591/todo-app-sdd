# Implementation Plan: Todo In-Memory Python Console App (Phase I)

**Branch**: `001-todo-console-app` | **Date**: 2026-02-19 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-todo-console-app/spec.md`

## Summary

Build a command-line Todo application with five core operations (add,
view, mark complete, update, delete) using pure in-memory storage.
Architecture follows clean layered design: domain models → service
layer → CLI layer. Python 3.13+ with UV package management, src-based
layout, no external runtime dependencies.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (stdlib only; pytest as dev dependency)
**Storage**: In-memory dictionary (no persistence)
**Testing**: pytest
**Target Platform**: Any platform with Python 3.13+
**Project Type**: Single project (src-layout)
**Performance Goals**: Menu response < 1 second (trivially met)
**Constraints**: No external frameworks, no persistence, stdlib only
**Scale/Scope**: Single-user, single-session, ~5 operations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. Spec-First | spec.md exists and is approved | PASS |
| II. Incremental Architecture | Repository abstraction enables Phase II migration | PASS |
| III. Clean Architecture | 3 layers: domain, service, CLI. No business logic in CLI | PASS |
| IV. Testability | Service and domain testable without CLI dependency | PASS |
| V. Observability | Structured logging from Phase I (basic print-based feedback) | PASS |
| VI. AI-Augmented Dev | N/A for Phase I (no AI integration) | N/A |
| VII. Reproducibility | UV lockfile + pyproject.toml ensure reproducible env | PASS |

**Code Quality Standards**:
- Type hints: All functions and parameters typed | PASS
- Linting: Ruff configured in pyproject.toml | PASS
- Modular structure: domain/, services/, cli/ | PASS

**Phase I Constraints**:
- Pure in-memory storage only | PASS
- Console-based interface only | PASS
- No database, no file persistence | PASS

All gates pass. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── service-contract.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
└── todo_app/
    ├── __init__.py
    ├── __main__.py          # Entry point (uv run todo-app)
    ├── domain/
    │   ├── __init__.py
    │   ├── models.py        # Todo dataclass, Status enum
    │   └── repository.py    # TodoRepository ABC, InMemoryTodoRepository
    ├── services/
    │   ├── __init__.py
    │   └── todo_service.py  # TodoService (business logic + validation)
    └── cli/
        ├── __init__.py
        └── app.py           # Menu loop, input parsing, output formatting

tests/
└── unit/
    ├── __init__.py
    ├── test_models.py       # Todo creation, Status enum
    ├── test_repository.py   # InMemoryTodoRepository CRUD
    └── test_service.py      # TodoService validation + business logic
```

**Structure Decision**: Single project with src-layout. The `todo_app`
package under `src/` prevents accidental imports. Domain, services, and
CLI are separate sub-packages matching the 3-layer architecture required
by constitution principle III. Tests mirror source structure under
`tests/unit/`.

## Complexity Tracking

No constitution violations. No complexity justification needed.

## Layer Responsibilities

### Domain Layer (`domain/`)

- `models.py`: Todo dataclass (id, title, status), Status enum
  (PENDING, COMPLETED)
- `repository.py`: TodoRepository ABC (abstract methods: add, get,
  get_all, update, delete), InMemoryTodoRepository (dict-based
  implementation with auto-increment counter)
- **Rules**: No imports from services/ or cli/. Pure data and contracts.

### Service Layer (`services/`)

- `todo_service.py`: TodoService class that accepts a TodoRepository
  in its constructor (dependency injection). Contains all business
  logic: title validation, status transition guards, delegation to
  repository.
- **Rules**: No imports from cli/. No direct I/O. Raises ValueError
  and KeyError for invalid operations.

### CLI Layer (`cli/`)

- `app.py`: TodoApp class with run() method. Implements the menu loop,
  input parsing (reads from stdin), output formatting (writes to
  stdout), and error presentation. Catches service exceptions and
  translates them to user-friendly messages.
- **Rules**: No business logic. Only I/O and delegation to TodoService.

### Entry Point (`__main__.py`)

- Wires together: creates InMemoryTodoRepository, injects into
  TodoService, injects into TodoApp, calls run().
- **Rules**: Only composition. No logic.

## Dependency Flow

```text
__main__.py
    └── cli/app.py (TodoApp)
        └── services/todo_service.py (TodoService)
            └── domain/repository.py (TodoRepository ABC)
                └── domain/models.py (Todo, Status)
```

Dependencies flow inward: CLI → Service → Domain. Domain depends on
nothing. This ensures domain logic is testable in isolation.

## Testing Strategy

All tests target the service and domain layers directly. No CLI
testing via subprocess in Phase I (CLI is a thin wrapper).

| Test File           | What It Tests                         |
|---------------------|---------------------------------------|
| test_models.py      | Todo creation, Status enum values     |
| test_repository.py  | Add, get, get_all, update, delete     |
|                     | Auto-increment, deleted ID not reused |
| test_service.py     | Title validation (empty, whitespace)  |
|                     | Mark complete (success, already done, |
|                     | not found)                            |
|                     | Update (success, not found, empty)    |
|                     | Delete (success, not found)           |

## Configuration

### pyproject.toml

- **name**: todo-app
- **requires-python**: ">=3.13"
- **dependencies**: [] (empty — stdlib only)
- **dev-dependencies**: ["pytest>=8.0", "ruff>=0.9"]
- **scripts**: todo-app = "todo_app.__main__:main"
- **ruff**: line-length = 88, target-version = "py313"
