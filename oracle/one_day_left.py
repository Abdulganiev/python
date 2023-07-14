from generating_report_files import *

#***************************************************************
name_log = 'one_day_left'
name_def = 'Гос_услуги - остался 1 день'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def one_day_left():
    with open('one_day_left.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

    data = {
         'name' : [],
         'Организация' : [],
         'id человека' : [],
         'Описание заявителя' : [],
         'Id обращения' : [],
         'Id документа заявления' : [],
         'Гос_услуга вариант оказания' : [],
         'Гос_услуга наименование' : [],
         'Откуда пришло заявление' : [],
         'Дата регистрации' : [],
         'Контроль' : [],
         'План в календарных днях' : [],
         'Факт в календарных днях' : [],
         'План в рабочих днях' : [],
         'Факт в рабочих днях' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['Организация'].append(row[1])
        data['id человека'].append(row[2])
        data['Описание заявителя'].append(row[3])
        data['Id обращения'].append(row[4])
        data['Id документа заявления'].append(row[5])
        data['Гос_услуга вариант оказания'].append(row[6])
        data['Гос_услуга наименование'].append(row[7])
        data['Откуда пришло заявление'].append(row[8])
        data['Дата регистрации'].append(row[9])
        data['Контроль'].append(row[10])
        data['План в календарных днях'].append(row[11])
        data['Факт в календарных днях'].append(row[12])
        data['План в рабочих днях'].append(row[13])
        data['Факт в рабочих днях'].append(row[13])
    
    return data

#***************************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    data = one_day_left()
except Exception as e:
    text = f'произошла ошибка при вызове функции one_day_left() - {e}'
    alarm_log(mail, name_log, text)

generating_report_files(data, name_log, name_def, test, mail)
