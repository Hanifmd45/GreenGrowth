from flask import Blueprint, render_template, session, redirect, url_for, abort
from greengrowth_project.models.program import get_all_programs, get_program_by_id

program_user_bp = Blueprint('program_user', __name__, url_prefix='/user/program')

@program_user_bp.route('/', methods=['GET'])
def list_programs():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    programs = get_all_programs()
    return render_template('user/dashboard.html', programs=programs)

@program_user_bp.route('/<int:program_id>', methods=['GET'])
def show(program_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    program = get_program_by_id(program_id)
    if not program:
        abort(404)
    return render_template('user/program_show.html', program=program)