# a. Project Title and Description

##  Task Manager Prototype

This is a Python-based Task Manager prototype built using Tkinter for the user interface. The application allows users to manage tasks by adding, editing, deleting, and filtering tasks based on priority or completion status. Tasks can also be saved and loaded from a file for persistence between sessions. The application also features a color-coded task list, with completed tasks highlighted in green and high-priority tasks highlighted in red.

# b. Features
## Features

- Add, edit, and delete tasks
- Filter tasks by priority (Low, Medium, High)
- Mark tasks as completed with a green highlight
- High-priority tasks are highlighted in red
- Save and load tasks from a JSON file
- Task progress tracking (0% to 100%)

# c. Prerequisites
## Prerequisites

Make sure you have the following installed:

- Python 3.6 or higher
- Tkinter (comes pre-installed with Python)
- tkcalendar (for date entry)

# d. Installation

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/shuaihaowang/TaskManager.git
   cd TaskManager

2. Create a virtual environment (optional, but recommended)
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate

3. Install the required dependencies
pip install -r requirements.txt

The dependencies include:

tkinter: For the GUI (comes pre-installed with Python)
tkcalendar: For the DateEntry widget (installed via pip)

4. Run the application:
python main.py

# **e. Project Structure**

```markdown
## Project Structure

- `main.py`: The main entry point for running the Task Manager application.
- `task_manager_ui.py`: Contains the `TaskManagerUI` class that handles all the UI components and backend logic.
- `tasks.json`: A JSON file where task data is saved between sessions.
- `requirements.txt`: A file that lists all the Python packages required to run the project.
```
# f. Usage Instructions
## Usage

1. **Add a Task**: Fill out the task details such as Title, Description, Deadline, Priority, and Progress, then click "Add Task".
2. **Edit a Task**: Select a task from the list and click "Edit Task". Modify the details and click "Save Changes".
3. **Delete a Task**: Select a task and click "Delete Task" to remove it from the list.
4. **Filter by Priority**: Use the filter dropdown to filter tasks by Low, Medium, or High priority.
5. **Save Tasks**: Click "Save Tasks" to persist the current list of tasks to the `tasks.json` file.
6. **Load Tasks**: Click "Load Tasks" to load the tasks from the `tasks.json` file.

# g. Saving and Loading Task Data

## Saving and Loading Task Data

The application allows users to save their tasks to a `tasks.json` file, which can be reloaded when the application is reopened. This ensures that tasks persist across sessions.

- **Save Tasks**: Click the "Save Tasks" button to save the current tasks to `tasks.json`.
- **Load Tasks**: Click the "Load Tasks" button to load tasks from `tasks.json`.

5. Managing Dependencies (requirements.txt)
Generate the requirements.txt file by running the following command in your virtual environment
pip freeze > requirements.txt
