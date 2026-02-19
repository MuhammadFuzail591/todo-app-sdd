# Feature Specification: Todo In-Memory Python Console App (Phase I)

**Feature Branch**: `001-todo-console-app`
**Created**: 2026-02-19
**Status**: Draft
**Input**: User description: "Build a command-line Todo application that stores tasks in memory with 5 basic features (Add, Delete, Update, View, Mark Complete), following Agentic Dev Stack workflow, Python 3.13+, UV managed, src-based layout."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add a New Todo (Priority: P1)

As a user, I want to add a new todo item by providing a title so that
I can track tasks I need to complete. When I select the "Add Todo"
option from the menu and enter a title, the system creates the todo
and confirms it was added successfully.

**Why this priority**: Adding todos is the foundational action. Without
it, no other feature has data to operate on. This is the minimum viable
interaction.

**Independent Test**: Can be fully tested by launching the app, selecting
"Add Todo", typing a title, and verifying the confirmation message
displays. Delivers the ability to capture tasks.

**Acceptance Scenarios**:

1. **Given** the app is running and the main menu is displayed,
   **When** the user selects "Add Todo" and enters "Buy groceries",
   **Then** the system creates a todo with title "Buy groceries",
   assigns it a unique ID, sets status to "pending", and displays
   a confirmation message with the todo ID.

2. **Given** the app is running,
   **When** the user selects "Add Todo" and enters an empty title,
   **Then** the system displays an error message "Title cannot be empty"
   and returns to the menu without creating a todo.

3. **Given** the app is running,
   **When** the user selects "Add Todo" and enters a title with only
   whitespace,
   **Then** the system displays an error message "Title cannot be empty"
   and returns to the menu without creating a todo.

---

### User Story 2 - View All Todos (Priority: P1)

As a user, I want to view all my todos in a list so that I can see
what tasks I have and their current status.

**Why this priority**: Viewing is essential to verify any other operation
worked. Co-priority with Add because adding without viewing provides
no feedback loop.

**Independent Test**: Can be tested by adding one or more todos, then
selecting "View Todos" and verifying the list displays all items with
their IDs, titles, and statuses.

**Acceptance Scenarios**:

1. **Given** one or more todos exist,
   **When** the user selects "View Todos",
   **Then** the system displays a formatted list showing each todo's
   ID, title, and status (pending/completed).

2. **Given** no todos exist,
   **When** the user selects "View Todos",
   **Then** the system displays "No todos found." and returns to the
   main menu.

---

### User Story 3 - Mark Todo as Complete (Priority: P2)

As a user, I want to mark a todo as complete so that I can track
which tasks are finished.

**Why this priority**: Completing a todo is the primary workflow
closure. It changes state and gives meaning to the status field.

**Independent Test**: Can be tested by adding a todo, marking it
complete by ID, then viewing todos to confirm the status changed
to "completed".

**Acceptance Scenarios**:

1. **Given** a todo with ID 1 exists in "pending" status,
   **When** the user selects "Mark Complete" and enters ID 1,
   **Then** the system updates the todo status to "completed" and
   displays a confirmation message.

2. **Given** a todo with ID 1 exists in "completed" status,
   **When** the user selects "Mark Complete" and enters ID 1,
   **Then** the system displays "Todo is already completed." and
   makes no changes.

3. **Given** no todo exists with ID 99,
   **When** the user selects "Mark Complete" and enters ID 99,
   **Then** the system displays "Todo not found." and returns to
   the menu.

---

### User Story 4 - Update Todo Title (Priority: P3)

As a user, I want to update the title of an existing todo so that
I can correct mistakes or refine task descriptions.

**Why this priority**: Updating is a secondary editing capability.
The core workflow (add, view, complete) works without it.

**Independent Test**: Can be tested by adding a todo, updating its
title by ID, then viewing todos to confirm the title changed.

**Acceptance Scenarios**:

1. **Given** a todo with ID 1 exists with title "Buy groceries",
   **When** the user selects "Update Todo", enters ID 1, and provides
   new title "Buy organic groceries",
   **Then** the system updates the title and displays a confirmation.

2. **Given** no todo exists with ID 99,
   **When** the user selects "Update Todo" and enters ID 99,
   **Then** the system displays "Todo not found." and returns to
   the menu.

3. **Given** a todo with ID 1 exists,
   **When** the user selects "Update Todo", enters ID 1, and provides
   an empty new title,
   **Then** the system displays "Title cannot be empty" and makes no
   changes.

---

### User Story 5 - Delete a Todo (Priority: P3)

As a user, I want to delete a todo so that I can remove tasks that
are no longer relevant.

