import unittest
import os
import json
import sys
from io import StringIO
from unittest.mock import patch
import taskcli

class TestTaskCLI(unittest.TestCase):

    def setUp(self):
        """
        Runs before each test.
        Resets the tasks file with an empty task list to ensure test isolation.
        """
        self.filename = taskcli.filename
        if os.path.exists(self.filename):
            os.remove(self.filename)
        with open(self.filename, 'w') as f:
            json.dump({"Tasks": []}, f)

    def tearDown(self):
        """
        Runs after each test.
        Deletes the tasks file to clean up.
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def run_cli_with_args(self, args):
        """
        Helper method to run CLI commands with given arguments and capture printed output.
        """
        with patch.object(sys, 'argv', args), patch('sys.stdout', new=StringIO()) as fake_out:
            try:
                taskcli.main()
            except SystemExit:
                pass  # Ignore SystemExit for testing
            return fake_out.getvalue()

    def test_add_task(self):
        """
        Tests if a task is added successfully and appears in the file with correct description.
        """
        output = self.run_cli_with_args(["taskcli.py", "add", "Buy groceries"])
        self.assertIn("Task added successfully", output)
        with open(self.filename) as f:
            data = json.load(f)
            self.assertEqual(len(data["Tasks"]), 1)
            self.assertEqual(data["Tasks"][0]["description"], "Buy groceries")

    def test_list_all_tasks(self):
        """
        Tests if listing tasks shows correct task content and status.
        """
        self.run_cli_with_args(["taskcli.py", "add", "Task A"])
        output = self.run_cli_with_args(["taskcli.py", "list"])
        self.assertIn("Task A", output)
        self.assertIn("to-do", output)

    def test_update_task(self):
        """
        Tests updating a task's description.
        """
        self.run_cli_with_args(["taskcli.py", "add", "Initial Task"])
        output = self.run_cli_with_args(["taskcli.py", "update", "1", "Updated Task"])
        self.assertIn("Task ID:1 update successfully", output)
        with open(self.filename) as f:
            data = json.load(f)
            self.assertEqual(data["Tasks"][0]["description"], "Updated Task")

    def test_delete_task(self):
        """
        Tests deletion of a task and verifies it's removed from file.
        """
        self.run_cli_with_args(["taskcli.py", "add", "Task to delete"])
        output = self.run_cli_with_args(["taskcli.py", "delete", "1"])
        self.assertIn("deleted successfully", output)
        with open(self.filename) as f:
            data = json.load(f)
            self.assertEqual(len(data["Tasks"]), 0)

    def test_mark_done(self):
        """
        Tests if a task can be marked as 'done'.
        """
        self.run_cli_with_args(["taskcli.py", "add", "Finish homework"])
        output = self.run_cli_with_args(["taskcli.py", "mark-done", "1"])
        self.assertIn("marked as done", output)
        with open(self.filename) as f:
            data = json.load(f)
            self.assertEqual(data["Tasks"][0]["status"], "done")

    def test_mark_in_progress(self):
        """
        Tests if a task can be marked as 'in-progress'.
        """
        self.run_cli_with_args(["taskcli.py", "add", "Prepare slides"])
        output = self.run_cli_with_args(["taskcli.py", "mark-in-progress", "1"])
        self.assertIn("marked as in-progress", output)
        with open(self.filename) as f:
            data = json.load(f)
            self.assertEqual(data["Tasks"][0]["status"], "in-progress")

    def test_list_by_status(self):
        """
        Tests filtered listing of tasks by status: done, to-do.
        """
        self.run_cli_with_args(["taskcli.py", "add", "Task 1"])
        self.run_cli_with_args(["taskcli.py", "add", "Task 2"])
        self.run_cli_with_args(["taskcli.py", "mark-done", "2"])

        output_done = self.run_cli_with_args(["taskcli.py", "list", "done"])
        self.assertIn("Task 2", output_done)
        self.assertNotIn("Task 1", output_done)

        output_todo = self.run_cli_with_args(["taskcli.py", "list", "to-do"])
        self.assertIn("Task 1", output_todo)
        self.assertNotIn("Task 2", output_todo)

    def test_invalid_delete(self):
        """
        Tests handling of deletion attempt on non-existent task ID.
        """
        output = self.run_cli_with_args(["taskcli.py", "delete", "99"])
        self.assertTrue("not found" in output or "Your task list is empty" in output)

    def test_invalid_update(self):
        """
        Tests handling of update attempt on non-existent task ID.
        """
        output = self.run_cli_with_args(["taskcli.py", "update", "42", "No task"])
        self.assertTrue("not found" in output or "Your task list is empty" in output)

    def test_help_command(self):
        """
        Tests if the help command prints available command instructions.
        """
        output = self.run_cli_with_args(["taskcli.py", "help"])
        self.assertIn("Available Commands", output)

    def test_missing_command(self):
        """
        Tests behavior when no command is provided.
        """
        output = self.run_cli_with_args(["taskcli.py"])
        self.assertIn("USAGE", output)

    def test_invalid_command(self):
        """
        Tests handling of unrecognized command.
        """
        output = self.run_cli_with_args(["taskcli.py", "nonsense"])
        self.assertIn("Invalid command", output)

# Entry point to run all tests
if __name__ == '__main__':
    unittest.main()
