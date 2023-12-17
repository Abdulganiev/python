from generating_report_files import *

#***************************************************************
name_log = 'category_svo'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'Перерасчет категорий СВО'
check = 1

#***************************************************************
def category_svo(curs):
    with open('category_svo.sql', 'r', encoding='utf8') as f:
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
        category_svo(curs)
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции category_svo() - {e}'
        alarm_log(mail, name_log, text)
        check = 1
writing_to_log_file(name_log, f'************************end****************************************')