**Why this priority**: Deletion is a cleanup operation. The app is
fully functional without it since todos can simply be marked complete.

**Independent Test**: Can be tested by adding a todo, deleting it
by ID, then viewing todos to confirm it no longer appears.

**Acceptance Scenarios**:

1. **Given** a todo with ID 1 exists,
   **When** the user selects "Delete Todo" and enters ID 1,
   **Then** the system removes the todo and displays a confirmation
   message.

2. **Given** no todo exists with ID 99,
   **When** the user selects "Delete Todo" and enters ID 99,
   **Then** the system displays "Todo not found." and returns to
   the menu.

---

### User Story 6 - Exit Application (Priority: P1)

As a user, I want to exit the application cleanly so that the
program terminates gracefully.

**Why this priority**: Without a clean exit, the user must force-kill
the process. This is a fundamental UX requirement.

**Independent Test**: Can be tested by selecting "Exit" from the menu
and verifying the application terminates with a goodbye message.

**Acceptance Scenarios**:

1. **Given** the app is running and the main menu is displayed,
   **When** the user selects "Exit",
   **Then** the system displays "Goodbye!" and terminates.

---

### Edge Cases

- What happens when the user enters a non-numeric value for a todo ID?
  The system MUST display "Invalid ID. Please enter a number." and
  return to the menu.
- What happens when the user selects an invalid menu option?
  The system MUST display "Invalid option. Please try again." and
  re-display the menu.
- What happens when the user enters an extremely long title (>200 chars)?
  The system MUST accept it. No artificial length limits are imposed
  in Phase I.
- What happens if the user enters a negative or zero ID?
  The system MUST display "Todo not found." (IDs start from 1).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a new todo by providing
  a title string.
- **FR-002**: System MUST assign a unique, auto-incrementing integer
  ID to each new todo starting from 1.
- **FR-003**: System MUST set new todos to "pending" status by default.
- **FR-004**: System MUST allow users to view all todos as a formatted
  list showing ID, title, and status.
- **FR-005**: System MUST allow users to mark a todo as "completed"
  by specifying its ID.
- **FR-006**: System MUST allow users to update the title of an
  existing todo by specifying its ID and a new title.
- **FR-007**: System MUST allow users to delete a todo by specifying
  its ID.
- **FR-008**: System MUST validate all user inputs and display
  meaningful error messages for invalid input.
- **FR-009**: System MUST present a numbered menu of available
  operations on each loop iteration.
- **FR-010**: System MUST allow the user to exit the application
  cleanly from the main menu.
- **FR-011**: System MUST store all data in memory only; no data
  persists between application runs.
- **FR-012**: System MUST prevent marking an already-completed todo
  as complete again (idempotency guard with user feedback).

### Key Entities

- **Todo**: Represents a single task. Attributes: unique integer ID,
  title (non-empty string), status (pending or completed).
- **TodoRepository**: Abstraction for storing and retrieving todos.
  Operations: add, get by ID, get all, update, delete. Phase I uses
  an in-memory implementation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a todo and see it in the list within a
  single session in under 10 seconds of interaction.
- **SC-002**: All five core operations (add, view, mark complete,
  update, delete) function correctly and return appropriate feedback.
- **SC-003**: 100% of invalid inputs (empty titles, non-numeric IDs,
  non-existent IDs, invalid menu choices) produce clear, specific
  error messages rather than crashes.
- **SC-004**: Application runs a full workflow cycle (add, view,
  complete, update, delete, exit) without errors.
- **SC-005**: Application starts and presents the menu within 1 second.
- **SC-006**: All business logic is testable independently of the
  console interface.
- **SC-007**: Code follows clean architecture with at least 3 distinct
  layers (domain, service, CLI).

## Assumptions

- Single-user application; no concurrency considerations needed.
- Todo IDs are auto-incrementing integers starting from 1. Deleted IDs
  are not reused within a session.
- The menu is text-based and loops until the user selects "Exit".
- No confirmation prompts before destructive actions (delete) in
  Phase I. This keeps the interface simple.
- UV is used for project management (pyproject.toml, src-based layout).
- Python 3.13+ is the target runtime.
- No external dependencies beyond the Python standard library.

## Scope Boundaries

### In Scope

- Console-based CRUD operations for todos
- In-memory storage with repository abstraction
- Input validation and error handling
- Clean separation: domain model, service layer, CLI layer
- Unit-testable business logic

### Out of Scope

- Web interface, REST API, or any non-console interface
- Database integration or file persistence
- Authentication, authorization, or multi-user support
- AI integration or chatbot features
- Docker, Kubernetes, or cloud deployment
- Advanced features: priority levels, tags, due dates, categories,
  search, filtering, sorting
