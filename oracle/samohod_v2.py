import pandas as pd
import os, sys
from samohod_v1 import writing_to_log_file

#****************************************************************************************************
def v2_table_all(conn):
    curs = conn.cursor()

    writing_to_log_file('Загрузка данных в uszn.temp$_snowmobile_all')
    
    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_all')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile_all перед загрузкой - {cnt}')

    curs.execute('''INSERT INTO uszn.temp$_snowmobile_all (CarNumber, Brand, Name, RegDate, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, UploadDate)
                    SELECT t1.*
                    FROM uszn.temp$_snowmobile_temp t1
                         LEFT JOIN uszn.temp$_snowmobile_all t2
                    on t1.uploaddate = t2.uploaddate
                    WHERE t2.uploaddate is null''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_all')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile_all после загрузки - {cnt}')

#****************************************************************************************************
def v2_table_del(conn):
    curs = conn.cursor()

    writing_to_log_file('Удаление таблицы uszn.temp$_snowmobile_del')
    curs.execute('DROP TABLE uszn.temp$_snowmobile_del')

    writing_to_log_file('Создание таблицы uszn.temp$_snowmobile_del из загрузка в нее данных')
    curs.execute('''CREATE TABLE uszn.temp$_snowmobile_del as
                    SELECT 
                     t1.CarNumber,
                     t1.Brand,
                     t1.Name,
                     t1.RegDate,
                     t1.YearRelease,
                     t1.Owner,
                     t1.Address,
                     t1.IdentityDoc,
                     t1.Who,
                     t1.DateIssue,
                     t1.BirthDate
                     FROM uszn.temp$_v_snowmobile t1
                          LEFT JOIN uszn.temp$_v_snowmobile_temp t2
                     ON t1.carnumber = t2.carnumber
                    WHERE t2.carnumber is null''')

#****************************************************************************************************
def v2_table_new(conn):
    curs = conn.cursor()

    writing_to_log_file('Удаление таблицы uszn.temp$_snowmobile_new')
    curs.execute('DROP TABLE uszn.temp$_snowmobile_new')

    curs.execute('''CREATE TABLE uszn.temp$_snowmobile_new AS
                    SELECT
                     t1.CarNumber,
                     t1.Brand,
                     t1.Name,
                     t1.RegDate,
                     t1.YearRelease,
                     t1.Owner,
                     t1.Address,
                     t1.IdentityDoc,
                     t1.Who,
                     t1.DateIssue,
                     t1.BirthDate
                     FROM uszn.temp$_v_snowmobile_temp t1
                          LEFT JOIN uszn.temp$_v_snowmobile t2
                     ON t1.carnumber = t2.carnumber
                    WHERE t2.carnumber is null''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_new')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile_new после загрузки - {cnt}')

#****************************************************************************************************
def v2_table_chahge(conn):
    curs = conn.cursor()

    writing_to_log_file('Удаление таблицы uszn.temp$_snowmobile_change')
    curs.execute('DROP TABLE uszn.temp$_snowmobile_change')

    curs.execute('''CREATE TABLE uszn.temp$_snowmobile_change AS
                    SELECT
                     t1.CarNumber,
                     t1.Brand,
                     t1.Name,
                     t1.RegDate,
                     t1.YearRelease,
                     t1.Owner,
                     t1.Address,
                     t1.IdentityDoc,
                     t1.Who,
                     t1.DateIssue,
                     t1.BirthDate
                     FROM uszn.temp$_v_snowmobile_temp t1
                          INNER JOIN uszn.temp$_v_snowmobile t2
                     ON t1.carnumber = t2.carnumber and 
                        (t2.CarNumber != t1.CarNumber 
                         or t2.Brand != t1.Brand 
                         or t2.Name != t1.Name 
                         or t2.YearRelease != t1.YearRelease 
                         or t2.Owner != t1.Owner 
                         or t2.Address != t1.Address 
                         or t2.IdentityDoc != t1.IdentityDoc 
                         or t2.Who != t1.Who 
                         or t2.DateIssue != t1.DateIssue 
                         or t2.BirthDate != t1.BirthDate 
                         or t2.RegDate != t1.RegDate)''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_change')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile_change после загрузки - {cnt}')

#****************************************************************************************************
def v2_table_update(conn):
    curs = conn.cursor()

    writing_to_log_file('Обновление таблицы uszn.temp$_snowmobile из таблицы uszn.temp$_snowmobile_change')
    
    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_change')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile_change - {cnt}')

    curs.execute('''UPDATE uszn.temp$_snowmobile
                    SET dateTo = sysdate - INTERVAL '1' SECOND
                    WHERE CarNumber in (SELECT CarNumber FROM uszn.temp$_snowmobile_change)
                    and dateTo = to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')''')

    #******************************
    writing_to_log_file('Обновление таблицы uszn.temp$_snowmobile из таблицы uszn.temp$_snowmobile_del')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_del')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile_del - {cnt}')

    curs.execute('''UPDATE uszn.temp$_snowmobile
                    SET dateTo = sysdate - INTERVAL '1' SECOND
                    WHERE CarNumber in (SELECT CarNumber FROM uszn.temp$_snowmobile_del)
                    and dateTo = to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')''')


