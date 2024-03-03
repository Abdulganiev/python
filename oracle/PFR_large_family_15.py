from generating_report_files import *

#***************************************************************
name_log = 'PFR_large_family_15'
name_def = 'DSZN_030_15-'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def PFR_large_family_15():
    with open('PFR_large_family_01.sql', 'r', encoding='utf8') as f:
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
goto_folder()

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    data = PFR_large_family_15()
except Exception as e:
    text = f'произошла ошибка при вызове функции PFR_large_family_15() - {e}'
    alarm_log(mail, name_log, text)

generating_report_files_PFR(data, name_log, name_def, test, mail)
