from flask import Blueprint, render_template, request, redirect, url_for, Response
from greengrowth_project.models.program_admin import createProgram_db
program_bp = Blueprint('program', __name__, url_prefix='/program')

ALLOWED_STATUS = {'perencanaan', 'berjalan', 'selesai'}

@program_bp.route('/create_program', methods=['GET', 'POST'])
def create_program():
    if request.method == 'POST':
        # Ambil data dari form
        nama_program = request.form['nama_program']
        sektor_program = request.form['sektor_program']
        tujuan_program = request.form['tujuan_program']
        lokasi_program = request.form['lokasi_program']
        status_program = request.form.get('status_program', 'perencanaan')
        if status_program not in ALLOWED_STATUS:
            status_program = 'perencanaan'
        deskripsi_program = request.form['deskripsi_program']
        createProgram_db(nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program)
        return redirect(url_for('program.create_program'))
    return render_template('admin/program.html')

