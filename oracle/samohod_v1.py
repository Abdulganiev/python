import pandas as pd 
from generating_report_files import *
import re

#***************************************************************
log = 'samohod'
mail = 'IVAbdulganiev@yanao.ru'

#****************************************************************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, log, text)

#****************************************************************************************************
def v1(xl):
    try:
        v1_drop()
    except Exception as e:
        text = f'произошла ошибка при вызове функции v1_drop() - {e}'
        alarm_log(mail, log, text)

    try:
        v1_insert(xl)
    except Exception as e:
        text = f'произошла ошибка при вызове функции v1_insert() - {e}'
        alarm_log(mail, log, text)

    try:
        v1_table_all()
    except Exception as e:
        text = f'произошла ошибка при вызове функции v1_table_all() - {e}'
        alarm_log(mail, log, text)

    try:
        v1_table_del()
    except Exception as e:
        text = f'произошла ошибка при вызове функции v1_table_del() - {e}'
        alarm_log(mail, log, text)

    try:
        v1_table_new()
    except Exception as e:
        text = f'произошла ошибка при вызове функции v1_table_new() - {e}'
        alarm_log(mail, log, text)

    try:
        v1_table_chahge()
    except Exception as e:
        text = f'произошла ошибка при вызове функции v1_table_chahge() - {e}'
        alarm_log(mail, log, text)

    try:
        v1_table_update()
    except Exception as e:
        text = f'произошла ошибка при вызове функции v1_table_update() - {e}'
        alarm_log(mail, log, text)

    try:
        v1_table_insert()
    except Exception as e:
        text = f'произошла ошибка при вызове функции v1_table_insert() - {e}'
        alarm_log(mail, log, text)


#****************************************************************************************************
def v1_table_all():
    writing_to_log_file(log, 'Загрузка данных в uszn.temp$_snowmobile_all')
    
    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_all')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile_all перед загрузкой - {cnt}')

    curs.execute('''INSERT INTO uszn.temp$_snowmobile_all (CarNumber, Brand, Name, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, RegDate, UploadDate)
                    SELECT t1.CarNumber, t1.Brand, t1.Name, t1.YearRelease, t1.Owner, t1.Address, t1.IdentityDoc, t1.Who, t1.DateIssue, t1.BirthDate, t1.RegDate, t1.UploadDate
                    FROM uszn.temp$_snowmobile_temp t1
                         LEFT JOIN uszn.temp$_snowmobile_all t2
                    on t1.uploaddate = t2.uploaddate
                    WHERE t2.uploaddate is null''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_all')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile_all после загрузки - {cnt}')

#****************************************************************************************************
def v1_table_del():
    writing_to_log_file(log, 'Удаление таблицы uszn.temp$_snowmobile_del')
    curs.execute('DROP TABLE uszn.temp$_snowmobile_del')

    writing_to_log_file(log, 'Создание таблицы uszn.temp$_snowmobile_del из загрузка в нее данных')
    curs.execute('''CREATE TABLE uszn.temp$_snowmobile_del AS
                    SELECT 
                     t1.CarNumber,
                     t1.Brand,
                     t1.Name,
                     t1.YearRelease,
                     t1.Owner,
                     t1.Address,
                     t1.IdentityDoc,
                     t1.Who,
                     t1.DateIssue,
                     t1.BirthDate,
                     t1.RegDate
                     FROM uszn.temp$_v_snowmobile t1
                          LEFT JOIN uszn.temp$_v_snowmobile_temp t2
                     ON t1.carnumber = t2.carnumber
                    WHERE t2.carnumber is null''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_del')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile_del после загрузки - {cnt}')

#****************************************************************************************************
def v1_table_new():
    writing_to_log_file(log, 'Удаление таблицы uszn.temp$_snowmobile_new')
    curs.execute('DROP TABLE uszn.temp$_snowmobile_new')

    curs.execute('''CREATE TABLE uszn.temp$_snowmobile_new AS
                    SELECT
                     t1.CarNumber,
                     t1.Brand,
                     t1.Name,
                     t1.YearRelease,
                     t1.Owner,
                     t1.Address,
                     t1.IdentityDoc,
                     t1.Who,
                     t1.DateIssue,
                     t1.BirthDate,
                     t1.RegDate
                     FROM uszn.temp$_v_snowmobile_temp t1
                          LEFT JOIN uszn.temp$_v_snowmobile t2
                     ON t1.carnumber = t2.carnumber
                    WHERE t2.carnumber is null''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_new')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile_new после загрузки - {cnt}')

#****************************************************************************************************
def v1_table_chahge():
    writing_to_log_file(log, 'Удаление таблицы uszn.temp$_snowmobile_change')
    curs.execute('DROP TABLE uszn.temp$_snowmobile_change')

    curs.execute('''CREATE TABLE uszn.temp$_snowmobile_change AS
                    SELECT
                     t1.CarNumber,
                     t1.Brand,
                     t1.Name,
                     t1.YearRelease,
                     t1.Owner,
                     t1.Address,
                     t1.IdentityDoc,
                     t1.Who,
                     t1.DateIssue,
                     t1.BirthDate,
                     t1.RegDate
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
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile_change после загрузки - {cnt}')

#****************************************************************************************************
def v1_table_update():
    writing_to_log_file(log, 'Обновление таблицы uszn.temp$_snowmobile из таблицы uszn.temp$_snowmobile_change')
    
    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_change')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile_change - {cnt}')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile до загрузки - {cnt}')

    curs.execute('''UPDATE uszn.temp$_snowmobile
                    SET dateTo = sysdate - INTERVAL '1' SECOND
                    WHERE CarNumber in (SELECT CarNumber FROM uszn.temp$_snowmobile_change)
                    and dateTo = to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile после загрузки - {cnt}')


    #******************************
    writing_to_log_file(log, 'Обновление таблицы uszn.temp$_snowmobile из таблицы uszn.temp$_snowmobile_del')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_del')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile_del - {cnt}')

    curs.execute('''UPDATE uszn.temp$_snowmobile
                    SET dateTo = sysdate - INTERVAL '1' SECOND
                    WHERE CarNumber in (SELECT CarNumber FROM uszn.temp$_snowmobile_del)
                    and dateTo = to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')''')
    
