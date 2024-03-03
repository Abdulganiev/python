from generating_report_files import *

name_log = 'report_milk_age_3'
mail = 'IVAbdulganiev@yanao.ru'
table = 'uszn.temp$_baby_3'
file_sql = 'report_milk_age_3.sql'

goto_folder()

report_temp_table(name_log, mail, table, file_sql)
