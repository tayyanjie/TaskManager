import tasks_flask as tasks
import re
from os import listdir
import pickle

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
                self.commands = f.readlines()
        else:
            raise Exception("commands.txt not found in directory.")

        # Checks for an existing data file and loads it if present
        if 'data.p' in listdir():
            with open('data.p', 'rb') as f:
                self.task_list = pickle.load(f)
            
        
    def save(self):
        """Saves the tasks added into a .txt file"""
        self.saved = True
        with open('data.p', 'wb') as fp:
            pickle.dump(self.task_list, fp, protocol=pickle.HIGHEST_PROTOCOL)
        
    def get_commands(self):
        return self.commands

    def welcome(self):
        """Prints out initial welcome message when the app is launched"""
        return "Hi, what can I do for you today?"

    def getCommand(self):
        """Obtains user command input"""
        return input("")
    
    def help(self):
        """Prints a list of commands available"""
        return self.commands
        
    def list_todos(self):
        """List out all the tasks that have been added into the app"""
        res = {}
        has_task = False
        for task_type in self.task_list:
            if self.task_list[task_type]:
                has_task = True
            res[task_type] = []
        if not has_task:
            return res

        for task_type in self.task_list:
            counter = 1
            for task in self.task_list[task_type]:
                res[task_type].append(task.showTask(counter))
                counter += 1
        return res


    def add(self, description, type = "Task", deadline=None):
        """Adds a task with description"""
        if type not in ['Task', 'ToDo', 'Deadline', 'Event']:
            return 'Invalid task type added.'
        
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
            try:
                self.task_list['Deadline'].append(tasks.Deadline(description, deadline))
                self.saved = False
            except:
                return "Invalid format added"
            
        # Check for Event
        elif type == "Event" and deadline != None:
            try:
                self.task_list['Event'].append(tasks.Event(description, deadline))
                self.saved = False
            except:
                return "Invalid format added"
        else:
            return "Invalid task added."
        res = ""
        res += f"added {type} {description}" + "\n"
        #res += f"Total number of tasks in list: {self.total_tasks} \n" 
        #res += f"Number of tasks completed: {self.num_done}"
        return res
        
    
    def done(self, ind, task_type):
        """Marks the task at a particular index as done"""
        if not self.task_list[task_type] or ind > len(self.task_list[task_type]):
            return ("There is no such task.")
        task_list = self.task_list[task_type]
        if not task_list[ind-1].done():
            task_list[ind-1].markDone()
            description = task_list[ind-1].get_description()
            label = task_list[ind-1].label
            
            self.num_done += 1
            self.saved = False
            return f"The task [{label}] {description} has been marked done"
        else:
            return ("The task has already been marked done.")
        

    def delete(self, ind, task_type):
        """Deletes the task at a particular index"""
        if ind > len(self.task_list[task_type]):
            return "Task index does not exist."
        res = "The following task has been deleted: "
        task = self.task_list[task_type][ind-1]
        description = task.get_description()
        label = task.label
        res += f"[{label}] {description}"
        self.saved = False

        # removes task from task list
        self.task_list[task_type].pop(ind-1)
        if task.done:
            self.num_done -= 1
        self.total_tasks -= 1
        #res += f"\nTotal number of tasks in list: {self.total_tasks}"
        #res += f"\nNumber of tasks completed: {self.num_done}"
        return res
    
    def delete_all(self, task_type):
        for type in self.task_list:
            self.task_list[type] = []
        return f"Deleted {task_type} tasks."
    
    def get_summary(self):
        """Prints out summary statistics regarding current stored taskes"""
        return f"Total number of tasks in list: {self.total_tasks}\nNumber of tasks completed: {self.num_done}"
        
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
 