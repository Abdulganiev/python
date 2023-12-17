from generating_report_files import *

#***************************************************************
name_log = 'duplicates_on_payment'
name_def = 'Дубликаты по выплате'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
check = 0

#***************************************************************
def duplicates_on_payment():
    with open('duplicates_on_payment.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
def duplicates_on_payment_MO():
    with open('duplicates_on_payment_MO.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
try:
    curs = connect_oracle()
    writing_to_log_file(name_log, f'Подключение к базе')
    check = 0
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)
    check = 1

if check == 0:
    try:
        mo = duplicates_on_payment_MO()
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции duplicates_on_payment_MO() - {e}'
        alarm_log(mail, name_log, text)
        check = 1

if check == 0:
    try:
        d = duplicates_on_payment()
    except Exception as e:
        text = f'произошла ошибка при вызове функции duplicates_on_payment() - {e}'
        alarm_log(mail, name_log, text)    

if check == 0:
    data = {
         'name' : [],
         'МО' : [],
         'УСЗН' : [],
         'Описание человека' : [],
         'Выплата' : [],
         'СНИЛС' : []
        }

    for region in mo:
        dt = datetime.now().strftime('%m.%Y')
        name = f'0{region[0]} - дубликаты получателей по виду выплаты на дату 01.{dt}'
        for row in d:
            data['name'].append(name)
            data['МО'].append(row[0])
            data['УСЗН'].append(row[1])
            data['Описание человека'].append(row[2])
            data['Выплата'].append(row[3])
            data['СНИЛС'].append(row[4])

    generating_report_files(data, name_log, name_def, test, mail)
