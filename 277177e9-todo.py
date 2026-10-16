
import json
import os

DATA_FILE = "tasks.json"


# ---------------------------------------------------------------
# MODEL (data logic) - knows nothing about print() or input()
# ---------------------------------------------------------------
def load_tasks():
    """Read tasks from disk so data survives after the program closes."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Write the list to disk (RAM is volatile, files are not)."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def add_task(tasks, text):
    """Append a new task. Each task is a dictionary, like a table row."""
    next_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": next_id, "task": text, "done": False})
    return next_id


def mark_done(tasks, task_id):
    """Mark a task as completed. Returns True if the id was found."""
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            return True
    return False


def delete_task(tasks, task_id):
    """Remove a task by its id. Returns True if the id was found."""
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(i)
            return True
    return False


# ---------------------------------------------------------------
# VIEW (user interface) - only deals with input() and print()
# ---------------------------------------------------------------
def view_tasks(tasks):
    """Display every task using a print loop with enumerate()."""
    print("\n" + "=" * 40)
    print("           YOUR TO-DO LIST")
    print("=" * 40)
    if not tasks:
        print("  No tasks yet. Add one from the menu!")
    else:
        for number, t in enumerate(tasks, start=1):
            status = "[x]" if t["done"] else "[ ]"
            print(f"  {number}. {status} {t['task']}  (ID: {t['id']})")
    pending = sum(1 for t in tasks if not t["done"])
    print("-" * 40)
    print(f"  Total: {len(tasks)} | Pending: {pending} | Done: {len(tasks) - pending}")
    print("=" * 40)


def show_menu():
    print("\n--- MENU ---")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Mark a task as done")
    print("4. Delete a task")
    print("5. Exit")


def ask_for_id(message):
    """Ask for a task ID and make sure the user typed a number."""
    value = input(message).strip()
    if value.isdigit():
        return int(value)
    print("Please enter a valid number.")
    return None


def main():
    tasks = load_tasks()
    print("Welcome to the To-Do List Manager!")

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            text = input("Enter your task: ").strip()
            if text:
                add_task(tasks, text)
                save_tasks(tasks)
                print(f'Task added: "{text}"')
            else:
                print("Task cannot be empty.")

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            view_tasks(tasks)
            task_id = ask_for_id("Enter the ID of the task you finished: ")
            if task_id is not None:
                if mark_done(tasks, task_id):
                    save_tasks(tasks)
                    print("Nice work! Task marked as done.")
                else:
                    print("No task found with that ID.")

        elif choice == "4":
            view_tasks(tasks)
            task_id = ask_for_id("Enter the ID of the task to delete: ")
            if task_id is not None:
                if delete_task(tasks, task_id):
                    save_tasks(tasks)
                    print("Task deleted.")
                else:
                    print("No task found with that ID.")

        elif choice == "5":
            print("Goodbye! Your tasks have been saved.")
            break

        else:
            print("Invalid choice. Please pick a number from 1 to 5.")


if __name__ == "__main__":
    main()
