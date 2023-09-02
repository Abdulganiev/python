from generating_report_files import *
import pandas as pd

#***************************************************************
name_log = 'check_RSD_works'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'РСД работает по данным СФР'
check = 0

#***************************************************************
def check_RSD_works_category(curs):
    with open('check_RSD_works_category.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return 0

#***************************************************************
def check_RSD_works(curs):
    with open('check_RSD_works.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    data = {
         'id района' : [],
         'name' : [] ,
         'Наименование района' : [],
         'id человека' : [] ,
         'ФИО др' : [] ,
            }
    for row in curs.fetchall():
        data['id района'].append(row[0])
        data['name'].append(row[1])
        data['Наименование района'].append(row[2])
        data['id человека'].append(row[3])
        data['ФИО др'].append(row[4])
    return data

#***************************************************************
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
        check_RSD_works_category(curs)
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_RSD_works_category() - {e}'
        alarm_log(mail, name_log, text)
        check = 1

if check == 0:
    try:
        data = pd.DataFrame(check_RSD_works(curs))
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_RSD_works() - {e}'
        alarm_log(mail, name_log, text)
        check = 1
    
    if check == 0:
        writing_to_log_file(name_log, f'Количество записей - {len(data)}')
    
        for mo in sorted(set(data['name'])):
            cnt = data[data['name'].isin([mo])].count()[0]
            text = f'{mo} - {cnt} строк'
            writing_to_log_file(name_log, text)
            
        generating_report_files(data, name_log, name_def, test, mail)