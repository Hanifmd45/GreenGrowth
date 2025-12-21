from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from greengrowth_project.models.user import get_account_user, add_account_user
import MySQLdb.cursors

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Logic login
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Validasi data
        akun = get_account_user(email)
        if akun is None:
            flash('Login gagal, email atau password anda salah!')
        elif not check_password_hash(akun[4], password):
            flash('Login gagal, email atau password anda salah!')
        else:
            session['logged_in'] = True
            session['user_id'] = akun[0]
            session['user_role'] = akun[3]
            return redirect(url_for('user.dashboard'))
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Logic register
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        conf_password = request.form['conf_password']
        # Kondisi konfirmasi password
        if password != conf_password:
            flash('Password yang anda masukan tidak sesuai, silahkan coba lagi!')
            return redirect(url_for('auth.register'))
        # Mengecek apakah email sudah digunakan?
        user = get_account_user(email)
        if user:
            flash("Email sudah digunakan!")
            return render_template('auth/register.html')
        # Proses menambahkan akun baru
        add_account_user(nama,email,password)
        flash("Berhasil untuk mendaftar akun!")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')
