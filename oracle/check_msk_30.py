from generating_report_files import *

#***************************************************************
name_log = 'check_msk_30'
test = 0
mail = 'IVAbdulganiev@yanao.ru, olzpopova@yanao.ru'
name_def = 'Проверка ДУЛ на дату выдачи'
check = 0
msk = 0

#***************************************************************
def check_msk_30(curs):
    curs.execute('select count(1) from uszn.temp$_msk_cert')
    return curs.fetchall()[0][0]

#***************************************************************
goto_folder()

writing_to_log_file(name_log, f'***************************************************************')

try:
    curs = connect_oracle()
    check = 0
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)
    check = 1

if check == 0:
    try:
        msk = check_msk_30(curs)
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_dul_date() - {e}'
        alarm_log(mail, name_log, text)
        check = 1
    
    if msk >= 30000 and msk < 30100: 
        alarm_log(mail, '!!! ВНИМАНИЕ МСК выдали 30 000', f'{msk}')