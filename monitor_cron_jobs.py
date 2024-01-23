import psycopg2
import json

def check_cron_jobs_status():
    # Database connection parameters
    db_params = {
        'database': 'dummydb',
        'user': 'jenkins_user',
        'password': 'dummyDB',
        'host': '172.28.144.49',
        'port': '5432'
    }

    # Connect to the database
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Query 
    query = "SELECT kode_pegawai, nama, jabatan FROM Karyawan"

    # Create a list to store the names of offline jobs
    karyawan = []

    try:
        cursor.execute(query)
        records = cursor.fetchall()

        for record in records:
            nama, kode_pegawai ,jabatan = record
            if not nama:
                karyawan.append(nama)

        # Return the list of offline jobs as a JSON string
        return json.dumps(karyawan)

    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    karyawan = check_cron_jobs_status()
    print(karyawan)