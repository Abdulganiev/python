from generating_report_files import *
import pandas as pd

#***************************************************************
name_log = '1-GMU'
mail = 'IVAbdulganiev@yanao.ru, AVShashkov@yanao.ru' 
# mail = 'IVAbdulganiev@yanao.ru' 
path_backup = r'd:/python/schedule/backup/GMU/'
test = 0

#***************************************************************
try:
    curs = connect_oracle()
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)    

#***************************************************************
def file_gu(id):
    with open('1-GMU-file.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{SERVICE}', f'{id}')
    curs.execute(sql)
    file_name = curs.fetchall()[0][0] + '.xlsx'
    file_name = file_name.replace('"', '')
    
    return file_name

#***************************************************************  
def find_gu():
    with open('1-GMU-find.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    df = curs.fetchall()
    return df

#***************************************************************
def out_gu(id):
    with open('1-GMU-pred.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{SERVICE}', f'{id}')
    curs.execute(sql)
    
    with open('1-GMU-out.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    data = pd.DataFrame(curs.fetchall())
    
    return data

#***************************************************************
def fact_gu(id):
    with open('1-GMU-pred_fact.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{SERVICE}', f'{id}')
    curs.execute(sql)
    
    with open('1-GMU-out_fact.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    data = pd.DataFrame(curs.fetchall())
    
    return data
    
#***************************************************************
def file_gu_all():
    with open('1-GMU-file_all.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    file_name = curs.fetchall()[0][0] + '.xlsx'

    return file_name

#***************************************************************
def out_gu_all():
    with open('1-GMU-pred_all.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    with open('1-GMU-out.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    data = pd.DataFrame(curs.fetchall())
    
    return data

#***************************************************************
def fact_gu_all():
    with open('1-GMU-pred_all_fact.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    with open('1-GMU-out_fact.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    data = pd.DataFrame(curs.fetchall())
    
    return data

#***************************************************************
writing_to_log_file(name_log, f'***************************************************************')

try:
    data_find = pd.DataFrame(find_gu())
except Exception as e:
    text = f'произошла ошибка при вызове функции data_find() - {e}'
    alarm_log(mail, name_log, text)

for row in data_find.itertuples(index=False):
    try:
        file_name = file_gu(row[0])
    except Exception as e:
        text = f'произошла ошибка при вызове функции file_gu() - {e}'
        alarm_log(mail, name_log, text)

    try:
        df_1 = out_gu(row[0])
    except Exception as e:
        text = f'произошла ошибка при вызове функции out_gu() - {e}'
        alarm_log(mail, name_log, text)

    try:
        df_2 = fact_gu(row[0])
    except Exception as e:
        text = f'произошла ошибка при вызове функции fact_gu() - {e}'
        alarm_log(mail, name_log, text)

    try:
        data = pd.concat([df_1, df_2], ignore_index=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции pd.concat([df_1, df_2]) - {e}'
        alarm_log(mail, name_log, text)

    try:        
        report_1gmu(data, file_name, mail, name_log, test, path_backup)
    except Exception as e:
        text = f'произошла ошибка при вызове функции report_1gmu() - {e}'
        alarm_log(mail, name_log, text)

try:
    file_name = file_gu_all()
    df_1 = out_gu_all()
    df_2 = fact_gu_all()
    data = pd.concat([df_1, df_2], ignore_index=True)
    report_1gmu(data, file_name, mail, name_log, test, path_backup)
except Exception as e:
    text = f'произошла ошибка при вызове функции out_gu_all() - {e}'
    alarm_log(mail, name_log, text)
