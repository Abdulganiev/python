import datetime as dt
from generating_report_files import *

#***************************************************************
name_log = 'PFR_to_3'
dt = datetime.now().strftime('%d')
name_def = f'DSZN_na_3_{dt}-' 
test = 0
mail = 'IVAbdulganiev@yanao.ru'
cnt_curs = 0
cnt_data = 0

#***************************************************************
def PFR_to_3():
    with open('PFR_to_3.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

    data = {
         'Муниципальное образование' : [],
         'Вид выплаты' : [],
         'СНИЛС получателя' : [],
         'ФИО и дата рождения получателя' : [],
         'СНИЛС ребенка' : [],
         'ФИО и дата рождения ребенка' : [],
         'Дата назначения С' : [],
         'Дата назначения ПО' : [],
         'Последний месяц оплаты' : [],
        }
    
    for row in curs.fetchall():
         data['Муниципальное образование'].append(row[0])
         data['Вид выплаты'].append(row[1])
         data['СНИЛС получателя'].append(row[2])
         data['ФИО и дата рождения получателя'].append(row[3])
         data['СНИЛС ребенка'].append(row[4])
         data['ФИО и дата рождения ребенка'].append(row[5])
         data['Дата назначения С'].append(row[6])
         data['Дата назначения ПО'].append(row[7])
         data['Последний месяц оплаты'].append(row[8])

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
        data = PFR_to_3()
    except Exception as e:
        writing_to_log_file(name_log, f'ошибка функции PFR_to_3 \n {e}')
else:
    cnt_curs = 1

if cnt_curs == 1:
    try:
        generating_report_files_PFR(data, name_log, name_def, test, mail)
    except Exception as e:
        writing_to_log_file(name_log, f'ошибка функции generating_report_files_PFR \n {e}')
