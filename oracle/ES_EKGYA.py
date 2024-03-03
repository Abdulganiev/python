from generating_report_files import *

#***************************************************************
name_log = 'ES_EKGYA'
name_def = 'Изменился номер карты МИР для ЕКЖЯ для ЭС'
mail = 'IVAbdulganiev@yanao.ru'
test = 0

#***************************************************************
def ES_EKGYA():
    with open('ES_EKGYA.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
goto_folder()

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

writing_to_log_file(name_log, f'***************************************')
writing_to_log_file(name_log, f'Подключение к базе')

data = {
    'name' : [],
    'Наименование выплаты' : [],
    'id получателя' : [],
    'Описание получателя' : [],
    'id субъекта назначение' : [],
    'Описание субъекта назначение' : [],
    'Номер карты МИР привязанная к ЕКЖЯ (новая)' : [],
    'Старая карта МИР' : []
    }

try:
    d = ES_EKGYA()
    cnt = len(d)
except:
    text = f'произошла ошибка при вызове функции ES_EKGYA - {e}'
    alarm_log(mail, name_log, text)

if cnt > 0:
    for row in d:
        data['name'].append(row[0])
        data['Наименование выплаты'].append(row[1])
        data['id получателя'].append(row[2])
        data['Описание получателя'].append(row[3])
        data['id субъекта назначение'].append(row[4])
        data['Описание субъекта назначение'].append(row[5])
        data['Номер карты МИР привязанная к ЕКЖЯ (новая)'].append(row[6])
        data['Старая карта МИР'].append(row[7])

    generating_report_files(data, name_log, name_def, test, mail)