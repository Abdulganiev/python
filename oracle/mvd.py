import pandas as pd
import os, re
import datetime as dt
from generating_report_files import *

#***************************************************************
name_log = 'mvd'
name_def = 'mvd'
mail = 'IVAbdulganiev@yanao.ru'
today = dt.date.today()
path_backup = r'd:/python/schedule/backup/mvd/'
path = r'd:/python/schedule/mvd/'
os.chdir(path)
test = 0
alarm_f = 0

#***************************************************************    
def mvd_insert_temp(xl):
    table = 'uszn.temp$_mvd_msp_temp'
    columns = '(' + ', '.join(list(xl)) + ')'
    question = 'values(' + ', '.join(list('?' * len(list(xl)))) + ')'
    sql = f'INSERT INTO {table} {columns} {question}'
    
    writing_to_log_file(name_log, f'Загрузка данных в {table}')
    writing_to_log_file(name_log, f'Количество записей в {table} перед загрузкой')
    table_cnt(table)
    
    for data in xl.itertuples(index=False):
        try:
            curs.execute(f'{sql}', list(data))
        except Exception as e:
            test_sql = list(data)
            text = f'произошла ошибка при вызове функции vk_insert_temp() - {e} {sql} {test_sql}'
            alarm_log(mail, name_log, text)
    
    writing_to_log_file(name_log, f'Количество записей в {table} после загрузки')
    table_cnt(table)

#***************************************************************
def pre_processing(xl, file):
    
    col = ['NOM', 'FAM', 'IMIA', 'OTH', 'DTR', 'MTR', 'SNILS', 'INN', 
            'DUL', 'DUL_SER', 'DULNOM', 'DTDOC', 'DOCV', 'KODP', 
            'NSP', 'UL', 'DOM', 'KORP', 'KV', 'DR', 'NMO', 
            'CAT', 'MONTH', 'DATE_START', 'DATE_STOP', 'RV', 
            'SBB', 'BIKB', 'LSH' ]

    xl.columns = col
    
    xl.dropna(thresh=21, inplace = True)

    for data in xl.itertuples():
        if pd.isna(data[1]):
            xl.drop(index=data[0], inplace = True)

    xl['DTR'] = xl['DTR'].apply(dat)
    xl['DTDOC'] = xl['DTDOC'].apply(dat)
    xl['DR'] = xl['DR'].apply(dat).apply(replace_nan).apply(replace_nat)
    xl['FAM'] = xl['FAM'].apply(up)
    xl['IMIA'] = xl['IMIA'].apply(up)
    xl['MTR'] = xl['MTR'].apply(num_int_to_str).apply(replace_nan).apply(replace_nat)
    xl['OTH'] = xl['OTH'].apply(up).apply(replace_nan).apply(replace_nat)
    xl['MONTH'] = xl['MONTH'].apply(dat)
    xl['DATE_START'] = xl['DATE_START'].apply(dat).apply(replace_nan).apply(replace_nat)
    xl['DATE_STOP'] = xl['DATE_STOP'].apply(dat).apply(replace_nan).apply(replace_nat)
    xl['DR'] = xl['DR'].apply(dat).apply(replace_nan).apply(replace_nat)
    xl['MO_ID'] = xl['NMO'].apply(mo_id)
    xl['DATE_LOAD'] = today
    xl['DATE_LOAD'] = xl['DATE_LOAD'].apply(dat)
    xl['FILE_LOAD'] = file
    
    xl['NOM'] = xl['NOM'].apply(num_int_to_str).apply(replace_nan).apply(replace_nat)
    xl['NSP'] = xl['NSP'].apply(replace_nan).apply(replace_nat)
    xl['UL'] = xl['UL'].apply(replace_nan).apply(replace_nat)
    xl['DOM'] = xl['DOM'].apply(num_int_to_str).apply(replace_nan).apply(replace_nat)
    xl['KORP'] = xl['KORP'].apply(num_int_to_str).apply(replace_nan).apply(replace_nat)
    xl['KV'] = xl['KV'].apply(num_int_to_str).apply(replace_nan).apply(replace_nat)
    
    xl = xl.fillna('')
    xl = xl.fillna(0)
    
    return xl

#*****************************************************
def del_kosyak():
    sql = "delete from uszn.temp$_mvd_msp_temp where snils='123-456-789 12'"
    curs.execute(sql)

#*****************************************************    
def del_temp():
    sql = "delete from uszn.temp$_mvd_msp_temp"
    curs.execute(sql)

#*****************************************************    
def table_drop(table):
    writing_to_log_file(name_log, f'Удаление таблицы {table}')
    try:
        sql = f'drop table {table}'
        curs.execute(sql)
        text = f'таблица {table} удалена'
    except Exception as e:
        text = f'таблицы {table} нету - {e}'
    writing_to_log_file(name_log, text)

