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
                id_pengiriman, id_franchaise, franchaise, id_produk, nama_produk, jumlah_dikirim, tanggal_pengiriman, pengirim, penerima, status_pengiriman = row
                # Perform the insert operation
                v_query     = """
                                INSERT INTO logistik_produk_retail (
                                    id_pengiriman, 
                                    id_franchaise, 
                                    franchaise, 
                                    id_produk, 
                                    nama_produk, 
                                    jumlah_dikirim, 
                                    tanggal_pengiriman, 
                                    pengirim, 
                                    penerima, 
                                    status_pengiriman
                                ) 
                                VALUES (
                                    %(id_pengiriman)s, 
                                    %(id_franchaise)s, 
                                    %(franchaise)s
                                    %(id_produk)s
                                    %(nama_produk)s
                                    %(jumlah_dikirim)s
                                    %(tanggal_pengiriman)s
                                    %(pengirim)s
                                    %(penerima)s
                                    %(status_pengiriman)s
                                )
                                ON CONFLICT (id_pengiriman) DO NOTHING;
                            """
                v_kondisi   = {
                    "id_pengiriman"     : id_pengiriman,
                    "id_franchaise"     : id_franchaise,
                    "franchaise"        : franchaise,
                    "id_produk"         : id_produk,
                    "nama_produk"       : nama_produk,
                    "jumlah_dikirim"    : jumlah_dikirim,
                    "tanggal_pengiriman": tanggal_pengiriman,
                    "pengirim"          : pengirim,
                    "penerima"          : penerima,
                    "status_pengiriman" : status_pengiriman,

                }
                cursor_pg.execute(v_query, v_kondisi)

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
    franchaise_pg  = []

    try:
        # Connect to the database
        connection_pg   = psycopg2.connect(**db_params_pg)
        cursor_pg       = connection_pg .cursor()

        # Query 
        query_pg        = """
                            SELECT 
                                id_pengiriman,
                                id_franchaise,
                                franchaise,
                                id_produk,
                                nama_produk,
                                jumlah_dikirim,
                                tanggal_pengiriman,
                                pengirim,
                                penerima,
                                status_pengiriman
                            FROM 
                                logistik_produk_retail
                        """
        v_body          = {}                   
        cursor_pg.execute(query_pg, v_body)
        
        # Fetch all records from PostgreSQL
        records_pg      = cursor_pg.fetchall()

        for record in records_pg :
            id_pengiriman, id_franchaise, franchaise, id_produk, nama_produk, jumlah_dikirim, tanggal_pengiriman, pengirim, penerima, status_pengiriman = record
            if franchaise:
                franchaise_pg.append(franchaise)

        # Return the list of offline jobs as a JSON string
        return json.dumps(franchaise_pg)

    except Exception as e:
        return json.dumps({"error_pg": str(e)})
    finally:
        if 'cursor_pg' in locals():
            cursor_pg.close()
        if 'connection_pg' in locals():
            connection_pg.close()


if __name__ == "__main__":
    v_directory     = "/var/lib/jenkins/dataCsvTemp"
    v_filename      = "logistic-dept_logistic-produk-retail_ora-to-pg.csv"
    insert_data_to_pg(v_directory, v_filename)
    
    franchaise_pg     =  cek_data_pg()

    print("Postgre Result:")
    print(franchaise_pg)