from generating_report_files import *

#***************************************************************
name_log = 'duplicates_on_payment'
name_def = 'Дубликаты по выплате'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def duplicates_on_payment():
    with open('duplicates_on_payment.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

writing_to_log_file(name_log, f'Подключение к базе')

try:
    d = duplicates_on_payment()
except Exception as e:
    text = f'произошла ошибка при вызове функции duplicates_on_payment() - {e}'
    alarm_log(mail, name_log, text)    

data = {
     'name' : [],
     'МО' : [],
     'УСЗН' : [],
     'Описание человека' : [],
     'Выплата' : [],
     'СНИЛС' : []
    }

for region in range(58, 71):
    dt = datetime.now().strftime('%m.%Y')
    name = f'0{region} - дубликаты получателей по виду выплаты на дату 01.{dt}'
    for row in d:
        data['name'].append(name)
        data['МО'].append(row[0])
        data['УСЗН'].append(row[1])
        data['Описание человека'].append(row[2])
        data['Выплата'].append(row[3])
        data['СНИЛС'].append(row[4])

generating_report_files(data, name_log, name_def, test, mail)
