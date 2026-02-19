# Research: Todo In-Memory Python Console App (Phase I)

**Branch**: `001-todo-console-app` | **Date**: 2026-02-19

## Phase 0: Research Findings

### R1: Python Project Structure (UV + src-layout)

**Decision**: Use UV-managed project with src-based layout.

**Rationale**: UV provides fast dependency resolution, lockfile support,
and Python version management. The src-layout (`src/todo_app/`) prevents
accidental imports from the project root and enforces proper packaging.

**Alternatives considered**:
- Flat layout (`todo_app/` at root) — simpler but allows accidental
  relative imports; rejected for Phase II compatibility.
- Poetry — viable but UV is specified in requirements and offers
  faster resolution.

### R2: Domain Model Pattern

**Decision**: Use dataclass-based Todo entity with Enum for status.

**Rationale**: Python dataclasses provide clean, typed data containers
with no external dependencies. Enum for status ensures type safety
and prevents invalid state values.

**Alternatives considered**:
- NamedTuple — immutable, which complicates status updates.
- Plain dict — no type safety, harder to test, violates constitution
  principle III (Clean Architecture).
- Pydantic — adds external dependency; overkill for Phase I with no
  serialization needs.

### R3: Repository Abstraction

**Decision**: Use abstract base class (ABC) for repository interface
with an in-memory dictionary-based implementation.

**Rationale**: ABC defines the contract that Phase II will implement
with SQLModel. Dictionary provides O(1) lookups by ID. This satisfies
constitution principle II (Incremental Architecture Evolution) by
ensuring the repository interface survives phase transitions.

**Alternatives considered**:
- Protocol (structural typing) — viable but ABC is more explicit
  about the contract and provides runtime enforcement via
  abstractmethod.
- No abstraction (direct dict) — violates constitution principle III
  and blocks Phase II migration.

### R4: Testing Framework

**Decision**: Use pytest with standard library only.

**Rationale**: pytest is the de facto Python testing standard. It
provides clean assertions, fixtures, and parametrize for edge cases.
While it is an external dependency, it is a dev-only dependency and
universally expected in Python projects.

**Alternatives considered**:
- unittest — stdlib but verbose; pytest is industry standard.
- No testing framework — violates constitution principle IV
  (Testability).

### R5: CLI Input Handling

**Decision**: Use built-in `input()` function with a menu loop pattern.

**Rationale**: No external dependencies needed. The menu loop is
simple, deterministic, and testable when the CLI layer is separated
from business logic. The service layer receives parsed inputs, not
raw stdin.

**Alternatives considered**:
- argparse — designed for command-line arguments, not interactive
  menu loops.
- click/typer — adds external dependency; overkill for Phase I.
- Rich — adds visual polish but is an external dependency.

### R6: ID Generation Strategy

**Decision**: Auto-incrementing integer counter maintained in the
repository implementation. Counter persists across deletions (deleted
IDs are not reused within a session).

**Rationale**: Simple, predictable, and deterministic. Matches spec
FR-002. Counter is internal to the repository, not exposed as a
global.

**Alternatives considered**:
- UUID — overkill for Phase I; harder for users to type in CLI.
- Random int — non-deterministic; harder to test.

## Summary

All technical decisions are resolved. No NEEDS CLARIFICATION items
remain. The stack is: Python 3.13+, UV, pytest (dev), stdlib only
for production code.