#****************************************************************************************************
def v2_table_insert(conn):
    curs = conn.cursor()

    #*****************************
    writing_to_log_file('Добавление записей в таблице uszn.temp$_snowmobile из таблицы uszn.temp$_snowmobile_new')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile до загрузки - {cnt}')

    curs.execute('''INSERT INTO uszn.temp$_snowmobile (CarNumber, Brand, Name, RegDate, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, DelFlg, DateFrom, DateTo)  
                    SELECT CarNumber, Brand, Name, RegDate, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, 0, sysdate, to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')
                    FROM uszn.temp$_snowmobile_new''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile после загрузки - {cnt}')

    #*****************************
    writing_to_log_file('Добавление записей в таблице uszn.temp$_snowmobile из таблицы uszn.temp$_snowmobile_change')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile до загрузки - {cnt}')

    curs.execute('''INSERT INTO uszn.temp$_snowmobile (CarNumber, Brand, Name, RegDate, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, DelFlg, DateFrom, DateTo)  
                    SELECT CarNumber, Brand, Name, RegDate, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, 0, sysdate, to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')
                    FROM uszn.temp$_snowmobile_change''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile после загрузки - {cnt}')

    #*****************************    
    writing_to_log_file('Добавление записей в таблице uszn.temp$_snowmobile из таблицы uszn.temp$_snowmobile_del')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile до загрузки - {cnt}')

    curs.execute('''INSERT INTO uszn.temp$_snowmobile (CarNumber, Brand, Name, RegDate, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, DelFlg, DateFrom, DateTo)  
                    SELECT CarNumber, Brand, Name, RegDate, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, 1, sysdate, to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss') 
                    FROM uszn.temp$_snowmobile_del''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'Количество записей в uszn.temp$_snowmobile после загрузки - {cnt}')

#****************************************************************************************************
def v2_drop(conn):
    curs = conn.cursor()

    writing_to_log_file('Удаление данных из uszn.temp$_snowmobile_temp')
    
    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_temp')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'В uszn.temp$_snowmobile_temp было {cnt} записей')

    curs.execute('DELETE FROM uszn.temp$_snowmobile_temp')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_temp')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'В uszn.temp$_snowmobile_temp осталось {cnt} записей')

#****************************************************************************************************
def v2_insert(conn, xl):
    curs = conn.cursor()

    writing_to_log_file(f'Загрузка данных в uszn.temp$_snowmobile_temp')
    
    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_temp')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'В uszn.temp$_snowmobile_temp было {cnt} записей')

    xl.drop(labels = [0,1,2],axis = 0, inplace = True)
    xl.dropna(thresh=3, inplace = True)

    for data in xl.itertuples(index=False):
        curs.execute('''INSERT INTO uszn.temp$_snowmobile_temp (CarNumber, Brand, Name, RegDate, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, UploadDate) 
        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, to_date(sysdate, 'dd.mm.yyyy'))''', [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10]])

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_temp')
    cnt = curs.fetchone()[0]
    writing_to_log_file(f'В uszn.temp$_snowmobile_temp стало {cnt} записей')