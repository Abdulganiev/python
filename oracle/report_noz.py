from generating_report_files import *

name_log = 'report_noz'
mail = 'IVAbdulganiev@yanao.ru'
table = 'uszn.temp$_r_inv_noz'
file_sql = 'report_noz.sql'

goto_folder()

report_temp_table(name_log, mail, table, file_sql)
