from flask import Blueprint, render_template, session, redirect, url_for, abort
from greengrowth_project.models.artikel import get_all_artikels, get_artikel_by_id

artikel_user_bp = Blueprint('artikel_user', __name__, url_prefix='/user/artikel')

@artikel_user_bp.route('/', methods=['GET'])
def list_artikel():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    artikels = get_all_artikels()
    return render_template('user/artikel.html', artikels=artikels)


@artikel_user_bp.route('/<int:artikel_id>', methods=['GET'])
def show(artikel_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    artikel = get_artikel_by_id(artikel_id)
    if not artikel:
        abort(404)
    return render_template('user/artikel.html', artikel=artikel)
