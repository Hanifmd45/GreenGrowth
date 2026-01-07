from flask import Blueprint, render_template, session, redirect, url_for

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    if session.get('role') != 'admin' or 'admin_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Import mysql here to avoid circular import
    from greengrowth_project.app import mysql
    
    admin_id = session.get('admin_id')

    # Get statistics for dashboard
    stats = {
        'total_programs': 0,
        'active_vacancies': 0,
        'pending_applications': 0,
        'total_articles': 0
    }
    
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        # Get programs count
        cursor.execute("SELECT COUNT(*) FROM program WHERE admin_id = %s", (admin_id,))
        result = cursor.fetchone()
        stats['total_programs'] = result[0] if result else 0
        
        # Get active vacancies count
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM lowongan l
            JOIN program p ON p.program_id = l.program_id
            WHERE p.admin_id = %s AND l.status_lowongan = 'dibuka'
            """,
            (admin_id,),
        )
        result = cursor.fetchone()
        stats['active_vacancies'] = result[0] if result else 0
        
        # Get pending applications count
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM lamaran a
            JOIN lowongan l ON l.lowongan_id = a.lowongan_id
            JOIN program p ON p.program_id = l.program_id
            WHERE p.admin_id = %s AND a.status_lamaran = 'menunggu'
            """,
            (admin_id,),
        )
        result = cursor.fetchone()
        stats['pending_applications'] = result[0] if result else 0
        
        # Get total articles count
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM artikel ar
            JOIN program p ON p.program_id = ar.program_id
            WHERE p.admin_id = %s
            """,
            (admin_id,),
        )
        result = cursor.fetchone()
        stats['total_articles'] = result[0] if result else 0
    except Exception as e:
        print(f"Error fetching stats: {e}")
        # Use default values if there's an error
    finally:
        try:
            if cursor is not None:
                cursor.close()
        except Exception:
            pass
    
    return render_template('admin/dashboard.html', stats=stats)

  
# greengrowth_project/controllers/admin/dashboard_admin.py