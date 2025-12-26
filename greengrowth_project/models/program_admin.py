def createProgram_db(admin_id, nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program):
    # Insert a program into the DB with admin_id
    from greengrowth_project.app import mysql

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO program(nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, admin_id) VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, admin_id),
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error creating program: {e}")
        return False


def readProgram_by_admin(admin_id):
    # Get semua program milik admin
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT program_id, nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, admin_id FROM program WHERE admin_id = %s", (admin_id,))
        programs = cur.fetchall()
        cur.close()
        return programs
    except Exception as e:
        print(f"Error reading programs: {e}")
        return []


def readProgram_by_id(program_id):
    # Get detail program berdasarkan ID - return: (program_id, nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, admin_id)
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT program_id, nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, admin_id FROM program WHERE program_id = %s", (program_id,))
        program = cur.fetchone()
        cur.close()
        return program
    except Exception as e:
        print(f"Error reading program: {e}")
        return None


def updateProgram_db(program_id, nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program):
    # Update program
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE program SET nama_program=%s, sektor_program=%s, tujuan_program=%s, lokasi_program=%s, status_program=%s, deskripsi_program=%s WHERE program_id=%s",
            (nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, program_id),
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error updating program: {e}")
        return False


def deleteProgram_db(program_id):
    # Hapus program
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM program WHERE program_id = %s", (program_id,))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error deleting program: {e}")
        return False



