import psycopg2, json
import pandas as pd
from sqlalchemy import create_engine
from generating_report_files import connect_oracle, writing_to_log_file
from generating_report_files import alarm_log
from generating_report_files import goto_folder

# *****************************************************************
goto_folder()

# *****************************************************************
def cnt_postgre(table_postgree, name_log, name_def, mail = 'IVAbdulganiev@yanao.ru'):
    
    #***************************************************************
    try:
        conn_postgre = connect_postgre()
        curs_postgree = conn_postgre.cursor()
    except Exception as e:
        text = f'произошла ошибка при вызове функции connect_postgre() - {e}'
        alarm_log(mail, name_log, text)

    #***************************************************************
    try:
        curs_postgree.execute(f'select count(*) FROM {table_postgree}')
        cnt = curs_postgree.fetchall()[0][0]
    except Exception as e:
        cnt = f'таблицы {table_postgree} нету - {e}'

    curs_postgree.close()
    conn_postgre.close()

    writing_to_log_file(name_log, f'Количество строк в {table_postgree} - {cnt}')


# *****************************************************************
def connect_postgre():
    mail = f'IVAbdulganiev@yanao.ru, 300195@mail.ru'
    name_log = 'access_postgre'
    connection = None

    #***************************************************************
    path = f'access_postgre.txt'
    with open(path) as f:
        access = json.load(f)
    
    host = access['path_base']
    password = access['password']
    user = access['login']
    port = access['port']
    database = access['sid']

    try:
        connection = psycopg2.connect(user = user,
            password = password,
            host = host,
            port = port,
            database = database)
        
    except OperationalError as e:
        text = f'произошла ошибка при вызове функции access_postgre - {e}'
        alarm_log(mail, name_log, text)

    return connection

# *****************************************************************
def load_postgre(table_oracle, table_postgree, name_log, name_def, mail = f'IVAbdulganiev@yanao.ru, 300195@mail.ru'):
    # *****************************************************************
    flag_alarm = 0

    # *****************************************************************
    writing_to_log_file(name_log, f'*************start*************')

    # *****************************************************************
    if flag_alarm == 0:
        try:
            curs = connect_oracle()
            writing_to_log_file(name_log, f'подключение к ГИС ЭСРН')
            flag_alarm = 0
        except Exception as e:    
            text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
            alarm_log(mail, name_log, text)
            flag_alarm = 1

    # *****************************************************************
    if flag_alarm == 0:
        try:
            col_table_oracle = table_oracle.replace('uszn.', '').upper() 
            curs.execute(f"SELECT uszn.StrCommaConcat(column_name) FROM DBA_TAB_COLS WHERE upper(table_name) = '{col_table_oracle}' order by column_id")
            col_oracle = curs.fetchall()[0][0]
            col = col_oracle.split(',')
            writing_to_log_file(name_log, f'Забрали из ГИС ЭСРН наименование столбцов из {col_table_oracle}')
            flag_alarm = 0
        except Exception as e:    
            text = f'произошла ошибка при наименование столбцов из {col_table_oracle} - {e}'
            alarm_log(mail, name_log, text)
            flag_alarm = 1

    if flag_alarm == 0:
        try:
            curs.execute(f'select {col_oracle} FROM {table_oracle}')
            writing_to_log_file(name_log, f'Забрали из ГИС ЭСРН данные из {table_oracle}')
            flag_alarm = 0
        except Exception as e:    
            text = f'произошла ошибка при select * FROM {table_oracle} - {e}'
            alarm_log(mail, name_log, text)
            flag_alarm = 1

    if flag_alarm == 0:
        try:
            data = pd.DataFrame(curs.fetchall())
            writing_to_log_file(name_log, f'Загрузили данные датафрейм')
            flag_alarm = 0
        except Exception as e:    
            text = f'произошла ошибка при select * FROM {table_oracle} - {e}'
            alarm_log(mail, name_log, text)
            flag_alarm = 1
    
    if flag_alarm == 0:
        try:        
            data.columns = col
            writing_to_log_file(name_log, f'Переименовали столбцы датафрейма')
            flag_alarm = 0
        except Exception as e:    
            text = f'произошла ошибка при select * FROM {table_oracle} - {e}'
            alarm_log(mail, name_log, text)
            flag_alarm = 1

        if flag_alarm == 0:
            cnt_postgre(table_postgree, name_log, name_def)

    # *****************************************************************
    path = f'access_postgre.txt'
    with open(path) as f:
        access = json.load(f)
    
    host = access['path_base']
    password = access['password']
    user = access['login']
    port = access['port']
    database = access['sid']
    
    #***************************************************************
    if flag_alarm == 0:
        try:
            conn_engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
            writing_to_log_file(name_log, f'Подключение к витрине {host}')
            flag_alarm = 0
        except Exception as e:
            text = f'произошла ошибка при вызове функции conn_engine() - {e}'
            alarm_log(mail, name_log, text)
            flag_alarm = 1

    if flag_alarm == 0:
        try:
            data.to_sql(table_postgree, con = conn_engine, if_exists='replace', index=False)
            writing_to_log_file(name_log, f'Загрузка данных в {table_postgree}')
            flag_alarm = 0
        except Exception as e:
            text = f'произошла ошибка при вызове функции to_sql() - {e}'
            alarm_log(mail, name_log, text)
            flag_alarm = 1

    if flag_alarm == 0:
        cnt_postgre(table_postgree, name_log, name_def) 

    writing_to_log_file(name_log, f'*************end')