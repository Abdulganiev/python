from generating_report_files import *

#**************************************************
name_log = 'present_check'
mail = 'IVAbdulganiev@yanao.ru'

#**************************************************
def present_check(curs):
    with open('present_check.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return int(curs.fetchall()[0][0])

#*********************************************
writing_to_log_file(name_log, '*******start*************************************')

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)    

try:
    cnt = present_check(curs)
    if cnt > 0:
        text = f'ВНИМАНИЕ !!! Появились рожденные - {cnt}'
        alarm_log(mail, name_log, text)
except Exception as e:    
    text = f'произошла ошибка при вызове функции present_check() - {e}'
    alarm_log(mail, name_log, text)    