#*****************************************************    
def table_cnt(table):
    try:
        sql = f'SELECT count(*) FROM {table}'
        curs.execute(sql)
        cnt = curs.fetchone()[0]
        text = f'Количество записей в {table} - {cnt}'
    except Exception as e:
        text = f'таблицы {table} нету - {e}'
    writing_to_log_file(name_log, text)
    
#*****************************************************    
def mvd_insert_all():
    table = 'uszn.temp$_mvd_msp_all'
    writing_to_log_file(name_log, f'Загрузка данных в {table}')
    writing_to_log_file(name_log, f'Количество записей в {table} перед загрузкой')
    table_cnt(table)
    
    sql = f'''INSERT INTO {table} 
              SELECT t1.*
              FROM uszn.temp$_mvd_msp_temp t1 LEFT JOIN {table} t2
                on replace(replace(t1.snils, '-', ''), ' ', '') = replace(replace(t2.snils, '-', ''), ' ', '') 
                   and t1.cat = t2.cat and t1.mo_id = t2.mo_id and t1.date_load = t2.date_load
                WHERE t2.date_load is null'''
    curs.execute(sql)
    writing_to_log_file(name_log, f'Количество записей в {table} после загрузки')
    table_cnt(table)  

#*****************************************************
def mvd_del():
    table = 'uszn.temp$_mvd_msp_del'
    writing_to_log_file(name_log, f'Загрузка данных в {table}')
    table_drop(table)
    
    sql=f'''
    create table {table} as
    select t1.*
    from uszn.temp$_mvd_msp t1 left join uszn.temp$_mvd_msp_temp t2
      on replace(replace(t1.snils, '-', ''), ' ', '') = replace(replace(t2.snils, '-', ''), ' ', '') 
         and t1.cat = t2.cat and t1.mo_id = t2.mo_id
      where t2.snils is null
    '''
    curs.execute(sql)
    writing_to_log_file(name_log, f'Количество записей в {table} после загрузки')
    table_cnt(table)  

#*****************************************************
def mvd_new():
    table = 'uszn.temp$_mvd_msp_new'
    writing_to_log_file(name_log, f'Загрузка данных в {table}')
    table_drop(table)
    
    sql=f'''
    create table {table} as
    select t1.*
    from uszn.temp$_mvd_msp_temp t1 left join uszn.temp$_mvd_msp t2
      on replace(replace(t1.snils, '-', ''), ' ', '') = replace(replace(t2.snils, '-', ''), ' ', '') 
         and t1.cat = t2.cat and t1.mo_id = t2.mo_id
      where t2.snils is null
    '''
    curs.execute(sql)
    writing_to_log_file(name_log, f'Количество записей в {table} после загрузки')
    table_cnt(table)    

#*****************************************************
def mvd_change():
    table = 'uszn.temp$_mvd_msp_change'
    writing_to_log_file(name_log, f'Загрузка данных в {table}')
    table_drop(table)
    
    sql=f'''
    create table {table} as
    select t1.*
    from uszn.temp$_mvd_msp_temp t1 join uszn.temp$_mvd_msp t2
      on replace(replace(t1.snils, '-', ''), ' ', '') = replace(replace(t2.snils, '-', ''), ' ', '') 
         and t1.cat = t2.cat and t1.mo_id = t2.mo_id and
            (t1.FAM != t2.FAM
             or t1.IMIA != t2.IMIA
             or t1.OTH != t2.OTH
             or t1.DTR != t2.DTR
             or t1.DUL_SER != t2.DUL_SER
             or t1.DULNOM != t2.DULNOM
             or t1.DATE_START != t2.DATE_START
             or t1.DATE_STOP != t2.DATE_STOP
             or t1.RV != t2.RV
             or t1.BIKB != t2.BIKB
             or t1.LSH != t2.LSH)         
    '''
    curs.execute(sql)
    writing_to_log_file(name_log, f'Количество записей в {table} после загрузки')
    table_cnt(table)

