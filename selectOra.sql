SET LINESIZE 1000 TRIMSPOOL ON PAGESIZE 0 FEEDBACK OFF
SPOOL /var/lib/jenkins/dataCsvTemp/finance-dept_transaksi-penjualan-retail_ora-to-pg.csv
select 
    'ID_TRANSAKSI|ID_FRANCHAISE|FRANCHAISE|TANGGAL_TRANSAKSI|ID_PRODUK|NAMA_PRODUK|JUMLAH_TERJUAL|STOCK|DISCOUNT|PPN|PPH4|PPH23|STATUS_PEMBAYARAN|TANGGAL_PEMBAYARAN' 
from dual;
select 
    id_transaksi || '|' || id_franchaise || '|' || franchaise || '|' || tanggal_transaksi || '|' || id_produk || '|' || nama_produk || '|' || jumlah_terjual || '|' || stock || '|' || discount || '|' || PPN || '|' || PPH4 || '|' || PPH23 || '|' || status_pembayaran || '|' || tanggal_pembayaran 
from
    transaksi_penjualan_retail
order by id_transaksi;
SPOOL OFF
SET PAGESIZE 14
quit
