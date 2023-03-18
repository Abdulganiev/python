from generating_report_files import *

#***************************************************************
name_log = 'EKJ_find_alarms_cnt.log'
mail = 'IVAbdulganiev@yanao.ru,300195@mail.ru'

#***************************************************************
def search_alarm():
    curs = connect_oracle()
    with open('EKJ_find_alarms_cnt.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    n = curs.fetchall()[0][0]
    curs.close()
    return n

def write_alarm(n):
    writing_to_log_file(name_log, '************************************************')
    text = f'ВНИМАНИЕ!!! Количество сбоев - {n}'
    writing_to_log_file(name_log, text)
    alarm_log(mail, name_log, text)

#***************************************************************
cnt = search_alarm()
# cnt = 1
if cnt > 0:
    write_alarm(cnt)