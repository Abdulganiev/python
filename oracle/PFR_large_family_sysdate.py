import datetime as dt
from generating_report_files import *

#***************************************************************
name_log = 'PFR_large_family_sysdate'
dt = datetime.now().strftime('%d')
name_def = f'DSZN_030_{dt}-' 
test = 0
mail = 'IVAbdulganiev@yanao.ru'
cnt_curs = 0
cnt_data = 0

#***************************************************************
def PFR_large_family_sysdate():
    with open('PFR_large_family_sysdate.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

    data = {
         '№ п.п' : [],
         'ФИО и дата рождения матери' : [] ,
         'СНИЛС матери' : [] ,
         'ФИО и дата рождения отца' : [] ,
         'СНИЛС отца' : [] ,
         'Данные о детях' : [] ,
         'Статус "Многодетная"' : [] ,
         'Дата присвоения статуса "Многодетная"' : [] ,
        }
    
    for row in curs.fetchall():
        data['№ п.п'].append(row[0])
        data['ФИО и дата рождения матери'].append(row[1])
        data['СНИЛС матери'].append(row[2])
        data['ФИО и дата рождения отца'].append(row[3])
        data['СНИЛС отца'].append(row[4])
        data['Данные о детях'].append(row[5])
        data['Статус "Многодетная"'].append(row[6])
        data['Дата присвоения статуса "Многодетная"'].append(row[7])

    return data

#***************************************************************
writing_to_log_file(name_log, '***********************************')

try:
    curs = connect_oracle()
except Exception as e:
    writing_to_log_file(name_log, f'ошибка подключения к базе \n {e}')
else:
    writing_to_log_file(name_log, 'К базе подключился')
    cnt_curs = 1

if cnt_curs == 1:
    try:
        data = PFR_large_family_sysdate()
    except Exception as e:
        writing_to_log_file(name_log, f'ошибка функции PFR_large_family_sysdate \n {e}')
else:
    cnt_curs = 1

if cnt_curs == 1:
    try:
        generating_report_files_PFR(data, name_log, name_def, test, mail)
    except Exception as e:
        writing_to_log_file(name_log, f'ошибка функции generating_report_files_PFR \n {e}')