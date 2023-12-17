from generating_report_files import *
import pandas as pd

#***************************************************************
name_log = 'check_EPB'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'Дубликаты ЕПБ'
check = 0

#***************************************************************
def check_EPB(curs):
    with open('check_EPB.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
def check_EPB_MO(curs):
    with open('check_EPB_MO.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

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
        mo = check_EPB_MO(curs)
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_EPB_MO() - {e}'
        alarm_log(mail, name_log, text)
        check = 1

if check == 0:
    try:
        d = check_EPB(curs)
        data = {
             'id района' : [],
             'name' : [] ,
             'Наименование района' : [],
             'id человека' : [] ,
             'ФИО др' : [] ,
             'СНИЛС' : [] ,
                }

        for region in mo:
            name = f'0{region[0]} - дубликаты получателей ЕПБ'
            for row in d:
                data['name'].append(name)
                data['id района'].append(row[0])
                data['Наименование района'].append(row[1])
                data['id человека'].append(row[2])
                data['ФИО др'].append(row[3])
                data['СНИЛС'].append(row[4])

        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_EPB() - {e}'
        alarm_log(mail, name_log, text)
        check = 1
    
if check == 0:
    generating_report_files(data, name_log, name_def, test, mail)