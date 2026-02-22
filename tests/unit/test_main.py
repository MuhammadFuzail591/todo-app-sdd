import pytest
from unittest.mock import patch

from todo_app.__main__ import main


class TestMain:
    def test_main_wires_and_runs(self) -> None:
        """Test that main() wires repository -> service -> app and runs."""
        inputs = iter(["6"])
        with patch("builtins.input", side_effect=inputs):
            main()

    def test_main_add_and_exit(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test a simple add + exit flow through main()."""
        inputs = iter(["1", "Test todo", "6"])
        with patch("builtins.input", side_effect=inputs):
            main()
        out = capsys.readouterr().out
        assert "Todo added: [1] Test todo (pending)" in out
        assert "Goodbye!" in out

    def test_main_full_workflow(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test full workflow: add, view, complete, update, delete, exit."""
        inputs = iter(
            [
                "1",
                "Buy groceries",
                "2",
                "3",
                "1",
                "4",
                "1",
                "Buy organic groceries",
                "5",
                "1",
                "6",
            ]
        )
        with patch("builtins.input", side_effect=inputs):
            main()
        out = capsys.readouterr().out
        assert "Todo added: [1] Buy groceries (pending)" in out
        assert "[1] Buy groceries - pending" in out
        assert "Todo marked as completed: [1] Buy groceries" in out
        assert "Todo updated: [1] Buy organic groceries (completed)" in out
        assert "Todo deleted." in out
        assert "Goodbye!" in out

    def test_main_invalid_menu_option(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test invalid menu option handling."""
        inputs = iter(["99", "6"])
        with patch("builtins.input", side_effect=inputs):
            main()
        out = capsys.readouterr().out
        assert "Invalid option. Please try again." in out

    def test_main_invalid_id_input(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test non-numeric ID input handling."""
        inputs = iter(["3", "abc", "6"])
        with patch("builtins.input", side_effect=inputs):
            main()
        out = capsys.readouterr().out
        assert "Invalid ID. Please enter a number." in out

    def test_main_not_found(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test todo not found handling."""
        inputs = iter(["3", "99", "6"])
        with patch("builtins.input", side_effect=inputs):
            main()
        out = capsys.readouterr().out
        assert "Todo not found." in out

    def test_main_empty_title(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test empty title validation through CLI."""
        inputs = iter(["1", "", "6"])
        with patch("builtins.input", side_effect=inputs):
            main()
        out = capsys.readouterr().out
        assert "Title cannot be empty" in out

    def test_main_no_todos_view(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test viewing empty todo list."""
        inputs = iter(["2", "6"])
        with patch("builtins.input", side_effect=inputs):
            main()
        out = capsys.readouterr().out
        assert "No todos found." in out
