import os
from flask import Flask, render_template
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from .controllers.auth.routes import auth_bp
from .controllers.user.dashboard_user import user_bp
from .controllers.admin.dashboard_admin import admin_bp
from .controllers.admin.program_admin import program_bp
from .controllers.admin.artikel import artikel_bp
from .controllers.admin.lowongan_admin import lowongan_bp
from .controllers.admin.laporan import laporan_bp
from .controllers.admin.statistik import statistik_bp
from .controllers.admin.lamaran import lamaran_admin_bp
from .controllers.user.artikel import artikel_user_bp
from .controllers.user.profile import profile_user_bp as profil_bp
from .controllers.user.program import program_user_bp
from .controllers.user.lowongan import lowongan_user_bp
from .controllers.user.lamaran import lamaran_user_bp
load_dotenv()

app = Flask(__name__)
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT", 42925))
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DATABASE"] = os.environ.get("MYSQL_DATABASE")
mysql = MySQL(app)

# File upload config
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp) 
app.register_blueprint(program_bp) 
app.register_blueprint(artikel_bp)
app.register_blueprint(lowongan_bp)
app.register_blueprint(laporan_bp)
app.register_blueprint(artikel_user_bp)
app.register_blueprint(profil_bp)
app.register_blueprint(program_user_bp)
app.register_blueprint(lowongan_user_bp)
app.register_blueprint(lamaran_user_bp)
app.register_blueprint(statistik_bp)
app.register_blueprint(lamaran_admin_bp)

@app.route('/')
def home():
    return render_template('homepage/home.html')


# Handle oversize uploads gracefully
from werkzeug.exceptions import RequestEntityTooLarge

@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(error):
    from flask import flash, redirect, request
    flash('File terlalu besar (max 5MB).', 'error')
    return redirect(request.referrer or url_for('home'))

