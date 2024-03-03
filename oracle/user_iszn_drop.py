from generating_report_files import *
import pandas as pd

# *****************************************************************
name_def = 'user_iszn_drop'
name_log = 'user_iszn_drop'
mail = 'IVAbdulganiev@yanao.ru'
alarm_flag = 0

patchs = get_platform()
trek = patchs['trek']

# *****************************************************************
def user_iszn_drop():
    with open(f'{trek}/user_iszn_drop.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

# *****************************************************************
def drop_user_iszn_drop(d):
    for sql in data.itertuples(index=False):
        try:
            writing_to_log_file(name_log, sql[0])
            curs.execute(sql[0])
        except Exception as e:    
            text = f'произошла ошибка при вызове функции user_iszn_drop() - {e}'
            writing_to_log_file(name_log, text)
# *****************************************************************
writing_to_log_file(name_log, '***********start**************')

try:
    curs = connect_oracle()
    alarm_flag = 0
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    writing_to_log_file(name_log, text)
    alarm_flag = 1


if alarm_flag == 0:
    try:
        user_lock = user_iszn_drop()
        alarm_flag = 0
    except Exception as e:    
        text = f'произошла ошибка при вызове функции user_iszn_drop() - {e}'
        writing_to_log_file(name_log, text)
        alarm_flag = 1

if alarm_flag == 0:
    data = pd.DataFrame(user_lock)

    if len(data) > 0:
        drop_user_iszn_drop(data)

writing_to_log_file(name_log, '***********end**************')