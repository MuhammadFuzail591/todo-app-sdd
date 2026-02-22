# Tasks: Todo In-Memory Python Console App (Phase I)

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/service-contract.md, quickstart.md

**Tests**: Included — plan.md specifies pytest-based unit testing for domain and service layers (constitution principle IV: Testability).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/todo_app/` (src-layout), `tests/unit/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, UV configuration, and directory structure

- [ ] T001 Create pyproject.toml with project metadata (name: todo-app, requires-python >=3.13, empty dependencies, dev-dependencies: pytest>=8.0 and ruff>=0.9, script entry-point: todo-app = "todo_app.__main__:main", ruff config: line-length=88, target-version=py313) in pyproject.toml
- [ ] T002 Create project directory structure: src/todo_app/__init__.py, src/todo_app/domain/__init__.py, src/todo_app/services/__init__.py, src/todo_app/cli/__init__.py, tests/__init__.py, tests/unit/__init__.py (all empty __init__.py files)
- [ ] T003 Run `uv sync` to generate uv.lock and install dev dependencies

**Checkpoint**: Project skeleton ready — `uv run python -c "import todo_app"` succeeds

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Domain models and repository abstraction that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 [P] Implement Status enum (PENDING, COMPLETED) and Todo dataclass (id: int, title: str, status: Status defaulting to PENDING) in src/todo_app/domain/models.py
- [ ] T005 [P] Implement TodoRepository ABC with abstract methods (add(title: str) → Todo, get(id: int) → Todo | None, get_all() → list[Todo], update(id: int, title: str) → Todo | None, delete(id: int) → bool) and InMemoryTodoRepository (dict-based storage, auto-increment counter starting at 1, deleted IDs never reused) in src/todo_app/domain/repository.py
- [ ] T006 [P] Write unit tests for Todo dataclass creation and Status enum values in tests/unit/test_models.py
- [ ] T007 [P] Write unit tests for InMemoryTodoRepository: add, get, get_all, update, delete, auto-increment behavior, deleted ID not reused, get returns None for missing ID, delete returns False for missing ID in tests/unit/test_repository.py
- [ ] T008 Run `uv run pytest tests/unit/test_models.py tests/unit/test_repository.py` — all tests must pass

**Checkpoint**: Foundation ready — domain models and repository are tested and working

---

## Phase 3: User Story 1 — Add a New Todo (Priority: P1) 🎯 MVP

**Goal**: Users can add a todo by providing a title; system validates input and confirms creation with assigned ID

**Independent Test**: Launch app → select "Add Todo" → enter title → see confirmation with ID. Also test empty/whitespace title rejection.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Write unit tests for TodoService.add_todo(): valid title returns Todo with auto-ID and PENDING status, empty title raises ValueError, whitespace-only title raises ValueError in tests/unit/test_service.py

### Implementation for User Story 1

- [ ] T010 [US1] Implement TodoService class with constructor accepting TodoRepository (dependency injection) and add_todo(title: str) → Todo method (strip + validate title, delegate to repository) in src/todo_app/services/todo_service.py
- [ ] T011 [US1] Run `uv run pytest tests/unit/test_service.py -k "add"` — add_todo tests must pass

**Checkpoint**: User Story 1 service logic is tested — add_todo works with validation

---

## Phase 4: User Story 2 — View All Todos (Priority: P1)

**Goal**: Users can view all todos as a formatted list showing ID, title, and status; empty list shows "No todos found."

**Independent Test**: Add one or more todos via service → call get_all_todos → verify list contains all items with correct fields.

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T012 [P] [US2] Write unit tests for TodoService.get_all_todos(): returns empty list when no todos, returns all todos ordered by ID after adding multiple in tests/unit/test_service.py

### Implementation for User Story 2

- [ ] T013 [US2] Add get_all_todos() → list[Todo] method to TodoService (delegates to repository.get_all()) in src/todo_app/services/todo_service.py
- [ ] T014 [US2] Run `uv run pytest tests/unit/test_service.py -k "get_all"` — get_all_todos tests must pass

**Checkpoint**: User Story 2 service logic is tested — get_all_todos works

---

