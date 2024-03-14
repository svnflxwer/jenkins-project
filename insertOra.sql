-- Create an External Table to read data from the CSV file
CREATE DIRECTORY temp_dir AS '/var/lib/jenkins/dataCsvTemp/';

CREATE TABLE ext_transaksi_penjualan_retail (
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
)
ORGANIZATION EXTERNAL (
    TYPE ORACLE_LOADER
    DEFAULT DIRECTORY temp_dir
    ACCESS PARAMETERS (
        RECORDS DELIMITED BY NEWLINE
        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
        MISSING FIELD VALUES ARE NULL
        REJECT ROWS WITH ALL NULL FIELDS
        (
            id_transaksi,
            id_franchise,
            franchise,
            tanggal_transaksi CHAR(10) DATE_FORMAT DATE MASK "YYYY-MM-DD",
            id_produk,
            nama_produk,
            jumlah_terjual,
            stock,
            discount,
            PPN,
            PPH4,
            PPH23,
            status_pembayaran,
            tanggal_pembayaran CHAR(10) DATE_FORMAT DATE MASK "YYYY-MM-DD"
        )
    )
    LOCATION ('finance-dept_transaksi-penjualan-retail_pg-to-ora.csv')
);

-- Insert data from the External Table into the target table in Oracle
MERGE INTO transaksi_penjualan_retail t
USING (
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
        ext_transaksi_penjualan_retail
) s
ON (t.id_transaksi = s.id_transaksi)
WHEN MATCHED THEN
    UPDATE SET
        t.id_franchise       = s.id_franchise,
        t.franchise          = s.franchise,
        t.tanggal_transaksi  = s.tanggal_transaksi,
        t.id_produk          = s.id_produk,
        t.nama_produk        = s.nama_produk,
        t.jumlah_terjual     = s.jumlah_terjual,
        t.stock              = s.stock,
        t.discount           = s.discount,
        t.PPN                = s.PPN,
        t.PPH4               = s.PPH4,
        t.PPH23              = s.PPH23,
        t.status_pembayaran  = s.status_pembayaran,
        t.tanggal_pembayaran = s.tanggal_pembayaran
WHEN NOT MATCHED THEN
    INSERT (
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
    VALUES (
        s.id_transaksi,
        s.id_franchise,
        s.franchise,
        s.tanggal_transaksi,
        s.id_produk,
        s.nama_produk,
        s.jumlah_terjual,
        s.stock,
        s.discount,
        s.PPN,
        s.PPH4,
        s.PPH23,
        s.status_pembayaran,
        s.tanggal_pembayaran
    );
