
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
import json

class TaskManagerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("900x600")

        # Initialize the main frames
        self.setup_frames()

        # Initialize task list as an empty list for now (to be integrated with backend logic later)
        self.tasks = []
        self.selected_task_index = None  # Track selected task for editing

        # Setup UI components
        self.setup_task_creation_form()
        self.setup_task_list_display()
        self.setup_filter_sorting_section()

        # Load tasks from a file (if available)
        self.load_tasks_from_file()

    def setup_frames(self):
        # Top frame for task creation form
        self.task_form_frame = tk.Frame(self.root)
        self.task_form_frame.pack(fill=tk.X, padx=10, pady=10)

        # Middle frame for task list display
        self.task_list_frame = tk.Frame(self.root)
        self.task_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bottom frame for filtering and sorting
        self.filter_sort_frame = tk.Frame(self.root)
        self.filter_sort_frame.pack(fill=tk.X, padx=10, pady=10)

    def setup_task_creation_form(self):
        # Labels and input fields for task creation
        tk.Label(self.task_form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.task_form_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.task_form_frame, text="Description:").grid(row=0, column=2, padx=5, pady=5)
        self.description_entry = tk.Entry(self.task_form_frame)
        self.description_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.task_form_frame, text="Deadline:").grid(row=1, column=0, padx=5, pady=5)
        # Use DateEntry widget for deadline (date picker)
        self.deadline_entry = DateEntry(self.task_form_frame, width=12, background='darkblue',
                                        foreground='white', borderwidth=2)
        self.deadline_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.task_form_frame, text="Priority:").grid(row=1, column=2, padx=5, pady=5)
        self.priority_var = tk.StringVar()
        self.priority_menu = ttk.Combobox(self.task_form_frame, textvariable=self.priority_var)
        self.priority_menu['values'] = ['Low', 'Medium', 'High']
        self.priority_menu.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(self.task_form_frame, text="Project:").grid(row=2, column=0, padx=5, pady=5)
        self.project_entry = tk.Entry(self.task_form_frame)
        self.project_entry.grid(row=2, column=1, padx=5, pady=5)

        # Task Progress dropdown
        tk.Label(self.task_form_frame, text="Progress:").grid(row=2, column=2, padx=5, pady=5)
        self.progress_var = tk.StringVar()
        self.progress_menu = ttk.Combobox(self.task_form_frame, textvariable=self.progress_var)
        self.progress_menu['values'] = ['0%', '25%', '50%', '75%', '100%']
        self.progress_menu.grid(row=2, column=3, padx=5, pady=5)

        # Error label to display validation messages
        self.error_label = tk.Label(self.task_form_frame, text="", fg="red")
        self.error_label.grid(row=3, column=0, columnspan=4)

        # Buttons for adding, editing, deleting, saving, and loading tasks
        self.add_task_button = tk.Button(self.task_form_frame, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=2, column=4, padx=5, pady=5)

        self.edit_task_button = tk.Button(self.task_form_frame, text="Edit Task", state=tk.DISABLED,
                                          command=self.edit_task)
        self.edit_task_button.grid(row=2, column=5, padx=5, pady=5)

        self.delete_task_button = tk.Button(self.task_form_frame, text="Delete Task", state=tk.DISABLED,
                                            command=self.delete_task)
        self.delete_task_button.grid(row=2, column=6, padx=5, pady=5)

        # Add Save and Load buttons
        self.save_task_button = tk.Button(self.task_form_frame, text="Save Tasks", command=self.save_tasks_to_file)
        self.save_task_button.grid(row=2, column=7, padx=5, pady=5)

        self.load_task_button = tk.Button(self.task_form_frame, text="Load Tasks", command=self.load_tasks_from_file)
        self.load_task_button.grid(row=2, column=8, padx=5, pady=5)

    def setup_task_list_display(self):
        # Setup treeview for task list display with checkbox for completed tasks
        columns = ('Completed', 'Title', 'Project', 'Deadline', 'Priority', 'Progress')
        self.task_tree = ttk.Treeview(self.task_list_frame, columns=columns, show='headings')

        # Define column headings
        self.task_tree.heading('Completed', text='Completed')
        self.task_tree.heading('Title', text='Title')
        self.task_tree.heading('Project', text='Project')
        self.task_tree.heading('Deadline', text='Deadline')
        self.task_tree.heading('Priority', text='Priority')
        self.task_tree.heading('Progress', text='Progress')

        # Set column sizes
        self.task_tree.column('Completed', width=100, anchor=tk.CENTER)
        self.task_tree.column('Title', width=150)
        self.task_tree.column('Project', width=100)
        self.task_tree.column('Deadline', width=100)
        self.task_tree.column('Priority', width=100)
        self.task_tree.column('Progress', width=100)

        # Define tags for row coloring
        self.task_tree.tag_configure('completed', background='lightgreen')
        self.task_tree.tag_configure('high_priority', background='lightcoral')

        # Pack the treeview widget
        self.task_tree.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar for large task lists
        self.task_scrollbar = ttk.Scrollbar(self.task_list_frame, orient="vertical", command=self.task_tree.yview)
        self.task_tree.configure(yscroll=self.task_scrollbar.set)
        self.task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind selection event to load task for editing
        self.task_tree.bind('<<TreeviewSelect>>', self.load_task_for_editing)

    def setup_filter_sorting_section(self):
        # Filtering and sorting options
        tk.Label(self.filter_sort_frame, text="Filter by Priority:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_priority_var = tk.StringVar()
        self.filter_priority_menu = ttk.Combobox(self.filter_sort_frame, textvariable=self.filter_priority_var)
        self.filter_priority_menu['values'] = ['All', 'Low', 'Medium', 'High']
        self.filter_priority_menu.grid(row=0, column=1, padx=5, pady=5)

        # Bind the combobox selection event to the filter function
        self.filter_priority_menu.bind("<<ComboboxSelected>>", self.apply_priority_filter)

        self.sort_deadline_button = tk.Button(self.filter_sort_frame, text="Sort by Deadline", command=self.sort_by_deadline)
        self.sort_deadline_button.grid(row=0, column=2, padx=5, pady=5)

    def apply_priority_filter(self, event):
        # Clear the Treeview before adding filtered tasks
        self.task_tree.delete(*self.task_tree.get_children())

        selected_priority = self.filter_priority_var.get()

        if selected_priority == 'All':
            # Show all tasks
            filtered_tasks = self.tasks
        else:
            # Filter tasks based on selected priority
            filtered_tasks = [task for task in self.tasks if task[4] == selected_priority]

        # Add the filtered tasks to the Treeview
        for task in filtered_tasks:
            self.task_tree.insert('', 'end', values=task)

    def add_task(self):
        task_title = self.title_entry.get()
        task_description = self.description_entry.get()
        task_deadline = self.deadline_entry.get()
        task_priority = self.priority_var.get()
        task_project = self.project_entry.get()
        task_progress = self.progress_var.get()

        # Clear any previous error messages
        self.error_label.config(text="")

        if not task_title or not task_priority:
            self.error_label.config(text="Task title and priority are required")
            return

        # Automatically set completed status based on progress
        task_completed = "Yes" if task_progress == "100%" else "No"

        # Add task to the task list
        task = (task_completed, task_title, task_project, task_deadline, task_priority, task_progress)
        self.tasks.append(task)

        # Insert into the Treeview
        item_id = self.task_tree.insert('', 'end', values=task)

        # Apply tag for completed and high-priority tasks
        if task_completed == "Yes":
            self.task_tree.item(item_id, tags=('completed',))
        elif task_priority == "High":
            self.task_tree.item(item_id, tags=('high_priority',))

        # Clear input fields
        self.clear_task_form()

    def load_task_for_editing(self, event):
        # Get selected items from the Treeview
        selected_items = self.task_tree.selection()

        # If no item is selected, exit the function
        if not selected_items:
            return

        # Get the selected item
        selected_item = selected_items[0]
        selected_task = self.task_tree.item(selected_item, 'values')

        # Find the index of the selected task in the tasks list
        self.selected_task_index = self.task_tree.index(selected_item)

        # Load task details into the form
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, selected_task[1])

        self.project_entry.delete(0, tk.END)
        self.project_entry.insert(0, selected_task[2])

        self.deadline_entry.set_date(selected_task[3])  # Use set_date for DateEntry

        self.priority_var.set(selected_task[4])
        self.progress_var.set(selected_task[5])

        # Enable the "Edit Task" and "Delete Task" buttons
        self.edit_task_button.config(state=tk.NORMAL)
        self.delete_task_button.config(state=tk.NORMAL)


    def edit_task(self):
        if self.selected_task_index is not None:
            updated_title = self.title_entry.get()
            updated_description = self.description_entry.get()
            updated_deadline = self.deadline_entry.get()
            updated_priority = self.priority_var.get()
            updated_project = self.project_entry.get()
            updated_progress = self.progress_var.get()

            updated_completed = "Yes" if updated_progress == "100%" else "No"

            updated_task = (
            updated_completed, updated_title, updated_project, updated_deadline, updated_priority, updated_progress)
            self.tasks[self.selected_task_index] = updated_task
            selected_item = self.task_tree.selection()[0]
            self.task_tree.item(selected_item, values=updated_task)

            # Clear old tags and apply new ones
            self.task_tree.item(selected_item, tags=())  # Clear old tags
            if updated_completed == "Yes":
                self.task_tree.item(selected_item, tags=('completed',))
            elif updated_priority == "High":
                self.task_tree.item(selected_item, tags=('high_priority',))

            # Clear input fields
            self.clear_task_form()
            self.selected_task_index = None
            self.edit_task_button.config(state=tk.DISABLED)
            self.delete_task_button.config(state=tk.DISABLED)

    def delete_task(self):
        # Remove the selected task from the list and Treeview
        if self.selected_task_index is not None:
            del self.tasks[self.selected_task_index]
            selected_item = self.task_tree.selection()[0]
            self.task_tree.delete(selected_item)

            # Clear input fields and disable buttons
            self.clear_task_form()
            self.selected_task_index = None
            self.edit_task_button.config(state=tk.DISABLED)
            self.delete_task_button.config(state=tk.DISABLED)

    def clear_task_form(self):
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        # Set to today's date instead of clearing the DateEntry
        self.deadline_entry.set_date(datetime.date.today())
        self.priority_var.set('')
        self.project_entry.delete(0, tk.END)
        self.progress_var.set('')

    def sort_by_deadline(self):
        # Sort tasks by deadline
        self.tasks.sort(key=lambda task: task[3])  # Sort tasks by the 'Deadline' field (task[3])
        # Clear and repopulate the Treeview after sorting
        self.task_tree.delete(*self.task_tree.get_children())
        for task in self.tasks:
            self.task_tree.insert('', 'end', values=task)

    def save_tasks_to_file(self):
        # Save the tasks to a JSON file
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file)


    def load_tasks_from_file(self):
        # Clear the current tasks in memory and the Treeview
        self.tasks.clear()
        self.task_tree.delete(*self.task_tree.get_children())

        try:
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)

                for task in self.tasks:
                    item_id = self.task_tree.insert('', 'end', values=task)

                    # Apply tag for completed and high-priority tasks
                    if task[0] == "Yes":  # task[0] is the 'Completed' status
                        self.task_tree.item(item_id, tags=('completed',))
                    elif task[4] == "High":  # task[4] is the 'Priority'
                        self.task_tree.item(item_id, tags=('high_priority',))
        except FileNotFoundError:
            pass

    def on_closing(self):
        # Save tasks before closing the app
        self.save_tasks_to_file()
        self.root.destroy()