## Phase 5: User Story 3 — Mark Todo as Complete (Priority: P2)

**Goal**: Users can mark a pending todo as completed by ID; already-completed todos show feedback; missing IDs show error

**Independent Test**: Add a todo → mark complete by ID → verify status changed. Also test already-completed and not-found cases.

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T015 [P] [US3] Write unit tests for TodoService.mark_complete(): pending todo transitions to COMPLETED, already-completed raises ValueError("Todo is already completed."), missing ID raises KeyError in tests/unit/test_service.py

### Implementation for User Story 3

- [ ] T016 [US3] Add mark_complete(todo_id: int) → Todo method to TodoService (get from repo, check status, update status, return) in src/todo_app/services/todo_service.py
- [ ] T017 [US3] Run `uv run pytest tests/unit/test_service.py -k "mark_complete"` — mark_complete tests must pass

**Checkpoint**: User Story 3 service logic is tested — mark_complete works with all edge cases

---

## Phase 6: User Story 4 — Update Todo Title (Priority: P3)

**Goal**: Users can update the title of an existing todo by ID; empty titles rejected; missing IDs show error

**Independent Test**: Add a todo → update title by ID → verify title changed. Also test empty title and not-found cases.

### Tests for User Story 4

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T018 [P] [US4] Write unit tests for TodoService.update_todo(): valid update returns updated Todo, empty title raises ValueError, missing ID raises KeyError in tests/unit/test_service.py

### Implementation for User Story 4

- [ ] T019 [US4] Add update_todo(todo_id: int, title: str) → Todo method to TodoService (validate title, delegate to repository, raise KeyError if None returned) in src/todo_app/services/todo_service.py
- [ ] T020 [US4] Run `uv run pytest tests/unit/test_service.py -k "update"` — update_todo tests must pass

**Checkpoint**: User Story 4 service logic is tested — update_todo works with validation

---

## Phase 7: User Story 5 — Delete a Todo (Priority: P3)

**Goal**: Users can delete a todo by ID; missing IDs show error

**Independent Test**: Add a todo → delete by ID → verify it no longer appears in get_all. Also test not-found case.

### Tests for User Story 5

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T021 [P] [US5] Write unit tests for TodoService.delete_todo(): existing todo returns True and is removed, missing ID raises KeyError in tests/unit/test_service.py

### Implementation for User Story 5

- [ ] T022 [US5] Add delete_todo(todo_id: int) → bool method to TodoService (delegate to repository, raise KeyError if False returned) in src/todo_app/services/todo_service.py
- [ ] T023 [US5] Run `uv run pytest tests/unit/test_service.py -k "delete"` — delete_todo tests must pass

**Checkpoint**: User Story 5 service logic is tested — delete_todo works

---

## Phase 8: User Story 6 — CLI Layer & Exit (Priority: P1)

**Goal**: Full interactive menu loop with all 5 operations + clean exit. CLI handles input parsing, output formatting, error presentation. No business logic in CLI.

**Independent Test**: Run `uv run todo-app` → execute full workflow: add, view, complete, update, delete, exit. Verify all menus, confirmations, and error messages match spec.

### Implementation for User Story 6

- [ ] T024 [US6] Implement TodoApp class in src/todo_app/cli/app.py with:
  - Constructor accepting TodoService
  - run() method with menu loop displaying options (1-6)
  - Handler methods for each operation: _add_todo(), _view_todos(), _mark_complete(), _update_todo(), _delete_todo()
  - Input parsing: numeric ID validation with "Invalid ID. Please enter a number." error
  - Invalid menu option: "Invalid option. Please try again."
  - Error handling: catch ValueError/KeyError from service, display user-friendly messages
  - Output formatting: "[ID] title (status)" for confirmations, "- " prefix for list items
  - Exit: display "Goodbye!" and terminate loop
- [ ] T025 [US6] Implement main() function in src/todo_app/__main__.py that wires InMemoryTodoRepository → TodoService → TodoApp and calls run()
- [ ] T026 [US6] Run full integration test manually: `uv run todo-app` and execute the example session from quickstart.md (add 2 todos, view, complete, update, delete, exit)

