from flask import Blueprint, render_template, session, redirect, url_for
from greengrowth_project.controllers.admin.program_admin import createProgram

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html')

@admin_bp.route('/create_program', methods=['GET', 'POST'])
def create_program():
    return createProgram()
  