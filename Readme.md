# Task Tracker CLI

Project URL: https://roadmap.sh/projects/task-tracker
A simple command-line interface (CLI) application to track and manage your tasks. Built with Python using native libraries and featuring a clean table display for better readability.

## Features

- Add new tasks with automatic ID assignment
- Update existing task descriptions
- Delete tasks with automatic ID reassignment
- Mark tasks as in-progress or done
- List all tasks or filter by status
- Pretty table display using Texttable
- Persistent storage using JSON file
- Comprehensive error handling
- Automatic timestamps for task creation and updates
- Full test suite with unittest

## Requirements

- Python 3.6 or higher
- `texttable` library for pretty table display

## Installation

1. Clone or download the project files:
   - `taskcli.py` - Main application
   - `test_taskcli.py` - Unit tests

2. Install the required dependency:
   ```bash
   pip install texttable
   ```


## Usage

### Basic Syntax
```bash
python taskcli.py <command> [arguments]
```

### Commands

#### Add a New Task
```bash
python taskcli.py add "Buy groceries"
# Output: Task added successfully
# Displays updated task table
```

#### Update a Task
```bash
python taskcli.py update 1 "Buy groceries and cook dinner"
# Output: Task ID:1 update successfully at 2024-06-04 15:30
```

#### Delete a Task
```bash
python taskcli.py delete 1
# Output: Task ID:1 deleted successfully
```
**Note:** After deletion, all remaining task IDs are automatically reassigned sequentially starting from 1.

#### Mark Task Status
```bash
# Mark as in progress
python taskcli.py mark-in-progress 1
# Output: Task ID:1 marked as in-progress successfully

# Mark as done
python taskcli.py mark-done 1
# Output: Task ID:1 marked as done successfully
```

#### List Tasks
```bash
# List all tasks
python taskcli.py list

# List only completed tasks
python taskcli.py list done

# List only pending tasks
python taskcli.py list to-do

# List only tasks in progress
python taskcli.py list in-progress
```

#### Get Help
```bash
python taskcli.py help
# Displays all available commands with usage instructions
```

### Example Output

```bash
$ python taskcli.py list
+----+---------------------------+-------------+------------------+------------------+
| ID | Description               | Status      | createdAt        | updatedAt        |
+====+===========================+=============+==================+==================+
| 1  | Buy groceries             | to-do       | 2024-06-04 10:30 | None             |
| 2  | Write project report      | in-progress | 2024-06-04 11:15 | 2024-06-04 14:20 |
| 3  | Setup development env     | done        | 2024-06-04 09:45 | 2024-06-04 12:10 |
+----+---------------------------+-------------+------------------+------------------+
```

## Task Properties

Each task contains the following properties:

- **id**: Unique identifier (automatically assigned and reassigned after deletions)
- **description**: Task description provided by user
- **status**: Current status (`to-do`, `in-progress`, `done`)
- **createdAt**: Timestamp when task was created (YYYY-MM-DD HH:MM format)
- **updatedAt**: Timestamp when task was last modified (initially `None`)

## Data Storage

Tasks are stored in a `tasks.json` file in the same directory as the script. The file structure:

```json
{
  "Tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "status": "to-do",
      "createdAt": "2024-06-04 10:30",
      "updatedAt": null
    },
    {
      "id": 2,
      "description": "Write documentation",
      "status": "done",
      "createdAt": "2024-06-04 11:15",
      "updatedAt": "2024-06-04 14:30"
    }
  ]
}
```

## Important Notes

1. **Task Descriptions**: Must be enclosed in quotes when adding or updating tasks
2. **ID Management**: Task IDs are automatically reassigned after deletions to maintain sequential order
3. **Status Values**: The application uses `to-do` (not `todo`) as the default status
4. **File Creation**: The JSON file is created automatically if it doesn't exist

## Error Handling

The application handles various scenarios gracefully:

- **Invalid Task IDs**: Shows "not found" message with suggestion to use `list` command
- **Empty Task List**: Displays appropriate message when no tasks exist
- **Missing Arguments**: Shows invalid command message
- **Non-existent Commands**: Provides guidance to use `help` command
- **Invalid Status Filters**: Shows error for unknown status filters

## Testing

The project includes a comprehensive test suite (`test_taskcli.py`) that covers:

- Adding tasks
- Listing all tasks and filtering by status
- Updating task descriptions
- Deleting tasks
- Marking tasks as done/in-progress
- Error handling for invalid operations
- Help command functionality

### Running Tests

```bash
python test_taskcli.py
```

The test suite uses Python's `unittest` framework and includes:
- **Setup/Teardown**: Ensures test isolation
- **Mock Output Capture**: Tests console output
- **File Verification**: Confirms JSON file changes
- **Edge Cases**: Tests invalid operations and error conditions

### Test Coverage

- Task addition with verification
- Task listing and filtering
- Task updates and status changes
- Task deletion with file verification
- Error handling for invalid IDs
- Help command output
- Invalid command handling
- Missing argument scenarios

## Project Structure

```
task-tracker/
├── taskcli.py          # Main CLI application
├── test_taskcli.py     # Unit test suite
├── tasks.json          # Auto-generated task storage(generated during the execution)
└── README.md           # This documentation
```

## Development

### Key Functions

- `load_file()`: Loads tasks from JSON file or creates empty structure
- `save_file(data)`: Saves task data to JSON file
- `print_filetable(sts=None)`: Displays tasks in table format with optional filtering
- `add_task(desc)`: Adds new task with auto-generated ID
- `del_task(tsk_id)`: Deletes task and reassigns IDs
- `update_task(tsk_id, tsk_value)`: Updates task description
- `status_update(tsk_id, mrkflag)`: Changes task status
- `print_help()`: Displays command usage help

### Design Decisions

1. **Sequential ID Management**: IDs are reassigned after deletions to maintain order
2. **Pretty Table Display**: Uses Texttable for better readability
3. **Status Naming**: Uses `to-do` instead of `todo` for consistency
4. **Comprehensive Testing**: Full test coverage for reliability
5. **User-Friendly Messages**: Clear feedback for all operations

## Contributing

To enhance the application, consider adding:

- Task priorities or categories
- Due dates and reminders
- Task search functionality
- Export/import capabilities
- Configuration file support
- Colored output for better visibility

## License

This project is open source and available under the MIT License.