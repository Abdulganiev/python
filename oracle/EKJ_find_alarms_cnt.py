from generating_report_files import *

#***************************************************************
name_log = 'EKJ_find_alarms_cnt.log'
mail = 'IVAbdulganiev@yanao.ru,300195@mail.ru'

#***************************************************************
def search_alarm():
    with open('EKJ_find_alarms_cnt.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    n = curs.fetchall()[0][0]
    return n

#***************************************************************
def write_alarm(n):
    writing_to_log_file(name_log, '************************************************')
    text = f'ВНИМАНИЕ!!! Количество сбоев - {n}'
    writing_to_log_file(name_log, text)
    alarm_log(mail, name_log, text)

#***************************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    cnt = search_alarm()
except Exception as e:
    text = f'произошла ошибка при вызове функции search_alarm() - {e}'
    alarm_log(mail, name_log, text)

if cnt > 0:
    try:
        write_alarm(cnt)
    except Exception as e:
        text = f'произошла ошибка при вызове функции write_alarm() - {e}'
        alarm_log(mail, name_log, text)
