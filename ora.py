import cx_Oracle
import json
import os
def check_cron_jobs_status_ora():
    cx_Oracle.init_oracle_client(config_dir="/mnt/d/MAGANG-SINAT/oracle-database-xe-11g/app/oracle/product/11.2.0/server/network/ADMIN")
    # Database connection parameters
    db_params_ora  = {
        'user'      : 'system',
        'password'  : 'sinatriaba',
        'dsn'       : 'localhost:1521/XE'
    }

    # Create a list to store the names of offline jobs
    karyawan_ora  = []

    try:
        # Connect to the database
        connection_ora  = cx_Oracle.connect(**db_params_ora)
        cursor_ora      = connection_ora.cursor()

        # Query 
        query_ora  = "SELECT KODE_KARYAWAN, NAMA, JABATAN FROM KARYAWAN"
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