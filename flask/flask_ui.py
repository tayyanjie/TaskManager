from flask import Flask, render_template, redirect, url_for, request, flash
import tasks_flask as tasks
import UI_flask as UI

app = Flask(__name__)
app.secret_key = "a10cs"

ui = UI.UI()


@app.route('/', methods=['GET','POST'])
def index():
    lst = [ui.list_todos()]
    print(lst)
    if request.method == 'POST':
        if 'button' in request.form:
            if "delete all tasks" in request.form['button']:
                return redirect(url_for('delete_all', type="all"))
            if "done" in request.form['button']:
                return redirect(url_for('done', messages=request.form['button'][5:]))
            if request.form['button'] == 'save':
                return redirect(url_for('save'))
            if "del" in request.form['button']:
                return redirect(url_for('delete', messages=request.form['button'][4:]))
            if "reset" in request.form['button']:
                return redirect(url_for('reset'))
        if 'add ToDo' in request.form:
            return redirect(url_for('add', description=request.form['description_ToDo'],
            type="ToDo"))
        elif 'add Deadline' in request.form:
            return redirect(url_for('add', description=request.form['description_Deadline'],
            dl=request.form['deadline_Deadline'], type="Deadline"))
        elif 'add Event' in request.form:
            return redirect(url_for('add', description=request.form['description_Event'],
            dl=request.form['deadline_Event'], type="Event"))
    return render_template('todos.html', todos = lst)


@app.route('/done', methods=['GET','POST'])
def done():
    msg = request.args['messages']
    task_type = "Event"
    ind = 1
    if 'ToDo' in msg:
        task_type = 'ToDo'
        ind = int(msg[4:])
    elif 'Deadline' in msg:
        task_type = 'Deadline'
        ind = int(msg[8:])
    else:
        ind = int(msg[5:])
    flash(ui.done(ind, task_type), "alert")
    return redirect('/')

@app.route('/add', methods=['GET', 'POST'])
def add():
    description = request.args['description']
    if description == "":
        res = "left_blank"
    elif request.args['type'] == 'ToDo':
        ui.add(description,"ToDo")
    elif request.args['type'] == 'Deadline':
        deadline = request.args['dl']
        res = (ui.add(description, "Deadline", deadline))
    elif request.args['type'] == 'Event':
        deadline = request.args['dl']
        res = (ui.add(description, "Event", deadline))
    if res == "Invalid format added":
        flash("Invalid format added", "error")
    elif res == "Invalid task added.":
        flash("Invalid task added", "error")
    elif res == "left_blank":
        flash("Do not leave description blank", "error")
    else:
        flash(res, "alert")
    return redirect('/')


@app.route('/delete', methods=['GET','POST'])
def delete():
    msg = request.args['messages']
    task_type = "Event"
    ind = 1
    if 'ToDo' in msg:
        task_type = 'ToDo'
        ind = int(msg[4:])
    elif 'Deadline' in msg:
        task_type = 'Deadline'
        ind = int(msg[8:])
    else:
        ind = int(msg[5:])
    flash(ui.delete(ind, task_type), "alert")
    return redirect('/')

@app.route('/delete_all', methods=['GET','POST'])
def delete_all():
    type = request.args['type']
    res = ui.delete_all(type)
    flash(res, 'alert')
    return redirect('/')

@app.route('/save')
def save():
    ui.save()
    flash("Saved!", "alert")
    return redirect('/')

@app.route('/reset')
def reset():
    global ui 
    ui = UI.UI()
    flash("Resetted!", "alert")
    return redirect('/')

#@app.route('/add')
#def add():
    

@app.route('/json')
def json():
    return render_template('json.html')

@app.route('/background_process_test')
def background_process_test():
    print ("Yos")
    return "nothing"

if __name__ == "__main__":
    app.run(debug=True)