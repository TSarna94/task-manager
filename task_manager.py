# ============================================================
#  PYTHON TASK MANAGER 
#  Developed by Tony Sarna
#
#  Academic Integrity Note:
#  This program was written by me (Tony) as part of my Python
#  learning. AI assistance was used only for debugging,
#  readability improvements, and learning support. All logic
#  and implementation decisions are my own.
# ============================================================

import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


# ============================================================
#  REGISTER USER
# ============================================================
def reg_user(username_password):
    """
    Register a new user and save to user.txt.
    Prevents duplicate usernames.
    """
    print("\n===== REGISTER USER =====\n")

    while True:
        new_username = input("New Username: ")

        if new_username in username_password:
            print("Username already exists. Please choose another.")
            continue
        break

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        username_password[new_username] = new_password

        with open("user.txt", "w", encoding="utf-8") as out_file:
            user_data = [f"{u};{p}" for u, p in username_password.items()]
            out_file.write("\n".join(user_data))

        print("New user added.")
    else:
        print("Passwords do not match.")


# ============================================================
#  ADD TASK
# ============================================================
def add_task(username_password, task_list):
    """
    Add a new task and save to tasks.txt.
    """
    print("\n===== ADD TASK =====\n")

    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password:
        print("User does not exist.")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid date format.")

    current_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": current_date,
        "completed": False
    }

    task_list.append(new_task)
    save_tasks(task_list)
    print("Task successfully added.")


# ============================================================
#  VIEW ALL TASKS
# ============================================================
def view_all(task_list):
    """
    Display all tasks in the system.
    """
    print("\n===== ALL TASKS =====\n")

    if not task_list:
        print("No tasks available.\n")
        return

    for task in task_list:
        print("-" * 30)
        print(f"Title:          {task['title']}")
        print(f"Assigned to:    {task['username']}")
        print(f"Date Assigned:  {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date:       {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Completed:      {'Yes' if task['completed'] else 'No'}")
        print(f"Description:\n{task['description']}\n")


# ============================================================
#  VIEW MY TASKS
# ============================================================
def view_mine(task_list, current_user):
    """
    Display tasks assigned to the logged-in user.
    Allows selecting a task for editing or completion.
    """
    print("\n===== YOUR TASKS =====\n")

    user_tasks = [t for t in task_list if t['username'] == current_user]

    if not user_tasks:
        print("You have no tasks assigned.\n")
        return

    for index, task in enumerate(user_tasks, start=1):
        print(f"Task #{index}")
        print("-" * 30)
        print(f"Title:          {task['title']}")
        print(f"Assigned to:    {task['username']}")
        print(f"Date Assigned:  {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date:       {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Completed:      {'Yes' if task['completed'] else 'No'}")
        print(f"Description:\n{task['description']}\n")

    while True:
        choice = input("Enter a task number to select it, or -1 to return: ")

        if choice == "-1":
            return

        if not choice.isdigit():
            print("Invalid input.")
            continue

        choice = int(choice)

        if 1 <= choice <= len(user_tasks):
            return user_tasks[choice - 1]

        print("Invalid task number.")


# ============================================================
#  VIEW COMPLETED TASKS
# ============================================================
def view_completed(task_list):
    """
    Display all completed tasks.
    """
    print("\n===== COMPLETED TASKS =====\n")

    completed = [t for t in task_list if t['completed']]

    if not completed:
        print("No completed tasks.\n")
        return

    for task in completed:
        print(f"{task['title']}")
        print(f"Assigned to:    {task['username']}")
        print(f"Date Assigned:  {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date:       {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Description:\n{task['description']}\n")


# ============================================================
#  VIEW OVERDUE TASKS
# ============================================================
def view_overdue(task_list):
    """
    Display all overdue tasks.
    """
    print("\n===== OVERDUE TASKS =====\n")

    overdue = [
        t for t in task_list
        if not t['completed'] and t['due_date'] < datetime.now()
    ]

    if not overdue:
        print("No overdue tasks.\n")
        return

    for task in overdue:
        print(f"OVERDUE: {task['title']}")
        print(f"Assigned to:    {task['username']}")
        print(f"Date Assigned:  {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date:       {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Description:\n{task['description']}\n")


