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
        #return str(num) + ". " + f"[{self.label}][{self.get_status_icon()}] {self.description}"
        return ("ToDo", str(num), self.label, self.get_status_icon(), self.description)
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
        #self.deadline = dt.datetime(day=int(deadline[:2]), month=int(deadline[3:5]), year=int(deadline[6:10]), 
        #hour = int(deadline[11:13]), minute=int(deadline[14:16]))
        self.deadline = dt.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
        self.label = 'D'
    def showTask(self, num):
        """Prints out the task description and whether it is done"""
        #return str(num) + ". "+ f"[{self.label}][{self.get_status_icon()}] {self.description} (by: {self.deadline.strftime('%A %d/%m/%Y %H:%M')})"
        return ("Deadline", str(num), self.label, self.get_status_icon(), self.description, f"(by: {self.deadline.strftime('%A %d/%m/%Y %H:%M')})")
    def get_deadline(self):
        return self.deadline


class Event(Task):
    def __init__(self, description, start, end) -> None:
        """datetime must be in the format `yyyy-mm-dd hh:mm:ss`"""
        super().__init__(description)
        self.start = dt.datetime.strptime(start, '%d/%m/%Y %H:%M')
        self.end = dt.datetime.strptime(end, '%d/%m/%Y %H:%M')
        self.label = 'E'
    def showTask(self, num):
        """Prints out the task description and whether it is done"""
        #return (str(num) + ". " + f"[{self.label}][{self.get_status_icon()}] {self.description} (at: {self.datetime})")
        return ("Event", str(num), self.label, self.get_status_icon(), self.description, f"start: {self.start.strftime('%A %d/%m/%Y %H:%M')}", f"end: {self.end.strftime('%A %d/%m/%Y %H:%M')}")
    def get_datetime(self):
        return self.datetime

    