#****************************************************************************************************
def v1_table_insert():
    #*****************************
    writing_to_log_file(log, 'Добавление записей в таблице uszn.temp$_snowmobile из таблицы uszn.temp$_snowmobile_new')
    
    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile до загрузки - {cnt}')

    curs.execute('''INSERT INTO uszn.temp$_snowmobile (CarNumber, Brand, Name, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, RegDate, DelFlg, DateFrom, DateTo)  
                    SELECT CarNumber, Brand, Name, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, RegDate, 0, sysdate, to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')
                    FROM uszn.temp$_snowmobile_new''')
    
    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile после загрузки - {cnt}')

    #*****************************
    writing_to_log_file(log, 'Добавление записей в таблице uszn.temp$_snowmobile из таблицы uszn.temp$_snowmobile_change')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile до загрузки - {cnt}')

    curs.execute('''INSERT INTO uszn.temp$_snowmobile (CarNumber, Brand, Name, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, RegDate, DelFlg, DateFrom, DateTo)  
                    SELECT CarNumber, Brand, Name, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, RegDate, 0, sysdate, to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss')
                    FROM uszn.temp$_snowmobile_change''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile после загрузки - {cnt}')
    
    #*****************************
    writing_to_log_file(log, 'Добавление записей в таблице uszn.temp$_snowmobile из таблицы uszn.temp$_snowmobile_del')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile до загрузки - {cnt}')

    curs.execute('''INSERT INTO uszn.temp$_snowmobile (CarNumber, Brand, Name, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, RegDate, DelFlg, DateFrom, DateTo)  
                    SELECT CarNumber, Brand, Name, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, RegDate, 1, sysdate, to_date('31.12.9999,23:59:59','dd.mm.yyyy,hh24:mi:ss') 
                    FROM uszn.temp$_snowmobile_del''')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в uszn.temp$_snowmobile после загрузки - {cnt}')

#****************************************************************************************************
def v1_drop():
    writing_to_log_file(log, 'Удаление данных из uszn.temp$_snowmobile_temp')
    
    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_temp')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'В uszn.temp$_snowmobile_temp было {cnt} записей')
    
    curs.execute('DELETE FROM uszn.temp$_snowmobile_temp')

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_temp')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'В uszn.temp$_snowmobile_temp осталось {cnt} записей')

#**************************************************************************************************
def v1_insert(xl):
    writing_to_log_file(log, f'Загрузка данных в uszn.temp$_snowmobile_temp')
    
    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_temp')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'В uszn.temp$_snowmobile_temp было {cnt} записей')

    xl.drop(labels = [0,1,2],axis = 0, inplace = True)
    xl.dropna(thresh=3, inplace = True)

    xl['Unnamed: 8'] = pd.to_datetime(xl['Unnamed: 8']).dt.normalize()
    xl['Unnamed: 8'] = xl['Unnamed: 8'].apply(dat)

    xl['Unnamed: 9'] = pd.to_datetime(xl['Unnamed: 9']).dt.normalize()
    xl['Unnamed: 9'] = xl['Unnamed: 9'].apply(dat)

    xl['Unnamed: 10'] = pd.to_datetime(xl['Unnamed: 10']).dt.normalize()
    xl['Unnamed: 10'] = xl['Unnamed: 10'].apply(dat)

    for data in xl.itertuples(index=False):
        curs.execute('''INSERT INTO uszn.temp$_snowmobile_temp (CarNumber, Brand, Name, YearRelease, Owner, Address, IdentityDoc, Who, DateIssue, BirthDate, RegDate, UploadDate) 
        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, to_date(sysdate, 'dd.mm.yyyy'))''', [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10]])

    curs.execute('SELECT count(*) FROM uszn.temp$_snowmobile_temp')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'В uszn.temp$_snowmobile_temp стало {cnt} записей')

#****************************************************************************************************
def dat(x):
    try:
        x = str(x).replace(' 00:00:00', '')
        return re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3.\2.\1', x)
    except:
        return x