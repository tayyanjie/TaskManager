import tasks
import re
from os import listdir

class UI:
    def __init__(self) -> None:
        self.task_list = {'ToDo':[], 'Deadline':[], 'Event':[]}
        self.num_done = 0
        self.total_tasks = 0
        self.commands = ""
        self.saved = True

        # Check commands.txt is in directory and prints out all available commands on startup
        if 'commands.txt' in listdir():
            with open('commands.txt') as f:
                lines = f.readlines()
            for line in lines:
                self.commands += line
        else:
            raise Exception("commands.txt not found in directory.")
        print(self.commands)

        # Checks for an existing data file and loads it if present
        if 'task.txt' in listdir():
            with open('task.txt') as f:
                contents = f.readlines()
            for task in contents:
                task = task.split(', ')
                description = re.sub("\n","", task[2])
                done = bool(int(task[1]))
                self.num_done = self.num_done + 1 if done else self.num_done
                self.total_tasks += 1
                if task[0] == 'T':
                    t = tasks.ToDo(description)
                    t.isDone = True if done == 1 else False
                    self.task_list['ToDo'].append(t)
                elif task[0] == 'D':
                    d = tasks.Deadline(description, re.sub("\n","", task[3]))
                    d.isDone = True if done == 1 else False
                    self.task_list['Deadline'].append(d)
                else:
                    e = tasks.Event(description, re.sub("\n","", task[3]))
                    e.isDone = True if done == 1 else False
                    self.task_list['Event'].append(e)
            print("Saved file loaded.")
            self.get_summary()
            print(25*'-')
        
    def save(self):
        """Saves the tasks added into a .txt file"""
        self.saved = True
        lst = []
        for task_type in self.task_list.keys():
            for task in self.task_list[task_type]:
                done = 1 if task.done() else 0
                if isinstance(task, tasks.ToDo):
                    lst.append('\nT, '+str(done) + ', ' + task.get_description())
                elif isinstance(task, tasks.Deadline):
                    lst.append('\nD, ' + str(done) + ', ' + task.get_description() + ', ' + task.get_deadline())
                else:
                    lst.append('\nE, ' + str(done) + ', ' + task.get_description() + ', ' + task.get_datetime())
        
        # removes the \n character for the first entry so that first line would not be empty
        if len(lst) > 0:
            lst[0] = lst[0][1:]

        # Overwrites the original txt file with the current data if task.txt is present
        if 'task.txt' in listdir():
            f = open('task.txt', 'w')
            f.writelines(lst)
        # Otherwise create a new txt file and save the data in that file
        else:
            f = open('task.txt', 'x')
            f.writelines(lst)
        

    def welcome(self):
        """Prints out initial welcome message when the app is launched"""
        print("Hi, what can I do for you today?")

    def getCommand(self):
        """Obtains user command input"""
        return input("")
    
    def help(self):
        """Prints a list of commands available"""
        print(self.commands)
        
    def list_todos(self):
        """List out all the tasks that have been added into the app"""
        for task_type in self.task_list:
            if self.task_list[task_type]:
                break
            print("No tasks added yet, please add a task!")
            return

        for task_type in self.task_list:
            counter = 1
            if not self.task_list[task_type]:
                print(f"There is no tasks that are of type {task_type}")
            else:
                print(task_type)
            for task in self.task_list[task_type]:
                task.showTask(counter)
                counter += 1
            print(25*'-')


    def add(self, description, type = "Task", deadline=None):
        """Adds a task with description"""
        if type not in ['Task', 'ToDo', 'Deadline', 'Event']:
            print('Invalid task type added.')
            return
        
        # Check for Task
        elif type == "Task":
            self.task_list['ToDo'].append(tasks.Task(description))
            self.saved = False

        # Check for ToDo
        elif type == "ToDo":
            self.task_list['ToDo'].append(tasks.ToDo(description))
            self.saved = False

        # Check for Deadline
        elif type == "Deadline" and deadline != None:
            self.task_list['Deadline'].append(tasks.Deadline(description, deadline))
            self.saved = False
        
        # Check for Event
        elif type == "Event" and deadline != None:
            self.task_list['Event'].append(tasks.Event(description, deadline))
            self.saved = False
        else:
            print("Invalid task added.")
            return
        print(f"added {type} {description}")
        print(f"Total number of tasks in list: {self.total_tasks}")
        print(f"Number of tasks completed: {self.num_done}")
        
    
    def done(self, ind, task_type):
        """Marks the task at a particular index as done"""
        if not self.task_list[task_type] or ind > len(self.task_list[task_type]):
            print("There is no such task.")
            return
        task_list = self.task_list[task_type]
        if not task_list[ind-1].done():
            task_list[ind-1].markDone()
            print("The following task has been marked done:")
            description = task_list[ind-1].get_description()
            done = task_list[ind-1].get_status_icon()
            print(f"[{done}] {description}")
            self.num_done += 1
            self.saved = False
        else:
            print("The task has already been marked done.")
        

    def delete(self, ind, task_type):
        """Deletes the task at a particular index"""
        if ind > len(self.task_list[task_type]):
            print("Task index does not exist.")
            return
        print("The following task has been deleted:")
        task = self.task_list[task_type][ind-1]
        description = task.get_description()
        done = task.get_status_icon()
        print(f"[{done}] {description}")
        self.saved = False

        # removes task from task list
        self.task_list[task_type].pop(ind-1)
        if task.done:
            self.num_done -= 1
        self.total_tasks -= 1
        print(f"Total number of tasks in list: {self.total_tasks}")
        print(f"Number of tasks completed: {self.num_done}")
    
    def get_summary(self):
        """Prints out summary statistics regarding current stored taskes"""
        print(f"Total number of tasks in list: {self.total_tasks}")
        print(f"Number of tasks completed: {self.num_done}")
        
    def parseCommand(self, command):
        """Reads in user's command to do appropriate action"""
        if command == "list":
            self.list_todos()

        # Checks for add command
        elif re.search("^(add) ", command) != None:
            self.add(command[4:])
        
        # Checks for done command
        elif re.search("^(done) ", command) != None:
            task_type = command[5]
            ind = int(command[7:])
            if task_type == 'T':
                task_type = "ToDo"
            elif task_type == 'D':
                task_type = "Deadline"
            elif task_type == "E":
                task_type = "Event"
            else:
                print("Invalid task type entered")
                return True
            self.done(ind, task_type)
        
        # Checks for delete command
        elif re.search("^(delete) ", command) != None:
            task_type = command[7]
            ind = int(command[9:])
            if task_type == 'T':
                task_type = "ToDo"
            elif task_type == 'D':
                task_type = "Deadline"
            elif task_type == "E":
                task_type = "Event"
            else:
                print("Invalide task type entered")
                return True
            self.delete(ind, task_type)
        
        # Checks for adding of ToDo task type
        elif re.search("^(todo) ", command) != None:
            self.add(command[5:], type="ToDo")
        
        # Checks for adding of Deadline task type
        elif re.search("^(deadline) ", command) != None:
            descriptions = re.findall("(?<=deadline).*(?=/by)", command)
            deadlines = re.findall("(?<=/by) .*", command)
            if len(descriptions) == 0 or len(deadlines) == 0:
                print("Command invalid, please type a valid command.")
            else:
                description = descriptions[0].strip()
                deadline = deadlines[0].strip()
                self.add(description, type="Deadline", deadline=deadline)
        
        # Checks for adding of Event task type
        elif re.search("^(event) ", command) != None:
            descriptions = re.findall("(?<=event).*(?=/at)", command)
            deadlines = re.findall("(?<=/at) .*", command)
            if len(descriptions) == 0 or len(deadlines) == 0:
                print("Command invalid, please type a valid command.")
            else:
                description = descriptions[0].strip()
                deadline = deadlines[0].strip()
                self.add(description, type="Event", deadline=deadline)
        
        elif command == 'save':
            self.save()
            print("Saved file.")
        
        elif command == 'help':
            self.help()
        
        elif command == 'exit':
            if self.saved:
                return False
            else:
                confirm = input("File has not yet been saved, are you sure you want to exit? [y/n]: ")
                if confirm == 'y':
                    print("File not saved, exiting...")
                    return False
                print("'y' is not entered, please give another command: ")

        else:
            print("Command invalid, please type a valid command.")
        
        return True
 