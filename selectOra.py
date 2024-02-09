import cx_Oracle
import json
import os, platform
def check_cron_jobs_status_ora():

    db_params_ora  = {
        'user'      : 'jenkinsdb',
        'password'  : 'sinatriaba',
        'dsn'       : '192.168.56.1:1521/XE'
    }

    # Create a list to store the names of offline jobs
    karyawan_ora  = []

    try:
        # Connect to the database
        print("MASUK KE ORACLE...")
        connection_ora  = cx_Oracle.connect(**db_params_ora)
        print(connection_ora)
        cursor_ora      = connection_ora.cursor()
        # Query 
        query_ora  = """
                        SELECT 
                            KODE_PEGAWAI, 
                            NAMA, 
                            JABATAN 
                        FROM 
                            KARYAWAN_IT
                    """
        cursor_ora.execute(query_ora)

        # Fetch all records from Oracle
        records_ora = cursor_ora.fetchall()

        for record in records_ora:
            kode_pegawai, nama, jabatan = record
            if nama:
                karyawan_ora.append(nama)

        # Return the list of offline jobs as a JSON string
        return json.dumps(karyawan_ora)

    except Exception as e:
        return json.dumps({"error_ora": str(e)})
    finally:
        if 'cursor_ora' in locals():
            cursor_ora.close()
        if 'connection_ora' in locals():
            connection_ora.close()

if __name__ == "__main__":
    karyawan_ora    = check_cron_jobs_status_ora()

    print("Oracle Result:")
    print(karyawan_ora)