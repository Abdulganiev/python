from generating_report_files import *

name_log = 'report_MSK_all'
mail = 'IVAbdulganiev@yanao.ru'
table = 'uszn.temp$_msk_all'
file_sql = 'report_MSK_all.sql'

report_temp_table(name_log, mail, table, file_sql)
