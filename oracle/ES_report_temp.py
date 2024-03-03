from generating_report_files import *

#***************************************************************
name_log = 'ES_report_temp'
name_def = 'Временная таблица для отчета ЭС'
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def ES_report_temp_drop():
    try:
        #curs.execute('delete from uszn.temp$_ecert_report')
        curs.execute('drop table uszn.temp$_ecert_report')
    except Exception as e:
        text = f'произошла ошибка при delete from uszn.temp$_ecert_report - {e}'
        alarm_log(mail, name_log, text)

#***************************************************************
def ES_report_temp_create():
    try:
        #curs.execute('insert into uszn.temp$_ecert_report select * from uszn.temp$_v_ecert')
        curs.execute('create table uszn.temp$_ecert_report as select * from uszn.temp$_v_ecert')
    except Exception as e:
        text = f'произошла ошибка при insert into uszn.temp$_ecert_report - {e}'
        alarm_log(mail, name_log, text)

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
    writing_to_log_file(name_log, f'Запуск скрипта ES_report_temp_drop')
    ES_report_temp_drop()
    writing_to_log_file(name_log, f'Скрипт отработан ES_report_temp_drop')
except Exception as e:
    text = f'произошла ошибка при вызове функции ES_report_temp_drop - {e}'
    alarm_log(mail, name_log, text)

#***************************************************************
try:
    writing_to_log_file(name_log, f'Запуск скрипта ES_report_temp_create')
    ES_report_temp_create()
    writing_to_log_file(name_log, f'Скрипт отработан ES_report_temp_create')
except Exception as e:
    text = f'произошла ошибка при вызове функции ES_report_temp_create - {e}'
    alarm_log(mail, name_log, text)