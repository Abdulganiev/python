from generating_report_files import *

#***************************************************************
name_log = 'category_large_family'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'Перерасчет категорий многодетные'
check = 1

#***************************************************************
def category_large_family(curs, region_id):
    with open('category_large_family.sql', 'r', encoding='utf8') as f:
        sql = f.read()
        sql = sql.replace('{region_id}', f'{region_id}')
    curs.execute(sql)

#***************************************************************
def category_large_family_member(curs, region_id):
    with open('category_large_family_member.sql', 'r', encoding='utf8') as f:
        sql = f.read()
        sql = sql.replace('{region_id}', f'{region_id}')
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
    for region_id in range(58, 71):
    # for region_id in range(59, 60):
        try:
            writing_to_log_file(name_log, f'category_large_family region_id {region_id} - start')
            category_large_family(curs, region_id)
            writing_to_log_file(name_log, f'category_large_family region_id {region_id} - end')
        except Exception as e:
            text = f'произошла ошибка при вызове функции category_large_family() - {e}'
            alarm_log(mail, name_log, text)

        try:
            writing_to_log_file(name_log, f'category_large_family_member region_id {region_id} - start')
            category_large_family_member(curs, region_id)
            writing_to_log_file(name_log, f'category_large_family_member region_id {region_id} - end')
        except Exception as e:
            text = f'произошла ошибка при вызове функции category_large_family_member() - {e}'
            alarm_log(mail, name_log, text)
        
writing_to_log_file(name_log, f'************************end****************************************')