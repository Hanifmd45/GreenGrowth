from flask import Blueprint, render_template, session, redirect, url_for
from greengrowth_project.models.program import get_all_programs

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    # Fetch programs from database
    programs = get_all_programs()
    
    # TODO: Fetch categories if needed
    categories = []
    
    return render_template('user/dashboard.html', programs=programs, categories=categories)