# ============================================================
#  SORT TASKS
# ============================================================
def sort_tasks(task_list):
    """
    Sort tasks by due date, username, or completion status.
    """
    print("\n===== SORT TASKS =====\n")

    print("1 - Sort by due date")
    print("2 - Sort by assigned user")
    print("3 - Sort by completion status")
    print("4 - Return")

    choice = input("Choose an option: ")

    if choice == "1":
        task_list.sort(key=lambda t: t['due_date'])
        print("Tasks sorted by due date.")

    elif choice == "2":
        task_list.sort(key=lambda t: t['username'].lower())
        print("Tasks sorted by assigned user.")

    elif choice == "3":
        task_list.sort(key=lambda t: t['completed'])
        print("Tasks sorted by completion status.")

    elif choice == "4":
        return

    else:
        print("Invalid choice.")

    input("\nPress Enter to continue...")


# ============================================================
#  SAVE TASKS
# ============================================================
def save_tasks(task_list):
    """
    Save all tasks to tasks.txt.
    """
    with open("tasks.txt", "w", encoding="utf-8") as task_file:
        lines = []
        for task in task_list:
            line = ";".join([
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task['completed'] else "No"
            ])
            lines.append(line)
        task_file.write("\n".join(lines))


# ============================================================
#  TASK ACTIONS
# ============================================================
def task_actions(task, task_list, username_password):
    """
    Allow user to mark a task complete or edit it.
    """
    while True:
        print("\n===== TASK ACTIONS =====\n")
        print("1 - Mark task as complete")
        print("2 - Edit task")
        print("3 - Return")

        choice = input("Choose an option: ")

        if choice == "1":
            task['completed'] = True
            save_tasks(task_list)
            print("Task marked as complete.")
            input("\nPress Enter to continue...")
            return

        elif choice == "2":
            edit_task(task, task_list, username_password)
            return

        elif choice == "3":
            return

        else:
            print("Invalid choice.")
            input("\nPress Enter to continue...")


# ============================================================
#  EDIT TASK
# ============================================================
def edit_task(task, task_list, username_password):
    """
    Edit task fields unless the task is completed.
    """
    if task['completed']:
        print("You cannot edit a completed task.")
        input("\nPress Enter to continue...")
        return

    print("\n===== EDIT TASK =====\n")
    print("1 - Change assigned user")
    print("2 - Change due date")
    print("3 - Change title")
    print("4 - Change description")
    print("5 - Return")

    choice = input("Choose an option: ")

    if choice == "1":
        new_user = input("Enter new username: ")
        if new_user in username_password:
            task['username'] = new_user
        else:
            print("User does not exist.")

    elif choice == "2":
        new_date = input("Enter new due date (YYYY-MM-DD): ")
        try:
            task['due_date'] = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
        except ValueError:
            print("Invalid date format.")

    elif choice == "3":
        task['title'] = input("Enter new title: ")

    elif choice == "4":
        task['description'] = input("Enter new description: ")

    elif choice == "5":
        return

    else:
        print("Invalid choice.")
        return

    save_tasks(task_list)
    print("Task updated successfully.")
    input("\nPress Enter to continue...")


# ============================================================
#  GENERATE REPORTS
# ============================================================
def generate_reports(task_list, username_password):
    """
    Generate task_overview.txt and user_overview.txt
    containing required statistics.
    """

    # -------------------------
    # TASK OVERVIEW
    # -------------------------
    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t['completed'])
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < datetime.now())

    percent_incomplete = (incomplete_tasks / total_tasks * 100) if total_tasks > 0 else 0
    percent_overdue = (overdue_tasks / total_tasks * 100) if total_tasks > 0 else 0

    with open("task_overview.txt", "w", encoding="utf-8") as f:
        f.write(f"Total tasks: {total_tasks}\n")
        f.write(f"Completed tasks: {completed_tasks}\n")
        f.write(f"Incomplete tasks: {incomplete_tasks}\n")
        f.write(f"Overdue tasks: {overdue_tasks}\n")
        f.write(f"Percentage incomplete: {percent_incomplete:.2f}%\n")
        f.write(f"Percentage overdue: {percent_overdue:.2f}%\n")

    # -------------------------
    # USER OVERVIEW
    # -------------------------
    with open("user_overview.txt", "w", encoding="utf-8") as f:
        f.write(f"Total users: {len(username_password)}\n")
        f.write(f"Total tasks: {total_tasks}\n\n")

        for user in username_password:
            user_tasks = [t for t in task_list if t['username'] == user]
            user_total = len(user_tasks)

            if total_tasks > 0:
                percent_assigned = (user_total / total_tasks * 100)
            else:
                percent_assigned = 0

            user_completed = sum(1 for t in user_tasks if t['completed'])
            user_incomplete = user_total - user_completed
            user_overdue = sum(1 for t in user_tasks if not t['completed'] and t['due_date'] < datetime.now())

            percent_user_completed = (user_completed / user_total * 100) if user_total > 0 else 0
            percent_user_incomplete = (user_incomplete / user_total * 100) if user_total > 0 else 0
            percent_user_overdue = (user_overdue / user_total * 100) if user_total > 0 else 0

            f.write(f"User: {user}\n")
            f.write(f"Total tasks assigned: {user_total}\n")
            f.write(f"Percentage of all tasks: {percent_assigned:.2f}%\n")
            f.write(f"Percentage completed: {percent_user_completed:.2f}%\n")
            f.write(f"Percentage incomplete: {percent_user_incomplete:.2f}%\n")
            f.write(f"Percentage overdue: {percent_user_overdue:.2f}%\n\n")

    print("Reports generated successfully.")


