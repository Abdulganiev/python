from generating_report_files import *
import pandas as pd

#***************************************************************
name_log = 'check_EPB'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'Дубликаты ЕПБ'
check = 0
range_ = range(58, 71)

#***************************************************************
def cnt_EPB(region):
    curs.execute(f'SELECT count(*) FROM uszn.temp$_r_EPB where region_id={region}')
    cnt = str(curs.fetchall()[0][0])
    return cnt

#***************************************************************
def ins_EPB(region):
    cnt = cnt_EPB(region)
    text = f'В {region} - {cnt} строк перед удалением'
    writing_to_log_file(name_log, text)

    curs.execute(f'DELETE FROM uszn.temp$_r_EPB where region_id={region}')

    cnt = cnt_EPB(region)
    text = f'В {region} - {cnt} строк после удалением'
    writing_to_log_file(name_log, text)

    with open('check_EPB_insert.sql', 'r', encoding='utf8') as f:
        sql = f.read()
        sql = sql.replace('{region}', f'{region}')
    curs.execute(sql) 

    cnt = cnt_EPB(region)
    text = f'В {region} - {cnt} строк после загрузки'
    writing_to_log_file(name_log, text)

#***************************************************************
def check_EPB():
    with open('check_EPB.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
def check_EPB_MO():
    with open('check_EPB_MO.sql', 'r', encoding='utf8') as f:
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
        for region in range_:
            ins_EPB(region)
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции ins_EPB() - {e}'
        alarm_log(mail, name_log, text)
        check = 1

if check == 0:
    try:
        mo = check_EPB_MO()
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_EPB_MO() - {e}'
        alarm_log(mail, name_log, text)
        check = 1

if check == 0:
    try:
        d = check_EPB()
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