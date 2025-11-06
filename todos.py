import json
import sys
import os

TODOS_FILE = 'todos.json'

def load_todos():
    if not os.path.exists(TODOS_FILE):
        return []
    try:
        with open(TODOS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def save_todos(todos):
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def get_next_id(todos):
    if not todos:
        return 1
    return max(todo["id"] for todo in todos) + 1

def add_task(task):
    todos = load_todos()
    new_id = get_next_id(todos)
    todos.append({'id': new_id, 'task': task, 'done': False})
    save_todos(todos)
    print(f'Added: [{new_id}] "{task}"')

def list_tasks():
    todos = load_todos()
    if not todos:
        print("No tasks found.")
        return
    for todo in todos:
        status = "x" if todo["done"] else " "
        print(f'{todo["id"]}. [{status}] {todo["task"]}')

def mark_done(task_id):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == task_id:
            todo["done"] = True
            save_todos(todos)
            print(f'Task {task_id} marked as done.')
            return
    print("Task not found.")

def delete_task(task_id):
    todos = load_todos()
    new_todos = [todo for todo in todos if todo["id"] != task_id]
    if len(todos) == len(new_todos):
        print("Task not found.")
    else:
        save_todos(new_todos)
        print(f'Task {task_id} deleted.')

def help_msg():
    print("Usage:")
    print("  python todo.py add <task>")
    print("  python todo.py list")
    print("  python todo.py done <id>")
    print("  python todo.py delete <id>")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        help_msg()
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif cmd == "list":
        list_tasks()
    elif cmd == "done" and len(sys.argv) == 3 and sys.argv[2].isdigit():
        mark_done(int(sys.argv[2]))
    elif cmd == "delete" and len(sys.argv) == 3 and sys.argv[2].isdigit():
        delete_task(int(sys.argv[2]))
    else:
        help_msg()
