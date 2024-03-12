from generating_report_files import *

#***************************************************************
name_log = 'ES_EKGYA_DO'
name_def = 'Изменился номер карты МИР для ЕКЖЯ для ЭС для ДО'
mail = 'IVAbdulganiev@yanao.ru'
test = 0
check = 0
cnt = 0

#***************************************************************
def ES_EKGYA_DO():
    with open('ES_EKGYA_DO.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
goto_folder()

writing_to_log_file(name_log, f'***********start***********************')

try:
    curs = connect_oracle()
    check = 0
    writing_to_log_file(name_log, f'Подключение к базе')
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)
    check = 1

try:
    data = pd.DataFrame(ES_EKGYA_DO())
    cnt = len(data)
    writing_to_log_file(name_log, f'количество строк для обработки - {cnt}')
    check = 0
except Exception as e:
    text = f'произошла ошибка при вызове функции ES_EKGYA_DO - {e}'
    alarm_log(mail, name_log, text)
    check = 1

if cnt > 0 and check == 0:
    try:
        col = ('name','Наименование выплаты','id получателя','Описание получателя','id субъекта назначение','Описание субъекта назначение','Номер карты МИР привязанная к ЕКЖЯ (новая)','Старая карта МИР')
        data.columns = col
        check = 0
    except Exception as e:
        text = f'произошла ошибка при переименовании столбцов - {e}'
        alarm_log(mail, name_log, text)
        check = 1

if cnt > 0 and check == 0:
    generating_report_files(data, name_log, name_def, test, mail, recipient='do')

writing_to_log_file(name_log, f'***********stop***********************')