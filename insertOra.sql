-- Use SQL*Loader to load data from CSV into Oracle table
OPTIONS (SKIP=1)
LOAD DATA
INFILE '/var/lib/jenkins/dataCsvTemp/finance-dept_transaksi-penjualan-retail_pg-to-ora.csv'
APPEND INTO TABLE transaksi_penjualan_retail
FIELDS TERMINATED BY ','
TRAILING NULLCOLS
(
    id_transaksi,
    id_franchise,
    franchise,
    tanggal_transaksi DATE "DD/MM/YYYY",
    id_produk,
    nama_produk,
    jumlah_terjual,
    stock,
    discount,
    PPN,
    PPH4,
    PPH23,
    status_pembayaran,
    tanggal_pembayaran DATE "DD/MM/YYYY"
)
