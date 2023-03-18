from generating_report_files import *

#***************************************************************
curs = connect_oracle()

#***************************************************************

def debtors_GKH():
    with open('debtors_GKH.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    data = {
         'id района' : [],
         'name' : [] ,
         'id человека' : [] ,
         'id заявления' : [] ,
         'СНИЛС' : [] ,
         'Адрес из запроса' : [] ,
         'ФИО из запроса' : [] ,
         'ФИО из ответа' : [] ,
         'Организация' : [] ,
         'Организация телефон' : []
        }
    
    for row in curs.fetchall():
        data['id района'].append(row[0])
        data['name'].append(row[1])
        data['id человека'].append(row[2])
        data['id заявления'].append(row[3])
        data['СНИЛС'].append(row[4])
        data['Адрес из запроса'].append(row[5])
        data['ФИО из запроса'].append(row[6])
        data['ФИО из ответа'].append(row[7])
        data['Организация'].append(row[8])
        data['Организация телефон'].append(row[9])
    
    return data

#***************************************************************

data = debtors_GKH()
name_log = 'debtors_GKH'
name_def = 'Должники ГИС ЖКХ'
test = 1
mail = 'IVAbdulganiev@yanao.ru'

generating_report_files(data, name_log, name_def, test, mail)
