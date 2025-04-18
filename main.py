# add task
# Mark task as done
# Delete task
# View all tasks
# Persist data using json file
import json
import os


class Todo:
    def __init__(self, is_done=False, title="", tasks=None, priority=""):
        if tasks is None:
            tasks = []
        self.title = title
        self.is_done = is_done
        self.priority = priority
        self.file_name = "todo.json"
        self.tasks = self.load_file()

    def save_file(self):
        with open(self.file_name, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def load_file(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                return json.load(file)
        return []

    def add_task(self):
        while True:
            self.title = input(
                "Enter the title of your to_do_list or 'o' to go back to the main menu: ").strip().lower()

            if not self.title:
                print("title cannot be empty")

            if self.title == "o":
                print("Returning to main menu...")
                return

            if any(task["title"].lower() == self.title.lower() for task in self.tasks):
                print(f"{self.title} already existed")
                continue

            self.priority = input("is task a High, Medium or Low priority (H, M, L)").strip().upper()

            # if self.priority not in ["H", "M", "L"]:
            #     print("Enter H, M or L")
            #     continue
            if self.priority == "H":
                self.priority = "High"
            elif self.priority == "M":
                self.priority = "Medium"
            elif self.priority == "L":
                self.priority = "Low"
            else:
                print("Invalid input, Enter H, M or L")
                continue

            # if self.title.lower() != "O":
            self.tasks.append({
                "title": self.title,
                "priority": self.priority,
                "is_done": self.is_done,

            })
            break

        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_tasks = sorted(self.tasks, key=lambda task: priority_order.get(task.get("priority", "Low"), 4))

        print(f"{'N0:':<5} {'Title':<20} {'Priority':<10} {'Status':<10}")
        for i, task in enumerate(sorted_tasks, start=1):
            status = "✅" if task["is_done"] else "❌"
            print(f"{i:<5} {task['title'].capitalize():<20} {task.get('priority', 'Low'):<10} {status:<10}")
        self.save_file()

    # def priority_check(self):
    #     user = input("is task a High, Medium or Low priority (H, M, L)")

    def mark_task(self):
        find_list = input("Enter tasks you want to mark as done: ").strip().lower()
        found = False
        for task in self.tasks:
            if task["title"].lower() == find_list:
                task["is_done"] = True

                print(f"{find_list} is completed")
            # status = "Done" if task["is_done"] else "Not Done"
            #
            # print(f"{task['title']} - {status}")
            found = True
            self.save_file()
        if not found:
            print("Task not found")

    def delete_task(self):
        delete_task = input("Enter the task you wish to delete: ").strip().lower()
        for i, task in enumerate(self.tasks):
            if delete_task in task["title"]:
                del self.tasks[i]
                self.save_file()
                print(f"{delete_task} Removed")
                break
        else:
            print("Task not found")

    def view_task(self):
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_tasks = sorted(self.tasks, key=lambda task: priority_order.get(task.get("priority", "Low"), 4))

        print("------------- Todo List -------------")
        print()
        print(f"{'N0:':<5} {'Title':<20} {'Priority':<10} {'Status':<10}")
        print()
        for i, task in enumerate(sorted_tasks, start=1):
            status = "✅" if task["is_done"] else "❌"
            print(f"{i:<5} {task['title'].capitalize():<20} {task.get('priority', 'Low'):<10} {status:<10}")
        print()

    def percent_of_task_completed(self):
        total = len(self.tasks)
        if total == 0:
            print("No tasks yet.")
            return
        completed = sum(1 for task in self.tasks if task["is_done"])
        percentage = (completed / total) * 100
        print(f"{completed} out of {total} tasks completed ({percentage:.2f}%)")

    def edit_task(self):
        edit_input = input("enter the name of the task you want to edit: ").strip().lower()
        found = False
        for task in self.tasks:
            if task["title"] == edit_input:
                replace_task = input("enter a replacement: ")
                priority_input = input("is task a High, Medium or Low priority (H, M, L)").strip().upper()
                priority_map = {"H": "High", "M": "Medium", "L": "Low"}
                if priority_input not in priority_map:
                    print("Invalid priority (H, L, M)")
                self.priority = priority_map[priority_input]

                task['title'] = replace_task
                task['priority'] = self.priority
                task['is_done'] = False
                print(f"{task['title']} successfully updated \n")
                self.save_file()
                found = True
        if not found:
            print(f"{edit_input} not in tasks")


class Run(Todo):
    def run_todo(self):
        try:
            while True:
                print("---- Todo List ----")
                print("1. Add Task")
                print("2. Mark Task as Done ")
                print("3. Delete Task")
                print("4. View all tasks")
                print("5. Show percentage of task completed")
                print("6. Edit task")
                print("7. Exit")

                choice = input("Choose an option: ").strip()

                if choice == "1":
                    self.add_task()
                elif choice == "2":
                    self.mark_task()
                elif choice == "3":
                    self.delete_task()
                elif choice == "4":
                    self.view_task()
                elif choice == "5":
                    self.percent_of_task_completed()
                elif choice == "6":
                    self.edit_task()
                elif choice == "7":
                    print("Exiting... Goodbye!")
                    break
                else:
                    print("Invalid choice. Try again.\n")
        except KeyboardInterrupt:
            print(" Todo List safely Ended")


run = Run()
run.run_todo()
