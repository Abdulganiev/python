from generating_report_files import *
import pandas as pd

# *****************************************************************
name_def = 'unlock_user_iszn'
name_log = 'unlock_user_iszn'
mail = 'IVAbdulganiev@yanao.ru'
alarm_flag = 0

# *****************************************************************
def unlock_user_iszn_find():
    with open('unlock_user_iszn_find.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

# *****************************************************************
def unlock_user_iszn_unlock(d):
    for sql in data.itertuples(index=False):
        writing_to_log_file(name_log, sql[0])
        curs.execute(sql[0])
    
# *****************************************************************
goto_folder()

try:
    curs = connect_oracle()
    alarm_flag = 0
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)
    alarm_flag = 1


if alarm_flag == 0:
    try:
        user_lock = unlock_user_iszn_find()
        alarm_flag = 0
    except Exception as e:    
        text = f'произошла ошибка при вызове функции unlock_user_iszn_find() - {e}'
        alarm_log(mail, name_log, text)
        alarm_flag = 1

if alarm_flag == 0:
    data = pd.DataFrame(user_lock)

    if len(data) > 0:
        try:
            unlock_user_iszn_unlock(data)
        except Exception as e:    
            text = f'произошла ошибка при вызове функции unlock_user_iszn_unlock() - {e}'
            alarm_log(mail, name_log, text)
