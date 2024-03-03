from generating_report_files import *
from access_postgre import load_postgre

#***************************************************************
name_log = 'rsud_v_msk_all'
name_def = 'rsud_v_msk_all'
mail = 'IVAbdulganiev@yanao.ru'
table_postgree = 'temp$_v_msk_all'
table_oracle = 'uszn.temp$_v_msk_all'

#***************************************************************
goto_folder()

load_postgre(table_oracle, table_postgree, name_log, name_def, mail)