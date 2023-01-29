from generating_report_files import *
import pandas as pd

#***************************************************************
name_log = '1-GMU'
mail = 'IVAbdulganiev@yanao.ru, AVShashkov@yanao.ru' # AVShashkov@yanao.ru

#***************************************************************
try:
    curs = connect_oracle()
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)    

#***************************************************************
def out_gu(id):
    with open('1-GMU-pred.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{SERVICE}', f'{id}')
    curs.execute(sql)
    
    with open('1-GMU-file.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{SERVICE}', f'{id}')
    curs.execute(sql)
    file_name = curs.fetchall()[0][0] + '.xlsx'
    file_name = file_name.replace('"', '')
    
    with open('1-GMU-out.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    data = pd.DataFrame(curs.fetchall())    
    
    report_1gmu(data, file_name, mail, name_log)

#***************************************************************
def find_gu():
    with open('1-GMU-find.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    df = curs.fetchall()
    return df

#***************************************************************
writing_to_log_file(name_log, f'***************************************************************')

try:
    data_find = pd.DataFrame(find_gu())
except Exception as e:
    text = f'произошла ошибка при вызове функции find_gu() - {e}'
    alarm_log(mail, name_log, text)

for row in data_find.itertuples(index=False):
    try:
        out_gu(row[0])
    except Exception as e:
        text = f'произошла ошибка при вызове функции out_gu() - {e}'
        alarm_log(mail, name_log, text)
