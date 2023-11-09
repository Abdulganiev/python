from generating_report_files import *

#***************************************************************
name_log = 'check_svo_category'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'Перерасчет категорий СВО'
check = 1

#***************************************************************
def check_svo_category(curs):
    with open('check_svo_category.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

#***************************************************************
writing_to_log_file(name_log, f'************************start***************************************')
try:
    curs = connect_oracle()
    check = 0
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)
    check = 1

if check == 0:
    try:
        check_svo_category(curs)
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_svo_category() - {e}'
        alarm_log(mail, name_log, text)
        check = 1
writing_to_log_file(name_log, f'************************end****************************************')