-- Step 1: Create a temporary table in Oracle to match the structure of the CSV file
CREATE GLOBAL TEMPORARY TABLE temp_transaksi_penjualan_retail (
    id_transaksi       VARCHAR2(255),
    id_franchise       VARCHAR2(255),
    franchise          VARCHAR2(255),
    tanggal_transaksi  DATE,
    id_produk          VARCHAR2(255),
    nama_produk        VARCHAR2(255),
    jumlah_terjual     NUMBER,
    stock              NUMBER,
    discount           NUMBER,
    PPN                NUMBER,
    PPH4               NUMBER,
    PPH23              NUMBER,
    status_pembayaran  VARCHAR2(255),
    tanggal_pembayaran DATE
) ON COMMIT PRESERVE ROWS; -- Preserve rows until commit

-- Step 2: Load data from the CSV file into the temporary table using External Tables
CREATE DIRECTORY temp_dir AS '/var/lib/jenkins/dataCsvTemp/';

-- Define the External Table
CREATE TABLE ext_transaksi_penjualan_retail
(
    id_transaksi       VARCHAR2(255),
    id_franchise       VARCHAR2(255),
    franchise          VARCHAR2(255),
    tanggal_transaksi  CHAR(10),
    id_produk          VARCHAR2(255),
    nama_produk        VARCHAR2(255),
    jumlah_terjual     NUMBER,
    stock              NUMBER,
    discount           NUMBER,
    PPN                NUMBER,
    PPH4               NUMBER,
    PPH23              NUMBER,
    status_pembayaran  VARCHAR2(255),
    tanggal_pembayaran CHAR(10)
)
ORGANIZATION EXTERNAL (
    TYPE ORACLE_LOADER
    DEFAULT DIRECTORY temp_dir
    ACCESS PARAMETERS (
        RECORDS DELIMITED BY NEWLINE
        FIELDS TERMINATED BY ','
        MISSING FIELD VALUES ARE NULL
        (
            id_transaksi,
            id_franchise,
            franchise,
            tanggal_transaksi CHAR(10) DATE_FORMAT DATE MASK "MM/DD/YYYY",
            id_produk,
            nama_produk,
            jumlah_terjual,
            stock,
            discount,
            PPN,
            PPH4,
            PPH23,
            status_pembayaran,
            tanggal_pembayaran CHAR(10) DATE_FORMAT DATE MASK "MM/DD/YYYY"
        )
    )
    LOCATION ('finance-dept_transaksi-penjualan-retail_pg_to_ora.csv')
);

-- Step 3: Insert data from the External Table into the temporary table
INSERT INTO temp_transaksi_penjualan_retail
SELECT * FROM ext_transaksi_penjualan_retail;

-- Step 4: Insert data from the temporary table into the target table in Oracle
INSERT INTO target_transaksi_penjualan_retail (
    id_transaksi,
    id_franchise,
    franchise,
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
)
SELECT
    id_transaksi,
    id_franchise,
    franchise,
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
    temp_transaksi_penjualan_retail;
