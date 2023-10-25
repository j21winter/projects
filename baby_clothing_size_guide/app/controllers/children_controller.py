from app import app
from app.models.child_model import Child
from flask import request, redirect, render_template, session

@app.route('/child/create', methods=['POST'])
def create_child():
    Child.create_child(request.form)
    return redirect('/user/dashboard' )

@app.route('/child/update', methods=['POST'])
def update_child():
    Child.update_child(request.form)
    return redirect(f'/child/show/{request.form["id"]}')

@app.route('/child/show/<int:id>')
def child_dashboard(id):
    child = Child.get_one_by_id(id)

    print(child.date_of_birth)
    


    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    
    month = months[int(child.date_of_birth.strftime('%m'))-1]
    day = child.date_of_birth.strftime('%d')
    if(day[0] == '0'):
        day = day[1:]
    year = child.date_of_birth.strftime('%Y')

    child.format_date = f"{month} {day} {year}"

    return render_template('child_page.html', child = child)

@app.route('/child/delete/<int:id>')
def child_delete(id):
    Child.delete_child(id)
    return redirect("/user/dashboard")
    

