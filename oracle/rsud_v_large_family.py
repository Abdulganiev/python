from generating_report_files import *
from access_postgre import load_postgre

#***************************************************************
name_log = 'rsud_v_large_family'
name_def = 'rsud_v_large_family'
mail = 'IVAbdulganiev@yanao.ru'
table_postgree = 'temp$_v_large_family'
table_oracle = 'uszn.temp$_v_large_family'

#***************************************************************
goto_folder()

load_postgre(table_oracle, table_postgree, name_log, name_def, mail)