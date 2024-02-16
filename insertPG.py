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
                id, brand, variant, arrival_date, price, supplier, discount, stock, expired_date, weight, category = row
                # Perform the insert operation
                v_query     = """
                                INSERT INTO produk_aaa (id, brand, variant, arrival_date, price, supplier, discount, stock, expired_date, weight, category) 
                                VALUES (
                                    %(id)s, 
                                    %(brand)s, 
                                    %(variant)s,
                                    %(arrival_date)s,
                                    %(price)s,
                                    %(supplier)s,
                                    %(discount)s,
                                    %(stock)s,
                                    %(expired_date)s,
                                    %(weight)s,
                                    %(category)s
                                )
                                ON CONFLICT (id) DO NOTHING;
                            """
                v_kondisi   = {
                    "id"            : id,
                    "brand"         : brand,
                    "variant"       : variant,
                    "arrival_date"  : arrival_date,
                    "price"         : price,
                    "supplier"      : supplier,
                    "discount"      : discount,
                    "stock"         : stock,
                    "expired_date"  : expired_date,
                    "weight"        : weight,
                    "category"      : category
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
    karyawan_pg  = []

    try:
        # Connect to the database
        connection_pg   = psycopg2.connect(**db_params_pg)
        cursor_pg       = connection_pg .cursor()

        # Query 
        query_pg        = """
                            SELECT 
                                id, brand, variant, arrival_date, price, supplier, discount, stock, expired_date, weight, category
                            FROM 
                                produk_aaa
                        """
        v_body          = {}                   
        cursor_pg.execute(query_pg, v_body)
        
        # Fetch all records from PostgreSQL
        records_pg      = cursor_pg.fetchall()

        for record in records_pg :
            id, first_name, last_name, email, job_title, department, gender = record
            if email:
                karyawan_pg.append(email)

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
    v_filename      = "logistic-dept_produk-aaa_ora-to-pg.csv"
    insert_data_to_pg(v_directory, v_filename)
    
    karyawan_pg     =  cek_data_pg()

    print("Postgre Result:")
    print(karyawan_pg)