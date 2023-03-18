from generating_report_files import *
import pandas as pd

#***************************************************************
name_log = 'not_snils'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'Нет СНИЛС'

#***************************************************************
def not_snils(curs):
    with open('not_snils.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    data = {
         'id района' : [],
         'name' : [] ,
         'Наименование района' : [],
         'id человека' : [] ,
         'ФИО др' : [] ,
         'Вид выплаты' : [] ,
            }
    for row in curs.fetchall():
        data['id района'].append(row[0])
        data['name'].append(row[1])
        data['Наименование района'].append(row[2])
        data['id человека'].append(row[3])
        data['ФИО др'].append(row[4])
        data['Вид выплаты'].append(row[5])

    return data

#***************************************************************

writing_to_log_file(name_log, f'***************************************************************')
try:
    curs = connect_oracle()
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    data = pd.DataFrame(not_snils(curs))
except Exception as e:
    text = f'произошла ошибка при вызове функции not_snils() - {e}'
    alarm_log(mail, name_log, text)

writing_to_log_file(name_log, f'Количество записей - {len(data)}')

for mo in sorted(set(data['name'])):
    cnt = data[data['name'].isin([mo])].count()[0]
    text = f'{mo} - {cnt} строк'
    writing_to_log_file(name_log, text)
    
generating_report_files(data, name_log, name_def, test, mail)