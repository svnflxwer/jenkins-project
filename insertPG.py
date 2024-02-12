import psycopg2, csv, json

def insert_data_to_pg(p_directory, p_filename):
    # Database connection parameters
    db_params_pg = {
        'database'  : 'dummydb',
        'user'      : 'postgres',
        'password'  : 'sinatriaba',
        'host'      : 'localhost',
        'port'      : '5432'
    }

    try:
        # Connect to the database
        print("MASUK KE POSTGRE...")
        connection_pg = psycopg2.connect(**db_params_pg)
        cursor_pg = connection_pg.cursor()

        # Open the CSV file for reading
        with open(f"{p_directory}/{p_filename}", newline='') as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header
            next(reader, None)
            # Iterate over each row in the CSV file
            for row in reader:
                kode_karyawan, nama, jabatan = row
                # Perform the insert operation
                cursor_pg.execute("INSERT INTO karyawan_it (kode_karyawan, nama, jabatan) VALUES (%s, %s, %s)", (kode_karyawan, nama, jabatan))

        # Commit the transaction
        connection_pg.commit()
        print("Data inserted successfully to PostgreSQL.")

    except Exception as e:
        print(f"Error inserting data to PostgreSQL: {e}")
        connection_pg.rollback()

    finally:
        cursor_pg.close()
        connection_pg.close()

def cek_data_pg():
    # Database connection parameters
    db_params_pg  = {
        'database'  : 'dummydb',
        'user'      : 'postgres',
        'password'  : 'sinatriaba',
        'host'      : 'localhost',
        'port'      : '5432'
    }

    # Create a list to store the names of offline jobs
    karyawan_pg  = []

    try:
        # Connect to the database
        connection_pg   = psycopg2.connect(**db_params_pg)
        cursor_pg       = connection_pg .cursor()

        # Query 
        query_pg        = """
                            SELECT 
                                kode_karyawan,
                                nama,
                                jabatan 
                            FROM 
                                karyawan_it
                        """
        v_body          = {}                   
        cursor_pg.execute(query_pg, v_body)
        
        # Fetch all records from PostgreSQL
        records_pg      = cursor_pg.fetchall()

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


if __name__ == "__main__":
    v_directory     = "/var/lib/jenkins/dataCsvTemp"
    v_filename      = "ora_to_post.csv"
    insert_data_to_pg(v_directory, v_filename)
    
    karyawan_pg     =  cek_data_pg()

    print("Postgre Result:")
    print(karyawan_pg)