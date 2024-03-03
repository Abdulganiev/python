from generating_report_files import *

#***************************************************************
name_log = 'not_processed_3_days'
name_def = 'Гос_услуги необработанные более 3 дней'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def not_processed_3_days():
    with open('not_processed_3_days.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    data = {
         'name' : [],
         'ID человека' : [],
         'Описание человека' : [],
         'ID заявления' : [],
         'Дата подачи' : [],
         'Гос_услуга' : [],
         'Статус' : [],
         'Откуда пришло заявление' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['ID человека'].append(row[1])
        data['Описание человека'].append(row[2])
        data['ID заявления'].append(row[3])
        data['Дата подачи'].append(row[4])
        data['Гос_услуга'].append(row[5])
        data['Статус'].append(row[6])
        data['Откуда пришло заявление'].append(row[7])

    return data

#***************************************************************
goto_folder()

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
  data = not_processed_3_days()
except Exception as e:
    text = f'произошла ошибка при вызове функции not_processed_3_days() - {e}'
    alarm_log(mail, name_log, text)

generating_report_files(data, name_log, name_def, test, mail)