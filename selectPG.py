import psycopg2, csv, json


def export_to_csv(p_data, p_filename, p_directory):
    try:
        with open(f"{p_directory}/{p_filename}", mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow([
                "ID_TRANSAKSI",
                "ID_FRANCHAISE",
                "FRANCHAISE",
                "TANGGAL_TRANSAKSI",
                "ID_PRODUK",
                "NAMA_PRODUK",
                "JUMLAH_TERJUAL",
                "STOCK",
                "DISCOUNT",
                "PPN",
                "PPH4",
                "PPH23",
                "STATUS_PEMBAYARAN",
                "TANGGAL_PEMBAYARAN"
            ])
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

    v_transaksi_pg      = []
    v_transaksi_pg_json = []
    
    try:
        # Connect to the database
        print("MASUK KE POSTGRE...")
        connection_pg = psycopg2.connect(**db_params_pg)
        cursor_pg = connection_pg.cursor()

        query_pg = """
                    SELECT 
                        id_transaksi,
                        id_franchaise,
                        franchaise,
                        tanggal_transaksi,
                        id_produk,
                        nama_produk,
                        jumlah_terjual,
                        stock,
                        discount,
                        PPN,
                        PPH4,
                        PPH23,
                        status_pembayaran,
                        tanggal_pembayaran
                    FROM 
                        transaksi_penjualan_retail
                    """
        cursor_pg.execute(query_pg)

        records_pg = cursor_pg.fetchall()

        for record in records_pg:
            kode_pegawai, nama ,jabatan ,status_pekerjaan, gaji, informasi_kontak = record
            if nama:
                v_transaksi_pg_json.append(nama)
            v_transaksi_pg.append(record)

        return {
            "raw_data": v_transaksi_pg,
            "json_data": json.dumps(v_transaksi_pg_json)
        }

    except Exception as e:
        print(f"Error inserting data to PostgreSQL: {e}")
        connection_pg.rollback()

    finally:
        cursor_pg.close()
        connection_pg.close()


if __name__ == "__main__":
    v_transaksi_pg   = select_data_pg()

    if v_transaksi_pg["raw_data"]:
        success = export_to_csv(v_transaksi_pg["raw_data"], "finance-dept_transaksi-penjualan-retail_pg-to-ora.csv", "/var/lib/jenkins/dataCsvTemp")
        if success:
            print("Data has been exported to CSV successfully.")
            print("Postgre Result:")
            print(v_transaksi_pg["json_data"])
        else:
            print("Failed to export data to CSV.")
    else:
        print("No data retrieved from Postgre.")