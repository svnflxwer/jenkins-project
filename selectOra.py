import cx_Oracle, csv, json

def export_to_csv(p_data, p_filename, p_directory):
    try:
        with open(f"{p_directory}/{p_filename}", mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['KODE_PEGAWAI', 'NAMA', 'JABATAN'])
            # Write the data
            for row in p_data:
                writer.writerow(row)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False

def get_data_ora():
    db_params_ora = {
        'user'      : 'jenkinsdb',
        'password'  : 'sinatriaba',
        'dsn'       : '192.168.56.1:1521/XE'
    }

    karyawan_ora        = []
    karyawan_ora_json   = []

    try:
        connection_ora  = cx_Oracle.connect(**db_params_ora)
        cursor_ora      = connection_ora.cursor()

        query_ora       = """
                            SELECT 
                                KODE_PEGAWAI, 
                                NAMA, 
                                JABATAN 
                            FROM 
                                KARYAWAN_IT
                        """
        v_body          = {}
        cursor_ora.execute(query_ora, v_body)

        records_ora     = cursor_ora.fetchall()

        for record in records_ora:
            kode_pegawai, nama ,jabatan = record
            if nama:
                karyawan_ora_json.append(nama)
            karyawan_ora.append(record)

        return {
            "raw_data": karyawan_ora,
            "json_data": json.dumps(karyawan_ora_json)
        }

    except Exception as e:
        print(f"Error querying Oracle: {e}")
        return []

    finally:
        cursor_ora.close()
        connection_ora.close()

if __name__ == "__main__":
    karyawan_ora = get_data_ora()

    if karyawan_ora["raw_data"]:
        success = export_to_csv(karyawan_ora["raw_data"], "logistic-dept_logistic-produk-retail_ora-to-pg.csv", "/var/lib/jenkins/dataCsvTemp")
        if success:
            print("Data has been exported to CSV successfully.")
            print("Oracle Result:")
            print(karyawan_ora["json_data"])
        else:
            print("Failed to export data to CSV.")
    else:
        print("No data retrieved from Oracle.")
