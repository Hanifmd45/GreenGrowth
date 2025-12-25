def createProgram_db(nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program):
    from greengrowth_project.app import mysql

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO program(nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program) VALUES(%s, %s, %s, %s, %s, %s)",
        (nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program),
    )
    mysql.connection.commit()
    cur.close()


def get_all_programs():
    """Return list of programs as dicts"""
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT program_id, nama_program FROM program ORDER BY nama_program ASC")
    rows = cur.fetchall()
    cur.close()
    programs = []
    for r in rows:
        programs.append({
            'program_id': r[0],
            'nama_program': r[1]
        })
    return programs


def get_program_by_id(program_id):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT program_id, nama_program FROM program WHERE program_id=%s", (program_id,))
    r = cur.fetchone()
    cur.close()
    if not r:
        return None
    return {'program_id': r[0], 'nama_program': r[1]}


