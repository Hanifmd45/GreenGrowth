# Query untuk fitur Admin
def createLowongan_db(program_id,nama_lowongan, status_lowongan, min_umur, max_umur, keahlian, pengalaman, min_pendidikan, kuota_pekerja):
    # Import MYSQL
    from greengrowth_project.app import mysql
    # Query untuk menambah data
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO lowongan(program_id, judul_lowongan, status_lowongan, lowongan_min_umur, lowongan_max_umur, lowongan_keahlian, lowongan_pengalaman, lowongan_min_pendidikan, kuota_pekerja) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (program_id, nama_lowongan, status_lowongan, min_umur, max_umur, keahlian, pengalaman, min_pendidikan, kuota_pekerja,)
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error creating lowongan: {e}")
        return False
    
def readLowongan_db(program_id):
    # Import MySQL
    from greengrowth_project.app import mysql
    # Query untuk menampilkan seluruh data lowongan yang telah ditambah
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM lowongan WHERE program_id=%s", (program_id,)
        )
        result = cur.fetchall()
        cur.close()
        return result
    except Exception as e:
        return []

def readLowongan_by_id(lowongan_id):
    # Get detail lowongan berdasarkan lowongan_id
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM lowongan WHERE lowongan_id=%s", (lowongan_id,)
        )
        result = cur.fetchone()
        cur.close()
        return result
    except Exception as e:
        print(f"Error reading lowongan: {e}")
        return None

def updateLowongan_db(lowongan_id, program_id, nama_lowongan, status_lowongan, min_umur, max_umur, keahlian, pengalaman, min_pendidikan, kuota_pekerja):
    # Update lowongan
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE lowongan SET 
            program_id=%s,
            judul_lowongan=%s,
            status_lowongan=%s,
            lowongan_min_umur=%s,
            lowongan_max_umur=%s,
            lowongan_keahlian=%s,
            lowongan_pengalaman=%s,
            lowongan_min_pendidikan=%s,
            kuota_pekerja=%s
            WHERE lowongan_id=%s
            """,
            (program_id, nama_lowongan, status_lowongan, min_umur, max_umur, keahlian, pengalaman, min_pendidikan, kuota_pekerja, lowongan_id)
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error updating lowongan: {e}")
        return False

def deleteLowongan_db(lowongan_id):
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            DELETE FROM lowongan WHERE lowongan_id=%s
            """,(lowongan_id,)
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error deleting lowongan {e}")
        return False
    