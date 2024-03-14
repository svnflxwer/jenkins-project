COPY (
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
        transaksi_penjualan_retail
) TO '/var/lib/jenkins/dataCsvTemp/finance-dept_transaksi-penjualan-retail_pg_to_ora.csv' WITH CSV HEADER;