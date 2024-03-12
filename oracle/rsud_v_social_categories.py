from generating_report_files import *
from access_postgre import load_postgre

#***************************************************************
name_log = 'rsud_v_social_categories'
name_def = 'rsud_v_social_categories'
mail = 'IVAbdulganiev@yanao.ru'
table_postgree = 'temp$_v_social_categories'
table_oracle = 'uszn.temp$_v_social_categories'

#***************************************************************
goto_folder()

load_postgre(table_oracle, table_postgree, name_log, name_def, mail)