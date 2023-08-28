from app import app
from app.models.suggestion_model import Suggestion
from flask import request, redirect, render_template

@app.route('/suggestion/search', methods=['POST'])
def search_suggestions():
    Suggestion.get_search_suggestions(request.form)
    # Suggestion.get_search_suggestions_for_height(request.form)
    # Suggestion.get_search_suggestions_for_weight(request.form)
    return redirect(f'/child/show/{request.form["child_id"]}')