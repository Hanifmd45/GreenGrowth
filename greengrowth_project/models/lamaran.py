def cek_lamaran_exist(lowongan_id, user_id):
    from greengrowth_project.app import mysql

    cur = mysql.connection.cursor()
    cur.execute(
        """
        SELECT lamaran_id FROM lamaran
        WHERE lowongan_id = %s AND user_id = %s
        """,
        (lowongan_id, user_id)
    )
    data = cur.fetchone()
    cur.close()

    return data is not None

def create_lamaran_db(lowongan_id, user_id, status_lamaran):
    from greengrowth_project.app import mysql

    if cek_lamaran_exist(lowongan_id, user_id):
        return 'duplicate'

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO lamaran (lowongan_id, user_id, status_lamaran)
            VALUES (%s, %s, %s)
            """,
            (lowongan_id, user_id, status_lamaran)
        )
        mysql.connection.commit()
        cur.close()
        return 'success'
    except Exception as e:
        print(f"Error creating lamaran: {e}")
        return 'error'

def get_user_lamaran(user_id):
    """Get all applications by user with details"""
    from greengrowth_project.app import mysql
    
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT 
                l.lamaran_id,
                l.lowongan_id,
                l.status_lamaran,
                l.applied_at,
                lo.judul_lowongan,
                lo.status_lowongan,
                p.program_id,
                p.nama_program,
                p.lokasi_program
            FROM lamaran l
            JOIN lowongan lo ON l.lowongan_id = lo.lowongan_id
            JOIN program p ON lo.program_id = p.program_id
            WHERE l.user_id = %s
            ORDER BY l.applied_at DESC
            """,
            (user_id,)
        )
        rows = cur.fetchall()
        cur.close()
        
        lamaran_list = []
        for row in rows:
            lamaran_list.append({
                'id': row[0],
                'lowongan_id': row[1],
                'status': row[2],
                'applied_at': row[3],
                'judul_lowongan': row[4],
                'status_lowongan': row[5],
                'program_id': row[6],
                'nama_program': row[7],
                'lokasi_program': row[8]
            })
        
        return lamaran_list
    except Exception as e:
        print(f"Error getting user lamaran: {e}")
        return []
