import cx_Oracle, csv, json

def export_to_csv(p_data, p_filename, p_directory):
    try:
        with open(f"{p_directory}/{p_filename}", mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['ID_PENGIRIMAN', 'ID_FRANCHAISE', 'FRANCHAISE', 'ID_PRODUK', 'NAMA_PRODUK', 'JUMLAH_DIKIRIM', 'TANGGAL_PENGIRIMAN', 'PENGIRIM', 'PENERIMA', 'STATUS_PENGIRIMAN' ])
            # Write the data
            for row in p_data:
                writer.writerow(row)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False

def get_data_ora():
    db_params_ora = {
        'user'      : 'giovanni',
        'password'  : 'iamhuman',
        'dsn'       : 'localhost.1:1521/XE'
    }

    logistik_ora        = []
    logistik_ora_json   = []

    try:
        connection_ora  = cx_Oracle.connect(**db_params_ora)
        cursor_ora      = connection_ora.cursor()

        query_ora       = """
                            SELECT 
                                ID_PENGIRIMAN,
                                ID_FRANCHAISE,
                                FRANCHAISE,
                                ID_PRODUK,
                                NAMA_PRODUK,
                                JUMLAH_DIKIRIM,
                                TANGGAL_PENGIRIMAn,
                                PENGIRIM,
                                PENERIMA,
                                STATUS_PENGIRIMAN
                            FROM 
                                LOGISTIK_PRODUK_RETAIL
                        """
        v_body          = {}
        cursor_ora.execute(query_ora, v_body)

        records_ora     = cursor_ora.fetchall()

        for record in records_ora:
            id_pengiriman, id_franchaise, franchaise, id_produk, nama_produk, jumlah_dikirim, tanggal_pengiriman, pengirim, penerima, status_pengiriman = record
            if id_franchaise:
                logistik_ora_json.append(id_franchaise)
            logistik_ora.append(record)

        return {
            "raw_data": logistik_ora,
            "json_data": json.dumps(logistik_ora_json)
        }

    except Exception as e:
        print(f"Error querying Oracle: {e}")
        return []

    finally:
        cursor_ora.close()
        connection_ora.close()

if __name__ == "__main__":
    logistik_ora = get_data_ora()

    if logistik_ora["raw_data"]:
        success = export_to_csv(logistik_ora["raw_data"], "logistic-dept_logistic-produk-retail_ora-to-pg.csv", "/var/lib/jenkins/dataCsvTemp")
        if success:
            print("Data has been exported to CSV successfully.")
            print("Oracle Result:")
            print(logistik_ora["json_data"])
        else:
            print("Failed to export data to CSV.")
    else:
        print("No data retrieved from Oracle.")