**Checkpoint**: Application is fully functional end-to-end — all 6 user stories work through the CLI

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, linting, and test suite completion

- [ ] T027 [P] Run `uv run ruff check src/ tests/` and fix any linting issues
- [ ] T028 [P] Run `uv run ruff format src/ tests/` to ensure consistent formatting
- [ ] T029 Run full test suite: `uv run pytest tests/ -v` — all tests must pass
- [ ] T030 Run quickstart.md validation: execute the full example session from specs/001-todo-console-app/quickstart.md and verify output matches expected behavior
- [ ] T031 Verify type hints on all public functions and parameters across src/todo_app/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) completion — BLOCKS all user stories
- **User Stories 1-5 (Phases 3-7)**: All depend on Foundational (Phase 2) completion
  - US1 (Add) and US2 (View) are independent of each other
  - US3 (Mark Complete) can proceed independently (needs add for testing but not for implementation)
  - US4 (Update) and US5 (Delete) are independent of each other and US3
- **User Story 6 / CLI (Phase 8)**: Depends on ALL service methods being implemented (Phases 3-7)
- **Polish (Phase 9)**: Depends on Phase 8 completion

### User Story Dependencies

- **US1 (Add — P1)**: After Phase 2 — No dependencies on other stories
- **US2 (View — P1)**: After Phase 2 — No dependencies on other stories
- **US3 (Mark Complete — P2)**: After Phase 2 — Independent (uses its own add in tests)
- **US4 (Update — P3)**: After Phase 2 — Independent (uses its own add in tests)
- **US5 (Delete — P3)**: After Phase 2 — Independent (uses its own add in tests)
- **US6 (CLI + Exit — P1)**: After Phases 3-7 — Integrates all service methods

### Within Each User Story (Service Layer)

1. Tests MUST be written and FAIL before implementation
2. Implement service method
3. Run targeted tests — must pass
4. Story complete before moving to next priority

### Parallel Opportunities

- **Phase 2**: T004, T005, T006, T007 can all run in parallel (different files)
- **Phases 3-7**: US1 tests (T009), US2 tests (T012), US3 tests (T015), US4 tests (T018), US5 tests (T021) can be written in parallel
- **Phase 8**: T024 and T025 can be developed in parallel (different files)
- **Phase 9**: T027 and T028 can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational tasks together (different files):
Task: "Implement Status enum and Todo dataclass in src/todo_app/domain/models.py"
Task: "Implement TodoRepository ABC and InMemoryTodoRepository in src/todo_app/domain/repository.py"
Task: "Write unit tests for models in tests/unit/test_models.py"
Task: "Write unit tests for repository in tests/unit/test_repository.py"
```

## Parallel Example: All Service Tests (after Phase 2)

```bash
# Write all service test methods in parallel (same file but independent test functions):
Task: "Write add_todo tests in tests/unit/test_service.py"
Task: "Write get_all_todos tests in tests/unit/test_service.py"
Task: "Write mark_complete tests in tests/unit/test_service.py"
Task: "Write update_todo tests in tests/unit/test_service.py"
Task: "Write delete_todo tests in tests/unit/test_service.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 + 6 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational — models + repository (T004-T008)
3. Complete Phase 3: User Story 1 — Add Todo service (T009-T011)
4. Complete Phase 4: User Story 2 — View Todos service (T012-T014)
5. Complete Phase 8: CLI — wire up Add + View + Exit only
6. **STOP and VALIDATE**: Test add, view, exit flow end-to-end
7. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Add) + US2 (View) + CLI → Test independently → MVP!
3. Add US3 (Mark Complete) + update CLI → Test independently
4. Add US4 (Update) + US5 (Delete) + update CLI → Test independently
5. Polish → Final validation

### Single Developer Strategy (Recommended)

Execute phases sequentially in order (1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9). Within each phase, follow the test-first approach: write tests, verify they fail, implement, verify they pass.

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story's service method is independently testable
- CLI layer (Phase 8) is the integration point — no business logic there
- All service tests use InMemoryTodoRepository directly (no mocking needed)
- Commit after each phase or logical group
- Stop at any checkpoint to validate independently
