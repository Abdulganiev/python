from generating_report_files import *

name_log = 'report_ES'
mail = 'IVAbdulganiev@yanao.ru'
table = 'uszn.temp$_r_ecert'
file_sql = 'report_ES.sql'
 
goto_folder()

report_temp_table(name_log, mail, table, file_sql)
