from werkzeug.security import generate_password_hash


def get_account_admin(email):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin_pemerintah WHERE email_admin = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user


def get_program_by_admin(admin_id):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM program WHERE admin_id = %s LIMIT 1", (admin_id,))
    program = cur.fetchone()
    cur.close()
    return program


def get_all_programs_by_admin(admin_id):
    """Get semua program yang dimiliki admin"""
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT program_id, nama_program FROM program WHERE admin_id = %s", (admin_id,))
        programs = cur.fetchall()
        cur.close()
        print(f"DEBUG get_all_programs_by_admin: admin_id={admin_id}, programs={programs}")
        for i, p in enumerate(programs):
            print(f"  Program {i}: id={p[0]}, name={p[1]}")
        return programs
    except Exception as e:
        print(f"Error getting programs: {e}")
        return []