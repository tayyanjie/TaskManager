# Task Manager <!-- omit in toc -->
This repository contains the code for a simple Python Task Manager used to keep track of tasks. 

The idea of the task manager is referenced from [CS2103's Project Duke](https://nus-cs2103-ay2021s1.github.io/website/se-book-adapted/projectDuke/).

## Table of Contents <!-- omit in toc -->
- [Running the Task Manager](#running-the-task-manager)
- [Saving Data](#saving-data)
- [Task Types](#task-types)
- [Basic Commands:](#basic-commands)

## Running the Task Manager
To run the program, run the `run.py` file.

## Saving Data
The tasks added while using the program can be saved in a txt file (`task.txt`) which is loaded when Task Manager upon running `run.py`.

An initial filled sample `task.txt` is provided in the repository.

## Task Types
There are 3 basic task types:
1. `ToDo` - Similar to `Task`.
2. `Deadline` - Similar to `Task` but with a `datetime` as a deadline.
3. `Event` - Similar to `Task` but with a specific start and end `datetime`.

## Basic Commands:
The `commands.txt` file contains the list of commands which is needed for the startup of the Task Manager. **Do not delete the file and ensure that the `commands.txt` file remains in the directory**.
1. `todo <task>` - Adds a `ToDo` task with <task> as a description.
2. `deadline <task> /by <deadline>` - Adds a `Deadline` task with <task> as a description and <deadline> as the deadline.
3. `event <task> /at <datetime>` - Adds an `Event` task with <task> as a description and <datetime> as the specific start and end `datetime`.
4. `exit` - Exits the Task Manager.
5. `list` - Lists out all the tasks that have been added, indicating their status.
6. `delete <task_type> <index>` - Deletes task at <index> number of type <task_type> when listed out using `list`. <task_type> can be of values `T` for `ToDo`, `D` for `Deadline` and `E` for `Event`.
7. `done <task_type> <index>` - Marks the task at <index> number of type <task_type> when listed out using `list` as done.
8. `save` - Saves the tasks data in `task.txt`.