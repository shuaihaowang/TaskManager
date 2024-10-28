import tkinter as tk
from task_manager_ui import TaskManagerUI

# Entry point of the application

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Handle saving tasks on close
    root.mainloop()
