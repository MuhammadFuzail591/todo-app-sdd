# Data Model: Todo In-Memory Python Console App (Phase I)

**Branch**: `001-todo-console-app` | **Date**: 2026-02-19

## Entities

### Todo

Represents a single task that a user wants to track.

| Field  | Type   | Constraints                        |
|--------|--------|------------------------------------|
| id     | int    | Unique, auto-incrementing from 1   |
| title  | str    | Non-empty, whitespace-trimmed      |
| status | Status | Default: PENDING                   |

### Status (Enum)

Represents the completion state of a todo.

| Value     | Description                    |
|-----------|--------------------------------|
| PENDING   | Todo has not been completed    |
| COMPLETED | Todo has been marked complete  |

## State Transitions

```text
[New Todo] → PENDING → COMPLETED
                         (terminal — no reversal in Phase I)
```

- A todo is created with status PENDING (FR-003).
- A todo transitions from PENDING to COMPLETED via "Mark Complete"
  (FR-005).
- A todo that is already COMPLETED cannot be marked complete again;
  the system returns a user-facing message (FR-012).
- No reverse transition (COMPLETED → PENDING) exists in Phase I.

## Repository Interface

### TodoRepository (Abstract)

| Operation  | Input          | Output         | Notes                    |
|------------|----------------|----------------|--------------------------|
| add        | title: str     | Todo           | Creates with next ID     |
| get        | id: int        | Todo or None   | Returns None if missing  |
| get_all    | —              | list[Todo]     | Ordered by ID            |
| update     | id, title: str | Todo or None   | Returns None if missing  |
| delete     | id: int        | bool           | True if deleted          |

### InMemoryTodoRepository

Implements TodoRepository using an internal dictionary (`dict[int, Todo]`)
and an auto-incrementing counter.

- Counter starts at 1.
- Counter increments on each `add()` call regardless of deletions.
- Deleted IDs are never reused within a session.

## Validation Rules

| Rule                      | Applied At     | Error Message               |
|---------------------------|----------------|-----------------------------|
| Title is non-empty        | Service layer  | "Title cannot be empty"     |
| Title is not whitespace   | Service layer  | "Title cannot be empty"     |
| ID is a valid integer     | CLI layer      | "Invalid ID. Please enter a number." |
| ID exists in repository   | Service layer  | "Todo not found."           |
| Todo is not already done  | Service layer  | "Todo is already completed."|
