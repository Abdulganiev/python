import pandas as pd
import os, re
import zipfile
import datetime as dt
from generating_report_files import *

#***************************************************************
log = 'ES_present'
mail = 'IVAbdulganiev@yanao.ru'
today = dt.date.today()
test = 0
check_day = 10

patchs = get_platform()
trek = patchs['trek']

path_backup = f'{trek}/backup/ES_present/'
path = patchs['prezent']

os.chdir(path)

#***************************************************************
def movi_file(file):
    new_file_name = f'{today} - {file}'
    os.replace(file, f'{path_backup}/{new_file_name}')
    writing_to_log_file(log, f'Файл {file} перемещен в backup и переименован в {new_file_name}')

#***************************************************************    
def zdrav_insert_temp(xl):
    table = 'uszn.temp$_zdrav_prezent_temp'
    writing_to_log_file(log, f'Загрузка данных в {table}')
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'В {table} перед загрузкой {cnt} записей')

    if xl.iloc[0][0] != 1:
        xl.drop(index=list(range(0, xl['NOM'][xl['NOM'] == 1].index.tolist()[0])), inplace = True)

    for data in xl.itertuples(index=False):
        curs.execute(f'''
        INSERT INTO {table} 
        (HOSPITAL, 
         SNILS, F, I, O, DR, 
         DUL_TYPE, DUL_SER, DUL_NOM, DUL_PLACE, DUL_KEM, DUL_DATE, DUL_CODE, 
         BABY_DR, 
         ADR_MO, ADR_FULL, CONTACT, REASON, REGION_ID) 
         values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
         [data[1],  data[2],  data[3],  data[4],  data[5],  data[6], data[7], data[8], data[9], data[10],
          data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19]])
    
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в {table} после загрузки - {cnt}')
    
#***************************************************************    
def zdrav_new():
    table = 'uszn.temp$_zdrav_prezent_new'
    writing_to_log_file(log, f'Загрузка данных в {table}')
    try:
        curs.execute(f'DROP TABLE {table}')
    except:
        writing_to_log_file(log, f'Таблица {table} еще не создана')
    curs.execute(f'''CREATE TABLE {table} AS
                        SELECT
                         t1.HOSPITAL,  t1.SNILS,  t1.F,  t1.I,  t1.O,  t1.DR,  
                         t1.DUL_TYPE,  t1.DUL_SER,  t1.DUL_NOM,  t1.DUL_PLACE,  t1.DUL_KEM,  t1.DUL_DATE,  t1.DUL_CODE,  
                         t1.BABY_DR, t1.REGION_ID, t1.ADR_MO,  t1.ADR_FULL,  t1.CONTACT,  t1.REASON
                         FROM uszn.temp$_zdrav_prezent_temp t1
                              LEFT JOIN uszn.temp$_zdrav_prezent t2
                         ON t1.SNILS = t2.SNILS
                         WHERE t2.SNILS is null''')
    try:
        curs.execute(f'SELECT count(*) FROM {table}')
        cnt = curs.fetchone()[0]
        writing_to_log_file(log, f'В {table} загружено {cnt} записей')
    except:
        writing_to_log_file(log, f'Таблица {table} еще не создана')
        
#****************************************************************************************************
def zdrav_insert():
    table = 'uszn.temp$_zdrav_prezent'
    table_new = 'uszn.temp$_zdrav_prezent_new'
    writing_to_log_file(log, f'Добавление записей в таблицу {table} из таблицы {table_new}')
    
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в {table} до загрузки - {cnt}')

    curs.execute(f'''INSERT INTO {table} 
    (HOSPITAL, SNILS, F, I, O, DR, DUL_TYPE, DUL_SER, DUL_NOM, DUL_PLACE, DUL_KEM, DUL_DATE, DUL_CODE, 
     BABY_DR, REGION_ID, ADR_MO, ADR_FULL, CONTACT, REASON)  
    SELECT HOSPITAL, SNILS, F, I, O, DR, DUL_TYPE, DUL_SER, DUL_NOM, DUL_PLACE, DUL_KEM, DUL_DATE, DUL_CODE, 
           BABY_DR, REGION_ID, ADR_MO, ADR_FULL, CONTACT, REASON
    FROM {table_new}''')
    
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в {table} после загрузки - {cnt}')
    
#****************************************************************************************************
def zdrav_find_egisso():
    table = 'uszn.temp$_zdrav_prezent_egisso'
    try: 
        curs.execute(f'drop table {table}')
    except:
        writing_to_log_file(log, f'Таблица {table} еще не создана')
    
    sql = f'''create table {table} as
    select t1.*, t2.SNILS, t2.F, t2.I, t2.O, t2.DR, t2.REGION_ID, t2.ADR_MO, t2.ADR_FULL, t2.CONTACT, t2.REASON
from uszn.temp$_v_birth t1
     inner join
     uszn.temp$_zdrav_prezent t2
on  t1.baby_birth_date=t2.BABY_DR
    and
   (replace(replace(replace(upper(t1.MAMA_LAST_NAME||t1.MAMA_FIRST_NAME||t1.MAMA_MIDDLE_NAME||t1.MAMA_BIRTH_DATE), 'Ё', 'Е'), ' ', ''), '-', '') =
    replace(replace(replace(upper(t2.F||t2.I||t2.O||t2.DR), 'Ё', 'Е'), ' ', ''), '-', '')
    or
    replace(replace(replace(upper(t1.PAPA_LAST_NAME||t1.PAPA_FIRST_NAME||t1.PAPA_MIDDLE_NAME||t1.PAPA_BIRTH_DATE), 'Ё', 'Е'), ' ', ''), '-', '') =
    replace(replace(replace(upper(t2.F||t2.I||t2.O||t2.DR), 'Ё', 'Е'), ' ', ''), '-', '')
    or t1.MAMA_SNILS=replace(replace(t2.SNILS, ' ', ''), '-', '')
    or t1.MAMA_SNILS=replace(replace(t2.SNILS, ' ', ''), '-', ''))
    and t2.check_egisso=0 and t2.CHECK_CNT < {check_day}'''
    
    curs.execute(sql)
    
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Найдено {cnt} записей в ЕГИССО')
    
    if test == 0:
        sql = f'''update uszn.temp$_zdrav_prezent set check_egisso=1 where snils in (select snils from {table})'''
        curs.execute(sql)

        sql = f'''update uszn.temp$_zdrav_prezent set CHECK_CNT=CHECK_CNT+1'''
        curs.execute(sql)
    
    
#****************************************************************************************************
def zdrav_find_iszn():
    table = 'uszn.temp$_zdrav_prezent_iszn'
    try: 
        curs.execute(f'drop table {table}')
    except:
        writing_to_log_file(log, f'Таблица {table} еще не создана')
    
    sql = f'''create table {table} as
select distinct
       '0'||t2.region_id||' - '||uszn.pkTSrv.GetRegionName(t2.region_id)||' - претендент на ЭС подарок найдены в исзн' as name,
       uszn.pkTSrv.GetRegionName(t2.region_id) as MO,
       t2.region_id||'-'||t2.id as people_id,
       t1.*
from uszn.temp$_zdrav_prezent_egisso t1
     inner join
     uszn.v_people_and_colls t2
on (t1.SNILS=t2.snils_formatted
    or
   replace(replace(replace(upper(t2.LAST_NAME||t2.FIRST_NAME||t2.MIDDLE_NAME||t2.BIRTH_DATE), 'Ё', 'Е'), ' ', ''), '-', '') =
   replace(replace(replace(upper(t1.F||t1.I||t1.O||t1.DR), 'Ё', 'Е'), ' ', ''), '-', '') )
   and t2.close_date is null
   and t1.region_id=t2.region_id'''
    
    curs.execute(sql)
    
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Найдено {cnt} записей в исзн')
    
    curs.execute(f'''SELECT distinct 
region_id, 
name, 
MO, 
people_id, 
BABY_SNILS, 
BABY_LAST_NAME||' '||BABY_FIRST_NAME||' '||BABY_MIDDLE_NAME||' '||BABY_BIRTH_DATE, 
BABY_SEX, 
BABY_BIRTH_PLACE,
ZAGZ||' '||AZ_DATE||' '||AZ_NUM||' '||SV_SER||' '||SV_NUM||' '||SV_DATE,
MAMA_SNILS, 
MAMA_LAST_NAME||' '||MAMA_FIRST_NAME||' '||MAMA_MIDDLE_NAME||' '||MAMA_BIRTH_DATE,
MAMA_DUL_TYPE||' '||MAMA_DUL_SER_NOM||' '||MAMA_DUL_DATA||' '||MAMA_DUL_ISSUED||' '||MAMA_BIRTH_PLACE||' '||MAMA_ADR,
PAPA_SNILS,
PAPA_LAST_NAME||' '||PAPA_FIRST_NAME||' '||PAPA_MIDDLE_NAME||' '||PAPA_BIRTH_DATE,
PAPA_DUL_TYPE||' '||PAPA_DUL_SER_NOM||' '||PAPA_DUL_DATA||' '||PAPA_DUL_ISSUED||' '||PAPA_BIRTH_PLACE||' '||PAPA_ADR,
PAPA_OSN||' '||PAPA_OSN_DATA||' '||PAPA_OSN_KOD||' '||PAPA_OSN_NAME||' '||PAPA_OSN_NOM||' '||PAPA_OSN_TYPE,
BIRTH_DOC_TYPE||' '||BIRTH_DOC_KONTORA||' '||BIRTH_DOC_DATA||' '||BIRTH_DOC_SER_NOM,
SNILS||' '||F||' '||I||' '||O||' '||DR||' '||ADR_FULL,
CONTACT, 
REASON 
    FROM {table}''')

    data = {
        'id района' : [],
        'name' : [] ,
        'Наименование района' : [],
        'id родителя' : [] ,
        'СНИЛС ребенка' : [] ,
        'ФИО и дата рождения ребенка' : [] ,
        'Пол ребенка' : [] ,
        'Место рождения ребенка' : [] ,
        'Данные свидетельства о рождении ребенка' : [] ,
        'СНИЛС матери' : [] ,
        'ФИО и дата рождения матери' : [] ,
        'Данные ДУЛ матери' : [] ,
        'СНИЛС отца' : [] ,
        'ФИО и дата рождения отца' : [] ,
        'Данные ДУЛ отца' : [] ,
        'Основание для отца' : [] ,
        'Больница' : [],
        'Данные о родителе из больницы' : [] ,
        'Контактные данные' : [] ,
        'Причина' : [] ,
            }
    
    for row in curs.fetchall():
        data['id района'].append(row[0]),
        data['name'].append(row[1]),
        data['Наименование района'].append(row[2]),
        data['id родителя'].append(row[3]),
        data['СНИЛС ребенка'].append(row[4]),
        data['ФИО и дата рождения ребенка'].append(row[5]),
        data['Пол ребенка'].append(row[6]),
        data['Место рождения ребенка'].append(row[7]),
        data['Данные свидетельства о рождении ребенка'].append(row[8]),
        data['СНИЛС матери'].append(row[9]),
        data['ФИО и дата рождения матери'].append(row[10]),
        data['Данные ДУЛ матери'].append(row[11]),
        data['СНИЛС отца'].append(row[12]),
        data['ФИО и дата рождения отца'].append(row[13]),
        data['Данные ДУЛ отца'].append(row[14]),
        data['Основание для отца'].append(row[15]),
        data['Больница'].append(row[16]),
        data['Данные о родителе из больницы'].append(row[17]),
        data['Контактные данные'].append(row[18]),
        data['Причина'].append(row[19])
        
    name_def = 'Претенденты на ЭС подарок новорожденному найдены в исзн'
    generating_report_files(data, log, name_def, test, mail)
    
#****************************************************************************************************
def zdrav_not_find_iszn():
    table = 'uszn.temp$_zdrav_prezent_not_iszn'
    try: 
        curs.execute(f'drop table {table}')
    except:
        writing_to_log_file(log, f'Таблица {table} еще не создана')
    
    sql = f'''create table {table} as
select t1.*
from uszn.temp$_zdrav_prezent_egisso t1
     left join
     uszn.v_people_and_colls t2
on (t1.SNILS=t2.snils_formatted
    or
   replace(replace(replace(upper(t2.LAST_NAME||t2.FIRST_NAME||t2.MIDDLE_NAME||t2.BIRTH_DATE), 'Ё', 'Е'), ' ', ''), '-', '') =
   replace(replace(replace(upper(t1.F||t1.I||t1.O||t1.DR), 'Ё', 'Е'), ' ', ''), '-', '') )
   and t2.close_date is null
   and t1.region_id=t2.region_id
where t2.region_id is null'''
    
    curs.execute(sql)
    
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'НЕ найдено {cnt} записей в исзн')

    curs.execute(f'''SELECT 
region_id, 
'0'||region_id||' - '||uszn.pkTSrv.GetRegionName(region_id)||' - претендент на ЭС подарок НЕ найдены в исзн' as name,
uszn.pkTSrv.GetRegionName(region_id) as MO,
'' as people_id, --id родителя
BABY_SNILS, 
BABY_LAST_NAME||' '||BABY_FIRST_NAME||' '||BABY_MIDDLE_NAME||' '||BABY_BIRTH_DATE, 
BABY_SEX, -- Пол ребенка
BABY_BIRTH_PLACE,
ZAGZ||' '||AZ_DATE||' '||AZ_NUM||' '||SV_SER||' '||SV_NUM||' '||SV_DATE,
MAMA_SNILS, -- СНИЛС матери 
MAMA_LAST_NAME||' '||MAMA_FIRST_NAME||' '||MAMA_MIDDLE_NAME||' '||MAMA_BIRTH_DATE,
MAMA_DUL_TYPE||' '||MAMA_DUL_SER_NOM||' '||MAMA_DUL_DATA||' '||MAMA_DUL_ISSUED||' '||MAMA_BIRTH_PLACE||' '||MAMA_ADR,
PAPA_SNILS, -- СНИЛС отца 
PAPA_LAST_NAME||' '||PAPA_FIRST_NAME||' '||PAPA_MIDDLE_NAME||' '||PAPA_BIRTH_DATE,
PAPA_DUL_TYPE||' '||PAPA_DUL_SER_NOM||' '||PAPA_DUL_DATA||' '||PAPA_DUL_ISSUED||' '||PAPA_BIRTH_PLACE||' '||PAPA_ADR, -- Данные ДУЛ отца
PAPA_OSN||' '||PAPA_OSN_DATA||' '||PAPA_OSN_KOD||' '||PAPA_OSN_NAME||' '||PAPA_OSN_NOM||' '||PAPA_OSN_TYPE, -- Основание для отца
BIRTH_DOC_TYPE||' '||BIRTH_DOC_KONTORA||' '||BIRTH_DOC_DATA||' '||BIRTH_DOC_SER_NOM, -- 
SNILS||' '||F||' '||I||' '||O||' '||DR||' '||ADR_FULL, -- Данные о родителе из больницы
CONTACT, -- Контактные данные
REASON -- Причина
  FROM {table}''')

    data = {
        'id района' : [],
        'name' : [] ,
        'Наименование района' : [],
        'id родителя' : [] ,
        'СНИЛС ребенка' : [] ,
        'ФИО и дата рождения ребенка' : [] ,
        'Пол ребенка' : [] ,
        'Место рождения ребенка' : [] ,
        'Данные свидетельства о рождении ребенка' : [] ,
        'СНИЛС матери' : [] ,
        'ФИО и дата рождения матери' : [] ,
        'Данные ДУЛ матери' : [] ,
        'СНИЛС отца' : [] ,
        'ФИО и дата рождения отца' : [] ,
        'Данные ДУЛ отца' : [] ,
        'Основание для отца'  : [] ,
        'Больница' : [],
        'Данные о родителе из больницы' : [] ,
        'Контактные данные' : [] ,
        'Причина' : [] ,
            }
    
    for row in curs.fetchall():
        data['id района'].append(row[0]),
        data['name'].append(row[1]),
        data['Наименование района'].append(row[2]),
        data['id родителя'].append(row[3]),
        data['СНИЛС ребенка'].append(row[4]),
        data['ФИО и дата рождения ребенка'].append(row[5]),
        data['Пол ребенка'].append(row[6]),
        data['Место рождения ребенка'].append(row[7]),
        data['Данные свидетельства о рождении ребенка'].append(row[8]),
        data['СНИЛС матери'].append(row[9]),
        data['ФИО и дата рождения матери'].append(row[10]),
        data['Данные ДУЛ матери'].append(row[11]),
        data['СНИЛС отца'].append(row[12]),
        data['ФИО и дата рождения отца'].append(row[13]),
        data['Данные ДУЛ отца'].append(row[14]),
        data['Основание для отца'].append(row[15]),
        data['Больница'].append(row[16]),
        data['Данные о родителе из больницы'].append(row[17]),
        data['Контактные данные'].append(row[18]),
        data['Причина'].append(row[19])
    
    if cnt > 0:
        name_def = 'Претенденты на ЭС подарок новорожденному НЕ найдены в исзн'
        generating_report_files(data, log, name_def, test, mail)

#****************************************************************************************************
def zdrav_not_find_egisso():
    table = 'uszn.temp$_zdrav_prezent_not_egisso'
    try: 
        curs.execute(f'drop table {table}')
    except:
        writing_to_log_file(log, f'Таблица {table} еще не создана')
    
    sql = f'''create table {table} as
    select * from uszn.temp$_zdrav_prezent where CHECK_EGISSO=0 AND CHECK_CNT < {check_day}'''
    
    curs.execute(sql)
    
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'НЕ найдено {cnt} записей в ЕГИССО')
    
    curs.execute(f'''SELECT region_id, 
'0'||region_id||' - '||uszn.pkTSrv.GetRegionName(region_id)||' - претендент на ЭС подарок НЕ найдены в ЕГР ЗАГС' as name,
uszn.pkTSrv.GetRegionName(region_id) as MO,
SNILS, F||' '||I||' '||O||' '||DR, 
DUL_TYPE||' '||DUL_SER||' '||DUL_NOM||' '||DUL_PLACE||' '||DUL_KEM||' '||DUL_DATE||' '||DUL_CODE, 
BABY_DR, 
ADR_FULL, 
CONTACT, 
HOSPITAL, 
REASON FROM {table}''')

    data = {
        'id района' : [],
        'name' : [] ,
        'Наименование района' : [],
        'СНИЛС родителя' : [],
        'ФИО и дата рождения родителя' : [],
        'Данные ДУЛ родителя' : [],
        'Дата рождения ребенка' : [],
        'Адрес родителя' : [],
        'Контактные данные' : [],
        'Больница' : [],
        'Причина' : [],
            }
    
    for row in curs.fetchall():
        data['id района'].append(row[0]),
        data['name'].append(row[1]),
        data['Наименование района'].append(row[2]),
        data['СНИЛС родителя'].append(row[3]),
        data['ФИО и дата рождения родителя'].append(row[4]),
        data['Данные ДУЛ родителя'].append(row[5]),
        data['Дата рождения ребенка'].append(row[6]),
        data['Адрес родителя'].append(row[7]),
        data['Контактные данные'].append(row[8]),
        data['Больница'].append(row[9]),
        data['Причина'].append(row[10])
        
    if cnt > 0:
        name_def = 'Претенденты на ЭС подарок новорожденному НЕ найдены в ЕГР ЗАГС'
        generating_report_files(data, log, name_def, test, mail)    

#****************************************************************************************************
def zdrav_backup(file):
    new_file_name = f'{today} - {file}'
    if test == 0:
        os.replace(file, f'{path_backup}{new_file_name}')
    writing_to_log_file(log, f'Файл {file} перемещен в {path_backup} и переименован в {new_file_name}')

#****************************************************************************************************    
def main(xl, cnt_file):
    if cnt_file > 0:
        col = ['NOM', 'HOSPITAL', 'SNILS', 'F', 'I', 'O', 'DR', 
                'DUL_TYPE', 'DUL_SER', 'DUL_NOM', 'DUL_PLACE', 'DUL_KEM', 'DUL_DATE', 'DUL_CODE', 
                'BABY_DR', 'ADR_MO', 'ADR_FULL', 'CONTACT', 'REASON']

        xl.columns = col

        xl.dropna(thresh=13, inplace = True)

        for data in xl.itertuples():
            if pd.isna(data[1]):
                xl.drop(index=data[0], inplace = True)


        xl['DR'] = xl['DR'].apply(dat)
        xl['DUL_DATE'] = xl['DUL_DATE'].apply(dat)
        xl['BABY_DR'] = xl['BABY_DR'].apply(dat)
        xl['F'] = xl['F'].apply(up)
        xl['I'] = xl['I'].apply(up)
        xl['O'] = xl['O'].apply(up)
        xl['REGION_ID'] = xl['ADR_MO'].apply(mo_id)
        
        xl = xl.fillna(0)
        
        try:
            zdrav_insert_temp(xl)
        except Exception as e:
            text = f'произошла ошибка при вызове функции zdrav_insert_temp() - {e}'
            alarm_log(mail, log, text)

        try:
            zdrav_new()
        except Exception as e:
            text = f'произошла ошибка при вызове функции zdrav_new() - {e}'
            alarm_log(mail, log, text)

        try:
            zdrav_insert()
        except Exception as e:
            text = f'произошла ошибка при вызове функции zdrav_insert() - {e}'
            alarm_log(mail, log, text)
        
        find_presend()

    #****************************************************************************************************
def find_presend():
    try:
        zdrav_find_egisso()
    except Exception as e:
        text = f'произошла ошибка при вызове функции zdrav_find_egisso() - {e}'
        alarm_log(mail, log, text)

    try:
        zdrav_find_iszn()
    except Exception as e:
        text = f'произошла ошибка при вызове функции zdrav_find_iszn() - {e}'
        alarm_log(mail, log, text)

    try:
        zdrav_not_find_iszn()
    except Exception as e:
        text = f'произошла ошибка при вызове функции zdrav_not_find_iszn() - {e}'
        alarm_log(mail, log, text)

    try:
        zdrav_not_find_egisso()
    except Exception as e:
        text = f'произошла ошибка при вызове функции zdrav_not_find_egisso() - {e}'
        alarm_log(mail, log, text)


#****************************************************************************************************
# goto_folder()

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, log, text)

#****************************************************************************************************
writing_to_log_file(log, '***************************************')
cnt_file = 0
c = os.listdir(os.getcwd())
for file in c:
    if file.endswith(".xlsx") or file.endswith(".xltx"):
        writing_to_log_file(log, f'Файл поступил - {file}')
#         print(file)
        xl = write_file(file, log)
        try:
            backup_file(test, file, log, log, path_backup, path)
            # zdrav_backup(file)
        except Exception as e:
            text = f'произошла ошибка при вызове функции zdrav_backup() - {e}'
            alarm_log(mail, log, text)
        cnt_file += 1
        
        main(xl, cnt_file)

if cnt_file == 0:
    find_presend()
    