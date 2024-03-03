from generating_report_files import *
import pandas as pd

#***************************************************************
name_log = 'check_duble_EK'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'Несколько ЕКЖЯ у одного'
check = 0

#***************************************************************
def check_duble_EK(curs):
    with open('check_duble_EK.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
def check_duble_EK_MO(curs):
    with open('check_duble_EK_MO.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

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
        mo = check_duble_EK_MO(curs)
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_duble_EK_MO() - {e}'
        alarm_log(mail, name_log, text)
        check = 1

if check == 0 and len(mo) > 0:
    try:
        d = check_duble_EK(curs)
        data = {
             'id района' : [],
             'name' : [] ,
             'Наименование района' : [],
             'id человека' : [] ,
             'ФИО др' : [] ,
             'СНИЛС' : [] ,
                }

        for region in mo:
            name = f'0{region[0]} - Несколько ЕКЖЯ у одного'
            for row in d:
                data['name'].append(name)
                data['id района'].append(row[0])
                data['Наименование района'].append(row[1])
                data['id человека'].append(row[2])
                data['ФИО др'].append(row[3])
                data['СНИЛС'].append(row[4])

        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_duble_EK() - {e}'
        alarm_log(mail, name_log, text)
        check = 1
    
if check == 0 and len(mo) > 0:
    generating_report_files(data, name_log, name_def, test, mail)