from generating_report_files import *

#***************************************************************
name_log = 'category_pfr_trud'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'Перерасчет категорий ПФР труд'
check = 1

#***************************************************************
def category_pfr_trud(curs):
    with open('category_pfr_trud.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

#***************************************************************
goto_folder()

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
        category_pfr_trud(curs)
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции category_pfr_trud() - {e}'
        alarm_log(mail, name_log, text)
        check = 1
writing_to_log_file(name_log, f'************************end****************************************')