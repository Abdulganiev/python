from generating_report_files import report_temp_table

name_log = 'report_bi_svo'
mail = 'IVAbdulganiev@yanao.ru'
table = 'uszn.temp$_r_svo_kind'
file_sql = 'report_bi_svo.sql'
 
report_temp_table(name_log, mail, table, file_sql)
