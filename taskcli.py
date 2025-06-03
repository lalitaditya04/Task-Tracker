import os
import sys
import json
from datetime import datetime
from texttable import Texttable # For pretty table display in terminal

filename = "tasks.json" # Default filename to store task data

# Load data from file if it exists, else return empty task list
def load_file():
    if os.path.exists(filename):
        with open(filename,'r') as file:
            return json.load(file)
    else:
        return{"Tasks":[]}

# Save data to file
def save_file(data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Display task table, optionally filtered by status (sts)
def print_filetable(sts=None):
    file = load_file()
    tasks = file["Tasks"]
    flag = False
    if not tasks:
        print("Your task list is empty.")
        return
    
    table = Texttable()
    table.header(["ID", "Description", "Status", "createdAt", "updatedAt"])
    # Display all tasks
    if not sts:
        for task in tasks:
            table.add_row([task["id"], task["description"], task["status"], task["createdAt"], task["updatedAt"]])
        print(table.draw())
    else:
        # Display only tasks with matching status
        for task in tasks:
            if task["status"] == sts:
                table.add_row([task["id"], task["description"], task["status"], task["createdAt"], task["updatedAt"]])
                flag = True
        if not flag:
            # No tasks matched the status filter
            if sts=="to-do":
                print("No task in \"TO DO\"")
            elif sts=="in-progress":
                print("No task is \"in_progress\"")
            else:
                print("No task done yet")
        else:
            print(table.draw())

# Add a new task with a description
def add_task(desc):
    file = load_file()
    tasks = file["Tasks"]
    new_id = len(tasks) + 1

    task = {
        "id" : new_id,
        "description" : desc,
        "status" : "to-do",
        "createdAt" : datetime.now().strftime('%Y-%m-%d %H:%M'),
        "updatedAt" : None
    }

    tasks.append(task)
    save_file(file)
    print(f"Task added successfully ")
    print_filetable()

# Delete a task by ID and reassign IDs sequentially
def del_task(tsk_id=None):
    tsk_id=int(tsk_id)
    file = load_file()
    tasks = file["Tasks"]
    flag = False
    if not tasks:
        print("Your task list is empty.")
        return

    # Remove task with matching ID
    og_len = len(tasks)
    tasks = [task for task in tasks if task["id"] != tsk_id]
    flag = len(tasks) != og_len

    if  flag:
        # Reassign task IDs after deletion
        for idx, task in enumerate(tasks, start=1):
            task["id"]=idx

        file["Tasks"]=tasks
        save_file(file)
        print(f"Task ID:{tsk_id} deleted successfully")
    else:
        print(f"Task with ID: {tsk_id} not found")
        print("use \"list\" command to view task list")

# Update the description of a task by ID
def update_task(tsk_id=None, tsk_value=None):
    tsk_id=int(tsk_id)
    file = load_file()
    tasks = file["Tasks"]
    if not tasks:
        print("Your task list is empty.")
        return

    for task in tasks:
        if task["id"] == tsk_id:
            task["description"] = tsk_value
            task["updatedAt"] = datetime.now().strftime('%Y-%m-%d %H:%M')
            save_file(file)
            print(f"Task ID:{tsk_id} update successfully at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            return

    print(f"Task with ID: {tsk_id} not found")
    print("use \"list\" command to view task list")

# Update the status of a task to 'in-progress' or 'done'
def status_update(tsk_id=None,mrkflag=None):
    tsk_id = int(tsk_id)
    file = load_file()
    tasks = file["Tasks"]
    flag = False
    if not tasks:
        print("Your task list is empty.")
        return

    for task in tasks:
        if task["id"]==tsk_id:
            flag = True
            if  mrkflag == "done":
                task["status"]=mrkflag
                print(f"Task ID:{tsk_id} marked as done successfully")
            elif  mrkflag == "in-progress":
                task["status"]=mrkflag
                print(f"Task ID:{tsk_id} marked as in-progress successfully")
    save_file(file)
    if not flag:
        print(f"Task with ID: {tsk_id} not found")
        print("use \"list\" command to view task list")

# Show available commands
def print_help():
    print("""
        Available Commands:
            Note: Task description should be include "  "
            add "<task>" : add task
            update <task id> "<task>" : update existing task
            delete <task id> : deleting existing task
            mark-in-progress <task id> : to mark status of the task as in-progress
            mark-done <task id> : to mark the status of task as done
            list : lists all the tasks
            list done : lists the tasks which are done 
            list todo : lists the tasks which are to be done
            list in-progress : lists the tasks which are in progress
            """)

# Main function to handle command-line arguments and call appropriate functions
def main():
    if len(sys.argv) < 2:
        print("USAGE: python taskcli.py <commands>")
        print("Run \"python taskcli.py help\" to see  available commands")
        sys.exit(1)

    action = sys.argv[1]
    if action == "add" and len(sys.argv)==3:
        add_task(sys.argv[2])

    elif action == "update" and len(sys.argv)==4:
        update_task(sys.argv[2],sys.argv[3])

    elif action == "delete" and len(sys.argv)==3:
        del_task(sys.argv[2])

    elif action == "mark-in-progress" and len(sys.argv)==3:
        status_update(sys.argv[2],"in-progress")

    elif action == "mark-done"and len(sys.argv)==3:
        status_update(sys.argv[2],"done")


    elif action == "list":
        if len(sys.argv) == 3:
            if sys.argv[2] == "done":
                print_filetable("done")
            elif sys.argv[2] == "to-do":
                print_filetable("to-do")
            elif sys.argv[2] == "in-progress":
                print_filetable("in-progress")
            else:
                print("Unknown filter. Use: done, to-do, or in-progress")
        else:
            print_filetable()

    elif action == "help" and len(sys.argv)==2:
        print_help()
    else:
        print("Invalid command or missing arguments.")
        print("use \"help\" command to see available commands")


if __name__ == "__main__":
    main()