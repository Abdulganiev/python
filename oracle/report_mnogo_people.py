from generating_report_files import *

name_log = 'report_mnogo_people'
mail = 'IVAbdulganiev@yanao.ru'
table = 'uszn.temp$_mnogo_people'
file_sql = 'report_mnogo_people.sql'

goto_folder()

report_temp_table(name_log, mail, table, file_sql)
