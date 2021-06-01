import datetime as dt
"""Task module containg the different task classes"""
class Task:
    def __init__(self, description) -> None:
        self.description = description
        self.isDone = False
        self.label = 'T'
    def get_status_icon(self):
        """Returns a tick if task is done and cross otherwise"""
        return "\u2713" if self.isDone else "\u2718"
    def showTask(self, num):
        """Prints out the task description and whether it is done"""
        print(str(num), f"[{self.label}][{self.get_status_icon()}] {self.description}")
    def markDone(self):
        """Marks the task as done"""
        self.isDone = True
    def done(self):
        """Returns whether the task is done"""
        return self.isDone
    def get_description(self):
        """Returns the description of the task"""
        return self.description

class ToDo(Task):
    def __init__(self, description) -> None:
        super().__init__(description)

class Deadline(Task):
    def __init__(self, description, deadline) -> None:
        super().__init__(description)
        self.deadline = deadline
        self.label = 'D'
    def showTask(self, num):
        """Prints out the task description and whether it is done"""
        print(str(num), f"[{self.label}][{self.get_status_icon()}] {self.description} (by: {self.deadline})")
    def get_deadline(self):
        return self.deadline


class Event(Task):
    def __init__(self, description, datetime) -> None:
        super().__init__(description)
        self.datetime = datetime
        self.label = 'E'
    def showTask(self, num):
        """Prints out the task description and whether it is done"""
        print(str(num), f"[{self.label}][{self.get_status_icon()}] {self.description} (at: {self.datetime})")
    def get_datetime(self):
        return self.datetime

    
