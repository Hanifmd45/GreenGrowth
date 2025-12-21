from werkzeug.security import generate_password_hash


def get_account_user(email):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email_user = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user

def add_account_user(nama_user, email_user, password_user):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(nama_user, email_user, password_user) VALUES(%s, %s, %s)", (nama_user, email_user, generate_password_hash(password_user)))
    mysql.connection.commit()
    cur.close()
