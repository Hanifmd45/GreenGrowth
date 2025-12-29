from flask import Blueprint, render_template, session, redirect, url_for, abort, request, flash 
from greengrowth_project.models.lowongan import readLowongan_db, readLowongan_by_id
from greengrowth_project.models.program import get_all_programs, get_program_by_id
from greengrowth_project.models.lamaran import create_lamaran_db, get_user_lamaran
from greengrowth_project.models.user import get_user_profile

ALLOWED_STATUS = {'menunggu', 'diterima', 'ditolak'}

lamaran_user_bp = Blueprint('lamaran_user', __name__, url_prefix='/user/lamaran')

@lamaran_user_bp.route('/apply/<int:lowongan_id>', methods=['GET', 'POST'])
def apply_lamaran(lowongan_id):
    """Halaman untuk apply lamaran - menampilkan profile user dan detail lowongan"""
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')

    # If user_id missing in session, redirect to login (preserve next)
    if not user_id:
        return redirect(url_for('auth.login', next=request.path))

    # Get user profile
    user_profile = get_user_profile(user_id)
    if not user_profile:
        flash('Profile belum lengkap. Silakan lengkapi profile terlebih dahulu.', 'warning')
        return redirect(url_for('profile_user.view_profile', user_id=user_id, next=request.path))
    
    # Get lowongan details
    lowongan = readLowongan_by_id(lowongan_id)
    if not lowongan:
        flash('Lowongan tidak ditemukan.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    # Get program details
    program = get_program_by_id(lowongan['program_id'])
    
    if request.method == 'POST':
        # Submit application
        result = create_lamaran_db(lowongan_id, user_id, 'menunggu')
        
        if result == 'duplicate':
            flash('Anda sudah melamar lowongan ini sebelumnya.', 'warning')
        elif result == 'success':
            flash('Lamaran berhasil dikirim! Anda dapat memantau status lamaran di My Activity.', 'success')
            return redirect(url_for('lamaran_user.my_activity'))
        else:
            flash('Terjadi kesalahan. Silakan coba lagi.', 'danger')
    
    return render_template(
        'user/lamaran_apply.html',
        user=user_profile,
        lowongan=lowongan,
        program=program
    )

@lamaran_user_bp.route('/my-activity', methods=['GET'])
def my_activity():
    """Halaman untuk melihat semua lamaran user dan statusnya"""
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')
    
    # Get all user's applications
    lamaran_list = get_user_lamaran(user_id)
    
    return render_template(
        'user/my_activity.html',
        lamaran_list=lamaran_list
    )

# Keep old route for backward compatibility
@lamaran_user_bp.route('/create', methods=['GET', 'POST'])
def create_lamaran():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))

    programs = get_all_programs()
    program_id = request.args.get('program_id')
    lowongan_id = request.args.get('lowongan_id')
    
    # If lowongan_id is provided, redirect to new apply route
    if lowongan_id:
        return redirect(url_for('lamaran_user.apply_lamaran', lowongan_id=lowongan_id))

    if not program_id:
        flash('Silakan pilih program terlebih dahulu.', 'warning')
        return render_template(
            'user/lamaran_create.html',
            programs=programs,
            lowongans=[],
            selected_program_id=None
        )

    lowongans = readLowongan_db(program_id)

    if request.method == 'POST':
        lowongan_id = request.form.get('lowongan_id')

        if not lowongan_id:
            flash('Lowongan tidak valid.', 'danger')
            return redirect(url_for('lamaran_user.create_lamaran', program_id=program_id))

        user_id = session.get('user_id')

        result = create_lamaran_db(lowongan_id, user_id, 'menunggu')

        if result == 'duplicate':
            flash('Kamu sudah melamar lowongan ini.', 'warning')
        elif result == 'success':
            flash('Lamaran berhasil dikirim.', 'success')
            return redirect(url_for('lamaran_user.my_activity'))
        else:
            flash('Terjadi kesalahan sistem.', 'danger')

        return redirect(url_for('lamaran_user.create_lamaran', program_id=program_id))

    return render_template(
        'user/lamaran_create.html',
        programs=programs,
        lowongans=lowongans,
        selected_program_id=program_id
    )

    

    
    

   
