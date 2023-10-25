from app import app
from app.models.suggestion_model import Suggestion
from flask import request, redirect, render_template, session

#*  NEW SEARCH
@app.route('/suggestion/search', methods=['POST'])
def search_suggestions():

    # GET ALL SUGGESTIONS USING THE FORM INFO
    Suggestion.get_search_suggestions(request.form)

    # RETURN BACK TO THE CHILD PAGE
    return redirect(f'/child/show/{request.form["child_id"]}')


#* FILTER SUGGESTION RESULTS ON THE CHILD PAGE
@app.route('/suggestion/filter', methods=['POST'])
def set_filter():
    # ASSIGN FILTER STRING TO SESSION
    session["result_filter"] = request.form["result_filter"]

    # RETURN TO CHILD PAGE
    return redirect (f"/child/show/{request.form['child_id']}")

#* DASHBOARD SEARCH RESULTS
@app.route('/suggestion/dashboard', methods=['POST'])
def set_CHILD_ID():
    # ASSIGN FILTER STRING TO SESSION
    session["display_child"] = request.form["display_child"]

    # RETURN TO CHILD PAGE
    return redirect ("/user/dashboard")