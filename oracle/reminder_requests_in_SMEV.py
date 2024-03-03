from generating_report_files import *

#***************************************************************
name_log = 'reminder_requests_in_SMEV'
name_def = 'Запросы в СМЭВ для переходников на 3-7'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def reminder_requests_in_SMEV():
    with open('reminder_requests_in_SMEV.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

    data = {
         'name' : [],
         'ID человека' : [],
         'Описание' : [],
         'ID коллектива' : [],
         'ID ребенка' : [],
         'ID получателя' : [],
         'Какой запрос необходимо сделать' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['ID человека'].append(row[1])
        data['Описание'].append(row[2])
        data['ID коллектива'].append(row[3])
        data['ID ребенка'].append(row[4])
        data['ID получателя'].append(row[5])
        data['Какой запрос необходимо сделать'].append(row[6])
    
    return data

#***************************************************************
goto_folder()

try:
  curs = connect_oracle()
except Exception as e:
  text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
  alarm_log(mail, name_log, text)

try:
  data = reminder_requests_in_SMEV()
except Exception as e:
  text = f'произошла ошибка при вызове функции reminder_requests_in_SMEV() - {e}'
  alarm_log(mail, name_log, text)

generating_report_files(data, name_log, name_def, test, mail)
