from generating_report_files import *

name_log = 'report_reab_sert_amount'
mail = 'IVAbdulganiev@yanao.ru'
table = 'uszn.temp$_r_reab_cert_inv_amount'
file_sql = 'report_reab_sert_amount.sql'

goto_folder()

report_temp_table(name_log, mail, table, file_sql)
