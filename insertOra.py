import cx_Oracle, csv, json

def insert_data_ora(p_directory, p_filename):
    db_params_ora = {
        'user'      : 'jenkinsdb',
        'password'  : 'sinatriaba',
        'dsn'       : '192.168.56.1:1521/XE'
    }

    try:
        print("MASUK KE ORACLE...")
        connection_ora = cx_Oracle.connect(**db_params_ora)
        cursor_ora = connection_ora.cursor()

        # Open the CSV file for reading
        with open(f"{p_directory}/{p_filename}", newline='') as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header
            next(reader, None)
            # Iterate over each row in the CSV file
            for row in reader:
                kode_pegawai, nama ,jabatan ,status_pekerjaan, gaji, informasi_kontak = row
                # Perform the insert operation
                query_ora   = """
                                INSERT INTO karyawan_hr (kode_pegawai, nama, jabatan, status_pekerjaan, gaji, informasi_kontak) 
                                VALUES (
                                    :kode_pegawai,
                                    :nama,
                                    :jabatan,
                                    :status_pekerjaan,
                                    :gaji,
                                    :informasi_kontak
                                )
                            """
                v_body      = {
                    "kode_pegawai"      : kode_pegawai,
                    "nama"              : nama,
                    "jabatan"           : jabatan,
                    "status_pekerjaan"  : status_pekerjaan,
                    "gaji"              : gaji,
                    "informasi_kontak"  : informasi_kontak
                }
                        
                cursor_ora.execute(query_ora, v_body)

        # Commit the transaction
        connection_ora.commit()
        print("Data inserted successfully to Oracle.")

    except Exception as e:
        print(f"Error querying Oracle: {e}")
        return []

    finally:
        cursor_ora.close()
        connection_ora.close()


def cek_data_ora():
    # Database connection parameters
    db_params_ora = {
        'user': 'jenkinsdb',
        'password': 'sinatriaba',
        'dsn': '192.168.56.1:1521/XE'
    }
    # Create a list to store the names of offline jobs
    karyawan_ora  = []

    try:
        # Connect to the database
        connection_ora  = cx_Oracle.connect(**db_params_ora)
        cursor_ora      = connection_ora.cursor()

        # Query 
        query_ora        = """
                            SELECT 
                                kode_pegawai,
                                nama,
                                jabatan,
                                status_pekerjaan,
                                gaji,
                                informasi_kontak 
                            FROM 
                                karyawan_hr
                        """
        v_body          = {}
        cursor_ora.execute(query_ora, v_body)
        
        # Fetch all records from Oracle
        records_ora     = cursor_ora.fetchall()

        for record in records_ora :
            kode_pegawai, nama ,jabatan, status_pekerjaan, gaji, informasi_kontak = record
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
    v_directory   = "/var/lib/jenkins/dataCsvTemp"
    v_filename    = "finance-dept_transfer-karyawan-it_pg-to-ora.csv"
    insert_data_ora(v_directory, v_filename)

    karyawan_ora  = cek_data_ora()

    print("Oracle Result:")
    print(karyawan_ora)
