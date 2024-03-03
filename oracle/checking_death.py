from generating_report_files import *
import pandas as pd

#***************************************************************
name_log = 'checking_death'
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
goto_folder()

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

#***************************************************************
def find_doc(curs):
    with open('checking_death_find.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

def processing(curs, region_id, id):
    with open('checking_death_preliminary.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{region_id}', f'{region_id}')
    sql = sql.replace('{id}', f'{id}')
    curs.execute(sql)

    with open('checking_death_check.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)    
    
    cnt = int(curs.fetchall()[0][0])

    if cnt == 1:
        writing_to_log_file(name_log, f'нашли запись')
        with open('checking_death_out.sql', 'r', encoding='utf8') as f:
            sql = f.read()
        curs.execute(sql)
        data = curs.fetchall()
        writing_to_log_file(name_log, f'{data}')
        report_death(data, region_id, id)

#***************************************************************

writing_to_log_file(name_log, f'***************************************************************')
writing_to_log_file(name_log, f'Проверка началась')

try:
    data = pd.DataFrame(find_doc(curs))
except Exception as e:
    text = f'произошла ошибка при вызове функции find_doc() - {e}'
    alarm_log(mail, name_log, text)

for row in data.itertuples(index=False):
    try:
        processing(curs, row[0], row[1])
    except Exception as e:    
        text = f'произошла ошибка при вызове функции processing() - {e}'
        alarm_log(mail, name_log, text)    

writing_to_log_file(name_log, f'Проверка завершилась')