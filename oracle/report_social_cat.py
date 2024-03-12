from generating_report_files import *

name_log = 'report_social_cat'
mail = 'IVAbdulganiev@yanao.ru'
table = 'uszn.temp$_r_social_categories'
file_sql = 'report_social_cat.sql'
 
goto_folder()

report_temp_table(name_log, mail, table, file_sql)