#*****************************************************
def mvd_update():
    table_msp = 'uszn.temp$_mvd_msp'
    #******************************
    table = 'uszn.temp$_mvd_msp_change'
    writing_to_log_file(name_log, f'Обновление таблицы {table_msp} из таблицы {table}')
    writing_to_log_file(name_log, f'Количество записей в {table}')
    table_cnt(table)
    writing_to_log_file(name_log, f'Количество записей в {table_msp}')
    table_cnt(table_msp)

    curs.execute(f'''UPDATE {table_msp}
                    SET dateTo = sysdate - INTERVAL '1' SECOND
                    WHERE replace(replace(snils, '-', ''), ' ', '')||cat||mo_id in 
                          (SELECT replace(replace(snils, '-', ''), ' ', '')||cat||mo_id FROM {table})
                    and dateTo = to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')''')

    writing_to_log_file(name_log, f'Количество записей в {table_msp}')
    table_cnt(table_msp)

    #******************************
    table = 'uszn.temp$_mvd_msp_del'
    writing_to_log_file(name_log, f'Обновление таблицы {table_msp} из таблицы {table}')
    writing_to_log_file(name_log, f'Количество записей в {table}')
    table_cnt(table)

    curs.execute(f'''UPDATE {table_msp}
                    SET dateTo = sysdate - INTERVAL '1' SECOND
                    WHERE replace(replace(snils, '-', ''), ' ', '')||cat||mo_id in 
                          (SELECT replace(replace(snils, '-', ''), ' ', '')||cat||mo_id FROM {table})
                    and dateTo = to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')''')

    writing_to_log_file(name_log, f'Количество записей в {table_msp} после загрузки')
    table_cnt(table_msp)

#*****************************************************
def mvd_insert():
    table_msp = 'uszn.temp$_mvd_msp'
    #*****************************
    table = 'uszn.temp$_mvd_msp_new'
    writing_to_log_file(name_log, f'Добавление записей в таблице {table_msp} из таблицы {table}')
    writing_to_log_file(name_log, f'Количество записей в {table_msp} до загрузки')
    table_cnt(table_msp)

    curs.execute(f'''
INSERT INTO {table_msp} 
        (NOM, FAM, IMIA, OTH, DTR, MTR, SNILS, INN, DUL, DUL_SER, DULNOM, DTDOC, DOCV, KODP, 
         NSP, UL, DOM, KORP, KV, DR, NMO, CAT, MONTH, DATE_START, DATE_STOP, RV, 
         SBB, BIKB, LSH, MO_ID, DATE_LOAD, FILE_LOAD, DELFLG, DATEFROM, DATETO)  
SELECT   NOM, FAM, IMIA, OTH, DTR, MTR, SNILS, INN, DUL, DUL_SER, DULNOM, DTDOC, DOCV, KODP, 
         NSP, UL, DOM, KORP, KV, DR, NMO, CAT, MONTH, DATE_START, DATE_STOP, RV, 
         SBB, BIKB, LSH, MO_ID, DATE_LOAD, FILE_LOAD, 0, sysdate, to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')
        FROM {table}
    ''')
    
    writing_to_log_file(name_log, f'Количество записей в {table_msp} после загрузки')
    table_cnt(table_msp)

    #*****************************
    table = 'uszn.temp$_mvd_msp_change'
    writing_to_log_file(name_log, f'Добавление записей в таблице {table_msp} из таблицы {table}')
    writing_to_log_file(name_log, f'Количество записей в {table_msp} до загрузки')
    table_cnt(table_msp)

    curs.execute(f'''
INSERT INTO {table_msp} 
        (NOM, FAM, IMIA, OTH, DTR, MTR, SNILS, INN, DUL, DUL_SER, DULNOM, DTDOC, DOCV, KODP, 
         NSP, UL, DOM, KORP, KV, DR, NMO, CAT, MONTH, DATE_START, DATE_STOP, RV, 
         SBB, BIKB, LSH, MO_ID, DATE_LOAD, FILE_LOAD, DELFLG, DATEFROM, DATETO)  
SELECT   NOM, FAM, IMIA, OTH, DTR, MTR, SNILS, INN, DUL, DUL_SER, DULNOM, DTDOC, DOCV, KODP, 
         NSP, UL, DOM, KORP, KV, DR, NMO, CAT, MONTH, DATE_START, DATE_STOP, RV, 
         SBB, BIKB, LSH, MO_ID, DATE_LOAD, FILE_LOAD, 0, sysdate, to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')
        FROM {table}
    ''')

    writing_to_log_file(name_log, f'Количество записей в {table_msp} после загрузки')
    table_cnt(table_msp)
    
    #*****************************
    table = 'uszn.temp$_mvd_msp_del'
    writing_to_log_file(name_log, f'Добавление записей в таблице {table_msp} из таблицы {table}')
    writing_to_log_file(name_log, f'Количество записей в {table_msp} до загрузки')
    table_cnt(table_msp)

    curs.execute(f'''
INSERT INTO {table_msp} 
        (NOM, FAM, IMIA, OTH, DTR, MTR, SNILS, INN, DUL, DUL_SER, DULNOM, DTDOC, DOCV, KODP, 
         NSP, UL, DOM, KORP, KV, DR, NMO, CAT, MONTH, DATE_START, DATE_STOP, RV, 
         SBB, BIKB, LSH, MO_ID, DATE_LOAD, FILE_LOAD, DELFLG, DATEFROM, DATETO)  
SELECT   NOM, FAM, IMIA, OTH, DTR, MTR, SNILS, INN, DUL, DUL_SER, DULNOM, DTDOC, DOCV, KODP, 
         NSP, UL, DOM, KORP, KV, DR, NMO, CAT, MONTH, DATE_START, DATE_STOP, RV, 
         SBB, BIKB, LSH, MO_ID, DATE_LOAD, FILE_LOAD, 1, sysdate, to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')
        FROM {table}
    ''')

    writing_to_log_file(name_log, f'Количество записей в {table_msp} после загрузки')
    table_cnt(table_msp)