# ============================================================
#  DISPLAY STATISTICS
# ============================================================
def display_statistics(task_list, username_password):
    """
    Display statistics from task_overview.txt and user_overview.txt.
    If files do not exist, generate them first.
    """

    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports(task_list, username_password)

    print("\n===== STATISTICS =====\n")

    print("----- Task Overview -----")
    with open("task_overview.txt", "r", encoding="utf-8") as f:
        print(f.read())

    print("----- User Overview -----")
    with open("user_overview.txt", "r", encoding="utf-8") as f:
        print(f.read())


# ============================================================
#  FILE LOADING
# ============================================================

if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding="utf-8") as default_file:
        pass

with open("tasks.txt", "r", encoding="utf-8") as task_file:
    task_data = [line for line in task_file.read().split("\n") if line.strip()]

task_list = []
for task in task_data:
    parts = task.split(";")
    task_list.append({
        "username": parts[0],
        "title": parts[1],
        "description": parts[2],
        "due_date": datetime.strptime(parts[3], DATETIME_STRING_FORMAT),
        "assigned_date": datetime.strptime(parts[4], DATETIME_STRING_FORMAT),
        "completed": parts[5] == "Yes"
    })

if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding="utf-8") as default_file:
        default_file.write("admin;password")

with open("user.txt", "r", encoding="utf-8") as user_file:
    user_data = [line for line in user_file.read().split("\n") if line.strip()]

username_password = {}
for user in user_data:
    username, password = user.split(";")
    username_password[username] = password


# ============================================================
#  LOGIN
# ============================================================
while True:
    print("\n===== LOGIN =====\n")

    current_user = input("Username: ")
    current_pass = input("Password: ")

    if current_user not in username_password:
        print("User does not exist.")
        input("\nPress Enter to continue...")
        continue

    if username_password[current_user] != current_pass:
        print("Wrong password.")
        input("\nPress Enter to continue...")
        continue

    print("Login Successful!")
    break


# ============================================================
#  MAIN MENU
# ============================================================
while True:
    print("\n===== MAIN MENU =====\n")
    menu = input(
        "Select one of the following options:\n"
        " r  - Register a user\n"
        " a  - Add a task\n"
        " va - View all tasks\n"
        " vm - View my tasks\n"
        " vc - View completed tasks\n"
        " vo - View overdue tasks\n"
        " gr - Generate reports\n"
        " ds - Display statistics\n"
        " s  - Sort tasks\n"
        " e  - Exit\n"
        ": "
    ).lower()

    if menu == "r":
        reg_user(username_password)

    elif menu == "a":
        add_task(username_password, task_list)

    elif menu == "va":
        view_all(task_list)

    elif menu == "vm":
        selected_task = view_mine(task_list, current_user)
        if selected_task:
            task_actions(selected_task, task_list, username_password)

    elif menu == "vc":
        view_completed(task_list)

    elif menu == "vo":
        view_overdue(task_list)

    elif menu == "gr":
        generate_reports(task_list, username_password)

    elif menu == "ds":
        display_statistics(task_list, username_password)

    elif menu == "s":
        sort_tasks(task_list)

    elif menu == "e":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")
        input("\nPress Enter to continue...")
