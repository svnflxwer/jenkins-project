-- Buat temporary table untuk menampung data dari file CSV
CREATE TEMP TABLE temp_import_table (
    ID_TRANSAKSI        VARCHAR(50),
    ID_FRANCHAISE       VARCHAR(6),
    FRANCHAISE          VARCHAR(10),
    TANGGAL_TRANSAKSI   VARCHAR(5),
    ID_PRODUK           VARCHAR(8),
    NAMA_PRODUK         VARCHAR(3),
    JUMLAH_TERJUAL      VARCHAR(3),
    STOCK               VARCHAR(3),
    DISCOUNT            VARCHAR(3),
    PPN                 VARCHAR(7),
    PPH4                VARCHAR(7),
    PPH23               VARCHAR(7),
    STATUS_PEMBAYARAN   VARCHAR(9),
    TANGGAL_PEMBAYARAN  VARCHAR(10)
);

-- Copy data dari file CSV ke temporary table
COPY temp_import_table FROM '/var/lib/jenkins/dataCsvTemp/finance-dept_transaksi-penjualan-retail_ora-to-pg.csv' DELIMITER '|' CSV HEADER;

-- Insert data dari temporary table ke tabel utama
INSERT INTO transaksi_penjualan_retail (
    ID_TRANSAKSI,
    ID_FRANCHAISE,
    FRANCHAISE,
    TANGGAL_TRANSAKSI,
    ID_PRODUK,
    NAMA_PRODUK,
    JUMLAH_TERJUAL,
    STOCK,
    DISCOUNT,
    PPN,
    PPH4,
    PPH23,
    STATUS_PEMBAYARAN,
    TANGGAL_PEMBAYARAN
)
SELECT
    ID_TRANSAKSI,
    ID_FRANCHAISE,
    FRANCHAISE,
    TANGGAL_TRANSAKSI,
    ID_PRODUK,
    NAMA_PRODUK,
    JUMLAH_TERJUAL,
    STOCK,
    DISCOUNT,
    PPN,
    PPH4,
    PPH23,
    STATUS_PEMBAYARAN,
    TANGGAL_PEMBAYARAN
FROM
    temp_import_table;

-- Hapus temporary table
DROP TABLE temp_import_table;
