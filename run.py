import tasks
import UI

def run():
    ui = UI.UI()
    ui.welcome()
    exit = False
    while not exit:
        command = ui.getCommand()
        exit = not ui.parseCommand(command)
    input("Press enter to exit.")


run()