#****************************************************************************************************
try: # подключение к серверу
    curs = connect_oracle()
    alarm_f = 0
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, log, text)
    alarm_f = 1

#****************************************************************************************************    
if alarm_f == 0: # очистка темп
    try:
        del_temp()
        alarm_f = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции del_temp() - {e}'
        alarm_log(mail, log, text)
        alarm_f = 1     
            
#****************************************************************************************************
writing_to_log_file(name_log, '*****************start**********************')
cnt = 0
c = os.listdir(os.getcwd())
for file in c: # читаем каталог, пишем все файлы в темп
    if file.endswith(".xlsx") or file.endswith(".xltx"): # если есть файлы, то
        writing_to_log_file(name_log, f'Файл поступил - {file}')
        
        if alarm_f == 0: # запичь файла в датафрейм
            try:
                xl = write_file_object(file, name_log)
                alarm_f = 0
            except Exception as e:
                text = f'произошла ошибка при вызове функции pre_processing() - {e}'
                alarm_log(mail, name_log, text)
                alarm_f = 1

        if alarm_f == 0: # перенос файла в бэкап
            try:
                backup_file(test, file, name_log, name_def, path_backup)
                alarm_f = 0
            except Exception as e:
                text = f'произошла ошибка при вызове функции backup_file() - {e}'
                alarm_log(mail, name_log, text)
                alarm_f = 1
                
        if alarm_f == 0: # очистка и обработка датафрейма
            try:
                pre_processing(xl, file)
                alarm_f = 0
            except Exception as e:
                text = f'произошла ошибка при вызове функции pre_processing() - {e}'
                alarm_log(mail, name_log, text)
                alarm_f = 1
        
        if alarm_f == 0: # загрузка датафрейма в темп
            try:
                mvd_insert_temp(xl)
                alarm_f = 0
                cnt += 1
            except Exception as e:
                text = f'произошла ошибка при вызове функции mvd_insert_temp() - {e}'
                alarm_log(mail, name_log, text)
                alarm_f = 1

        if alarm_f == 0: # загрузка датафрейма в накопитель всех данных
            try:
                mvd_insert_all()
                alarm_f = 0
            except Exception as e:
                text = f'произошла ошибка при вызове функции mvd_insert_all() - {e}'
                alarm_log(mail, name_log, text)
                alarm_f = 1
        
#****************************************************************************************************
if alarm_f == 0 and cnt > 0: # удаляем косяк мвд - тестовые записи
    try:
        del_kosyak()
        alarm_f = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции del_kosyak() - {e}'
        alarm_log(mail, name_log, text)
        alarm_f = 1
    
    if alarm_f == 0: # загрузка записей на удаление во временную таблицу
        try:
            mvd_del() 
        except Exception as e:
            text = f'произошла ошибка при вызове функции mvd_new() - {e}'
            alarm_log(mail, name_log, text)
            alarm_f = 1
    
    if alarm_f == 0: # загрузка новых записей во временную таблицу
        try:
            mvd_new() 
        except Exception as e:
            text = f'произошла ошибка при вызове функции mvd_new() - {e}'
            alarm_log(mail, name_log, text)
            alarm_f = 1
    
    if alarm_f == 0: # загрузка измененных записей во временную таблицу
        try:
            mvd_change()
        except Exception as e:
            text = f'произошла ошибка при вызове функции mvd_change() - {e}'
            alarm_log(mail, name_log, text)
            alarm_f = 1
    
    if alarm_f == 0: # обновление записей таблицы из изменений chahge и удаления del
        try:
            mvd_update()
        except Exception as e:
            text = f'произошла ошибка при вызове функции mvd_update() - {e}'
            alarm_log(mail, name_log, text)
            alarm_f = 1
            
    if alarm_f == 0: # добавление новых записей в таблицу из new, chahge и del
        try:
            mvd_insert()
        except Exception as e:
            text = f'произошла ошибка при вызове функции mvd_insert() - {e}'
            alarm_log(mail, name_log, text)
            alarm_f = 1
            
writing_to_log_file(name_log, '*****************end***********************')        