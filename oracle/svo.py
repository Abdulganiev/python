from generating_report_files import *

# *****************************************************************
log = 'report_GKV_YANAO'
test = 0
name_def = f'Отчет СВО'
name_log = 'svo'
mail = 'IVAbdulganiev@yanao.ru'
table = 'uszn.temp$_svo'
check = 0

# *****************************************************************
goto_folder()

try:
    curs = connect_oracle()
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

# *****************************************************************
def svo_create():
    with open('svo.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    # writing_to_log_file(name_log, sql)
    curs.execute(sql)

# *****************************************************************
def svo_drop():
    curs.execute(f'DROP TABLE {table}')

# *****************************************************************
def svo_cnt():
    curs.execute(f'SELECT count(*) FROM {table}')
    return curs.fetchall()[0][0]

# *****************************************************************
def svo_view():
    with open('svo_view.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

# *****************************************************************
writing_to_log_file(name_log, f' ')
writing_to_log_file(name_log, f'******старт***********************************')

try:
    curs = connect_oracle()
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    cnt = svo_cnt()
    writing_to_log_file(name_log, f'Количество строк в таблице {table} до начала - {cnt}')
except Exception as e:    
    text = f'произошла ошибка при вызове функции svo_cnt() - {e}'
    alarm_log(mail, name_log, text)

try:
    svo_drop()
    writing_to_log_file(name_log, f'Удаление таблицы {table}')
except Exception as e:    
    text = f'произошла ошибка при вызове функции svo_drop() - {e}'
    writing_to_log_file(name_log, text)

try:
    svo_create()
    writing_to_log_file(name_log, f'Создание таблицы {table}')
    check = 0
except Exception as e:    
    text = f'произошла ошибка при вызове функции svo_create() - {e}'
    alarm_log(mail, name_log, text)
    check = 1

try:
    cnt = svo_cnt()
    writing_to_log_file(name_log, f'Количество строк в таблице {table} после окончания - {cnt}')
except Exception as e:    
    text = f'произошла ошибка при вызове функции svo_cnt() - {e}'
    alarm_log(mail, name_log, text)


if check == 0:
    try:
        svo_view()
        writing_to_log_file(name_log, f'Пересоздание view')
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции svo_view() - {e}'
        alarm_log(mail, name_log, text)
        check = 1

writing_to_log_file(name_log, f'******конец***********************************')