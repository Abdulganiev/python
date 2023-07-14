from generating_report_files import *

#***************************************************************
name_log = 'not_correct_to_assign'
name_def = 'МСП с неправильным сроком назначения'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def not_correct_to_assign():
    with open('not_correct_to_assign.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    data = {
         'name' : [],
         'МО' : [],
         'ID человека' : [],
         'Описание субъекта назначения' : [],
         'Вид выплаты' : [],
         'Дата ПО' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['МО'].append(row[1])
        data['ID человека'].append(row[2])
        data['Описание субъекта назначения'].append(row[3])
        data['Вид выплаты'].append(row[4])
        data['Дата ПО'].append(row[5])
        
    return data

#***************************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    data = not_correct_to_assign()
except Exception as e:
    text = f'произошла ошибка при вызове функции not_correct_to_assign() - {e}'
    alarm_log(mail, name_log, text)

generating_report_files(data, name_log, name_def, test, mail)

