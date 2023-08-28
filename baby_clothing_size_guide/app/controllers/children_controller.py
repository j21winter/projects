from app import app
from app.models.child_model import Child
from flask import request, redirect, render_template

@app.route('/child/create', methods=['POST'])
def create_child():
    Child.create_child(request.form)
    return redirect('/user/dashboard')

@app.route('/child/update', methods=['POST'])
def update_child():
    Child.update_child(request.form)
    return redirect(f'/child/show/{request.form["id"]}')

@app.route('/child/show/<int:id>')
def child_dashboard(id):
    return render_template('child_page.html', child = Child.get_one_by_id(id))