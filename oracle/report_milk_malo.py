from generating_report_files import *

name_log = 'report_milk_malo'
mail = 'IVAbdulganiev@yanao.ru'
table = 'uszn.temp$_malo55_2024_01_01'
file_sql = 'report_milk_malo.sql'

goto_folder()

report_temp_table(name_log, mail, table, file_sql)
