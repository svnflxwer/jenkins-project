import psycopg2, csv, json


def export_to_csv(p_data, p_filename, p_directory):
    try:
        with open(f"{p_directory}/{p_filename}", mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['KODE_PEGAWAI', 'NAMA', 'JABATAN', 'STATUS_PEKERJAAN', 'GAJI', 'INFORMASI_KONTAK' ])
            # Write the data
            for row in p_data:
                writer.writerow(row)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False
    
    
def select_data_pg():
    # Database connection parameters
    db_params_pg = {
        'database'  : 'dummydb',
        'user'      : 'postgres',
        'password'  : 'sinatriaba',
        'host'      : 'localhost',
        'port'      : '5432'
    }

    karyawan_pg      = []
    karyawan_pg_json = []
    
    try:
        # Connect to the database
        print("MASUK KE POSTGRE...")
        connection_pg = psycopg2.connect(**db_params_pg)
        cursor_pg = connection_pg.cursor()

        query_pg = """
                    SELECT 
                        KODE_PEGAWAI, 
                        NAMA, 
                        JABATAN,
                        STATUS_PEKERJAAN,
                        GAJI,
                        INFORMASI_KONTAK 
                    FROM 
                        KARYAWAN_HR
                    """
        cursor_pg.execute(query_pg)

        records_pg = cursor_pg.fetchall()

        for record in records_pg:
            kode_pegawai, nama ,jabatan ,status_pekerjaan, gaji, informasi_kontak = record
            if nama:
                karyawan_pg_json.append(nama)
            karyawan_pg.append(record)

        return {
            "raw_data": karyawan_pg,
            "json_data": json.dumps(karyawan_pg_json)
        }

    except Exception as e:
        print(f"Error inserting data to PostgreSQL: {e}")
        connection_pg.rollback()

    finally:
        cursor_pg.close()
        connection_pg.close()


if __name__ == "__main__":
    karyawan_pg   = select_data_pg()

    if karyawan_pg["raw_data"]:
        success = export_to_csv(karyawan_pg["raw_data"], "finance-dept_transfer-karyawan-it_pg-to-ora.csv", "/var/lib/jenkins/dataCsvTemp")
        if success:
            print("Data has been exported to CSV successfully.")
            print("Postgre Result:")
            print(karyawan_pg["json_data"])
        else:
            print("Failed to export data to CSV.")
    else:
        print("No data retrieved from Postgre.")