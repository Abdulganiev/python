from generating_report_files import *

#***************************************************************
name_log = 'no_INN'
name_def = 'Нет ИНН'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def no_INN():
    with open('no_INN.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    data = {
         'name' : [],
         'ID человека' : [],
         'Описание' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['ID человека'].append(row[1])
        data['Описание'].append(row[2])
    
    return data

#***************************************************************
goto_folder()

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    data = no_INN()
except Exception as e:
    text = f'произошла ошибка при вызове функции no_INN() - {e}'
    alarm_log(mail, name_log, text)

generating_report_files(data, name_log, name_def, test, mail)