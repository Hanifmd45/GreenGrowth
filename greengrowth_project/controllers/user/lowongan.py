from flask import Blueprint, render_template, session, redirect, url_for, abort
from greengrowth_project.models.lowongan import readLowongan_db, readLowongan_by_id

lowongan_user_bp = Blueprint('lowongan_user', __name__, url_prefix='/user/lowongan')

@lowongan_user_bp.route('/program/<int:program_id>', methods=['GET'])
def list_lowongan(program_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    lowongans = readLowongan_db(program_id)
    return render_template('user/lowongan.html', lowongans=lowongans, program_id=program_id) 

@lowongan_user_bp.route('/detail/<int:lowongan_id>', methods=['GET'])  
def show(lowongan_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    lowongan = readLowongan_by_id(lowongan_id)
    if not lowongan:
        abort(404)
    return render_template('user/lowongan_show.html', lowongan=lowongan)