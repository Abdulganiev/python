import os
from generating_report_files import *

#***************************************************************
name_log = 'lk_reconnecting'
name_def = 'lk_reconnecting'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def lk_reconnecting():
    with open('lk_reconnecting_1.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

    with open('lk_reconnecting_2.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    writing_to_log_file(name_log, 'скрипт отработан')

#***************************************************************
goto_folder()

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    lk_reconnecting()
except Exception as e:
    text = f'произошла ошибка при вызове функции lk_reconnecting() - {e}'
    alarm_log(mail, name_log, text)