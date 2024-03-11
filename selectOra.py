import cx_Oracle, csv, json

def export_to_csv(p_data, p_filename, p_directory):
    try:
        with open(f"{p_directory}/{p_filename}", mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(["ID", "BRAND", "VARIANT", "ARRIVAL_DATE", "PRICE", "SUPPLIER", "DISCOUNT", "STOCK", "EXPIRED_DATE", "WEIGHT", "CATEGORY"])
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
        'dsn'       : 'localhost:1521/XE'
    }

    produk_ora        = []
    produk_ora_json   = []

    try:
        connection_ora  = cx_Oracle.connect(**db_params_ora)
        cursor_ora      = connection_ora.cursor()

        query_ora       = """
                            SELECT 
                                ID,
                                BRAND,
                                VARIANT,
                                ARRIVAL_DATE,
                                PRICE,
                                SUPPLIER,
                                DISCOUNT,
                                STOCK,
                                EXPIRED_DATE,
                                WEIGHT,
                                CATEGORY
                            FROM 
                                PRODUCT_AAA
                        """
        v_body          = {}
        cursor_ora.execute(query_ora, v_body)

        records_ora     = cursor_ora.fetchall()

        for record in records_ora:
            id, brand, variant, arrival_date, price, supplier, discount, stock, expired_date, weight, category = record
            if brand:
                produk_ora_json.append(brand)
            produk_ora.append(record)

        return {
            "raw_data": produk_ora,
            "json_data": json.dumps(produk_ora_json)
        }

    except Exception as e:
        print(f"Error querying Oracle: {e}")
        return []

    finally:
        cursor_ora.close()
        connection_ora.close()

if __name__ == "__main__":
    produk_ora = get_data_ora()

    if produk_ora["raw_data"]:
        success = export_to_csv(produk_ora["raw_data"], "logistic-dept_produk-aaa_ora-to-pg.csv", "/var/lib/jenkins/dataCsvTemp")
        if success:
            print("Data has been exported to CSV successfully.")
            print("Oracle Result:")
            print(produk_ora["json_data"])
        else:
            print("Failed to export data to CSV.")
    else:
        print("No data retrieved from Oracle.")
