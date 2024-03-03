from generating_report_files import *
import pandas as pd

#***************************************************************
name_log = 'check_RSD_to_uszn'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'РСД имеет право'
check = 0

#***************************************************************
def check_RSD_to_uszn(curs):
    with open('check_RSD_to_uszn.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    data = {
         'id района' : [],
         'name' : [] ,
         'Наименование района' : [],
         'id человека' : [] ,
         'СНИЛС' : [] ,
         'ФИО др' : [] ,
         'Дата выплат в УСЗН' : [] ,
         'Вид пенсии' : [] ,
         'Размер пенсии' : [] ,
         'Общий доход по выплатам в исзн' : [] ,
         'Размер прожиточного минимума' : [] ,
            }
    for row in curs.fetchall():
        data['id района'].append(row[0])
        data['name'].append(row[1])
        data['Наименование района'].append(row[2])
        data['id человека'].append(row[3])
        data['СНИЛС'].append(row[4])
        data['ФИО др'].append(row[5])
        data['Дата выплат в УСЗН'].append(row[6])
        data['Вид пенсии'].append(row[7])
        data['Размер пенсии'].append(row[8])
        data['Общий доход по выплатам в исзн'].append(row[9])
        data['Размер прожиточного минимума'].append(row[10])
    return data

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
        data = pd.DataFrame(check_RSD_to_uszn(curs))
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_RSD_to_uszn() - {e}'
        alarm_log(mail, name_log, text)
        check = 1
    
    if check == 0:
        writing_to_log_file(name_log, f'Количество записей - {len(data)}')
    
        for mo in sorted(set(data['name'])):
            cnt = data[data['name'].isin([mo])].count()[0]
            text = f'{mo} - {cnt} строк'
            writing_to_log_file(name_log, text)
            
        generating_report_files(data, name_log, name_def, test, mail)