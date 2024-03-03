from generating_report_files import *

#***************************************************************
name_log = 'ES_new_MIR'
name_def = 'Привязка нового номера карты к ЭС'
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def ES_new_MIR():
    with open('ES_new_MIR.sql', 'r', encoding='utf8') as f:
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

try:
    writing_to_log_file(name_log, f'Запуск скрипта')
    d = ES_new_MIR()
    writing_to_log_file(name_log, f'Скрипт отработан')
    cnt = len(d)
    writing_to_log_file(name_log, f'Подлежит обработке {cnt} записей')
except Exception as e:
    text = f'произошла ошибка при вызове функции ES_new_MIR - {e}'
    alarm_log(mail, name_log, text)

if cnt > 0:
    for row in d:
        try:
            writing_to_log_file(name_log, f'Обработка {row[0]} записи')
            curs.execute(row[0])
            writing_to_log_file(name_log, f'Запись {row[0]} обработана')
        except:
            text = f'произошла ошибка при обратке запроса {row[0]} - {e}'
            alarm_log(mail, name_log, text)
        
writing_to_log_file(name_log, f'Обработано {cnt} записей')
