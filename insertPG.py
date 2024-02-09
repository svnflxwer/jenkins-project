import psycopg2
import cx_Oracle
import json

def check_cron_jobs_status_pg():
    # Database connection parameters
    db_params_pg  = {
        'database': 'dummydb',
        'user': 'postgres',
        'password': 'sinatriaba',
        'host': 'localhost',
        'port': '5432'
    }

    # Create a list to store the names of offline jobs
    karyawan_pg  = []

    try:
        # Connect to the database
        connection_pg   = psycopg2.connect(**db_params_pg)
        cursor_pg       = connection_pg .cursor()

        # Query 
        query_pg        = "SELECT kode_karyawan, nama, jabatan FROM karyawan"
        cursor_pg.execute(query_pg )
        
        # Fetch all records from PostgreSQL
        records_pg          = cursor_pg.fetchall()

        for record in records_pg :
            kode_pegawai, nama ,jabatan = record
            if nama:
                karyawan_pg.append(nama)

        # Return the list of offline jobs as a JSON string
        return json.dumps(karyawan_pg)

    except Exception as e:
        return json.dumps({"error_pg": str(e)})
    finally:
        if 'cursor_pg' in locals():
            cursor_pg.close()
        if 'connection_pg' in locals():
            connection_pg.close()


# def check_cron_jobs_status_ora():
#     # Database connection parameters
#     db_params_ora  = {
#         'user'      : 'system',
#         'password'  : 'sinatriaba',
#         'dsn'       : 'localhost:1521/XE'
#     }

#     # Create a list to store the names of offline jobs
#     karyawan_ora  = []

#     try:
#         # Connect to the database
#         connection_ora  = cx_Oracle.connect(**db_params_ora)
#         cursor_ora      = connection_ora.cursor()

#         # Query 
#         query_ora  = "SELECT KODE_KARYAWAN, NAMA, JABATAN FROM KARYAWAN"
#         cursor_ora.execute(query_ora)

#         # Fetch all records from Oracle
#         records_ora = cursor_ora.fetchall()

#         for record in records_ora:
#             kode_pegawai, nama, jabatan = record
#             if kode_pegawai:
#                 karyawan_ora.append(kode_pegawai)

#         # Return the list of offline jobs as a JSON string
#         return json.dumps(karyawan_ora)

#     except Exception as e:
#         return json.dumps({"error_ora": str(e)})
#     finally:
#         if 'cursor_ora' in locals():
#             cursor_ora.close()
#         if 'connection_ora' in locals():
#             connection_ora.close()

if __name__ == "__main__":
    karyawan_pg     = check_cron_jobs_status_pg()
    # karyawan_ora    = check_cron_jobs_status_ora()
    
    # Print the results
    print("PostgreSQL Result:")
    print(karyawan_pg)

    # print("Oracle Result:")
    # print(karyawan_ora)