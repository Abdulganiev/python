import os
from datetime import datetime
from generating_report_files import *

#***************************************************************
name_log = 'ES_milk'
name_def = 'ES_milk'
mail = 'IVAbdulganiev@yanao.ru'
today = datetime.now().strftime('%d.%m.%Y')
test = 0
chech_alarm = 0

patchs = get_platform()
trek = patchs['trek']

path_backup = f'{trek}/backup/ES_milk/'
path = patchs['milk']

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
    
#***************************************************************    
def table_delete(table):
    writing_to_log_file(name_log, f'Очистка таблицы {table}')
    try:
        sql = f'delete from {table}'
        curs.execute(sql)
        text = f'данные из таблицы {table} удалены'
    except:
        text = f'таблицы {table} нету - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************    
def table_drop(table):
    writing_to_log_file(name_log, f'Удаление таблицы {table}')
    try:
        sql = f'drop table {table}'
        curs.execute(sql)
        text = f'Таблица {table} удалена'
    except:
        text = f'таблицы {table} нету - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************    
def zdrav_milk_new():
    writing_to_log_file(name_log, '-------------')
    table = 'uszn.temp$_zdrav_milk_new'
    writing_to_log_file(name_log, f'Загрузка данных в {table}')
    table_drop(table)
    
    sql=f'create table {table} as select t1.* from uszn.temp$_zdrav_milk_temp t1'
    curs.execute(sql)
    
    writing_to_log_file(name_log, f'Количество записей в {table} после загрузки')
    table_cnt(table)
    
#***************************************************************    
def zdrav_milk_insert_temp(xl):
    writing_to_log_file(name_log, '-------------')
    table = 'uszn.temp$_zdrav_milk_temp'
    table_delete(table)
    writing_to_log_file(name_log, f'Загрузка данных в {table}')
    writing_to_log_file(name_log, f'Количество записей в {table} до загрузки')
    table_cnt(table)

    columns = '(' + ', '.join(list(xl)) + ')'
    question = 'values(' + ', '.join(list('?' * len(list(xl)))) + ')'
    sql = f'INSERT INTO {table} {columns} {question}'
        
    for data in xl.itertuples(index=False):
        try:
            curs.execute(f'{sql}', list(data))
        except Exception as e:
            text = f'произошла ошибка при вызове функции connect_oracle() - {e} \n {sql} \n {list(data)}'
            writing_to_log_file(name_log, text)
            return 1
   
    writing_to_log_file(name_log, f'Количество записей в {table} после загрузки')
    table_cnt(table)
    return 0

#***************************************************************    
def zdrav_milk_insert():
    writing_to_log_file(name_log, '-------------')
    table = 'uszn.temp$_zdrav_milk'

    writing_to_log_file(name_log, f'Загрузка данных в {table}')
    writing_to_log_file(name_log, f'Количество записей в {table} до загрузки')
    table_cnt(table)

    sql = f'INSERT INTO {table} select t1.* from uszn.temp$_zdrav_milk_temp t1'
    curs.execute(f'{sql}')
        
    writing_to_log_file(name_log, f'Количество записей в {table} после загрузки')
    table_cnt(table)
    
#***************************************************************    
def zdrav_milk_processing(xl, file):
    writing_to_log_file(name_log, '-------------')
    writing_to_log_file(name_log, 'Предварительная обработка данных')
    col = ['NOM', 'HOSPITAL', 
           'SNILS', 'last_name', 'first_name', 'middle_name', 'birth_date',
           'DUL_TYPE', 'DUL_SER', 'DUL_NOM', 'DUL_PLACE', 'DUL_KEM', 'DUL_DATE', 'DUL_CODE', 
           'BABY_SNILS', 'BABY_last_name', 'BABY_first_name', 'BABY_middle_name', 'BABY_birth_date',
           'BABY_DUL_TYPE', 'BABY_DUL_SER', 'BABY_DUL_NOM', 'BABY_DUL_PLACE', 'BABY_DUL_KEM', 'BABY_DUL_DATE', 
           'ADR_MO', 'ADR_FULL', 
           'CONTACT', 'CAT', 'DATE_START', 'DATE_END']
    xl.columns = col
    xl.dropna(thresh=13, inplace = True)
    for data in xl.itertuples():
        if pd.isna(data[1]):
            xl.drop(index=data[0], inplace = True)
   
    xl['birth_date'] = xl['birth_date'].apply(dat)
    xl['DUL_DATE'] = xl['DUL_DATE'].apply(dat)
    xl['BABY_birth_date'] = xl['BABY_birth_date'].apply(dat)
    xl['BABY_DUL_DATE'] = xl['BABY_DUL_DATE'].apply(dat)
    xl['DATE_START'] = xl['DATE_START'].apply(dat)
    xl['DATE_END'] = xl['DATE_END'].apply(dat)

    xl['REGION_ID'] = xl['ADR_MO'].apply(mo_id)
    xl['BABY_last_name'] = xl['BABY_last_name'].apply(replace_nan)
    xl['BABY_first_name'] = xl['BABY_first_name'].apply(replace_nan)
    xl['BABY_middle_name'] = xl['BABY_middle_name'].apply(replace_nan)
    xl['BABY_birth_date'] = xl['BABY_birth_date'].apply(replace_nan)
    xl['BABY_DUL_TYPE'] = xl['BABY_DUL_TYPE'].apply(replace_nan)
    xl['BABY_DUL_SER'] = xl['BABY_DUL_SER'].apply(replace_nan)
    xl['BABY_DUL_NOM'] = xl['BABY_DUL_NOM'].apply(replace_nan)
    xl['BABY_DUL_PLACE'] = xl['BABY_DUL_PLACE'].apply(replace_nan)
    xl['BABY_DUL_KEM'] = xl['BABY_DUL_KEM'].apply(replace_nan)
    xl['BABY_DUL_DATE'] = xl['BABY_DUL_DATE'].apply(replace_nan)
    
    xl['FILE_LOAD'] = f'{file}'
    xl['DATE_LOAD'] = f'{today}'
    
    xl = xl.fillna('')
    
    return xl

#***************************************************************    
def zdrav_milk_to_mo():
    path = trek
    writing_to_log_file(name_log, '-------------')
    writing_to_log_file(name_log, 'Формирование отчета в УСЗН')
    
    with open(f'{path}/ES_milk.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    d = curs.fetchall()
    
    data = {
        'name' : [],
        'Наименование больницы' : [],
        'СНИЛС родителя' : [],
        'ФИО и дата рождения родителя' : [],
        'ДУЛ родителя' : [],
        'СНИЛС ребёнка' : [],
        'ФИО и дата рождения ребёнка' : [],
        'ДУЛ ребёнка' : [],
        'Адрес' : [],
        'Контактный телефон родителя' : [],
        'Категория получателя электронного сертификата' : [],
        'Период - Дата начала' : [],
        'Период - Дата окончания' : [],
        }
    for row in d:
        data['name'].append(row[0])
        data['Наименование больницы'].append(row[1])
        data['СНИЛС родителя'].append(row[2])
        data['ФИО и дата рождения родителя'].append(row[3])
        data['ДУЛ родителя'].append(row[4])
        data['СНИЛС ребёнка'].append(row[5])
        data['ФИО и дата рождения ребёнка'].append(row[6])
        data['ДУЛ ребёнка'].append(row[7])
        data['Адрес'].append(row[8])
        data['Контактный телефон родителя'].append(row[9])
        data['Категория получателя электронного сертификата'].append(row[10])
        data['Период - Дата начала'].append(row[11])
        data['Период - Дата окончания'].append(row[12])
        
    generating_report_files(data, name_log, name_def, test, mail)

# *************************************************
#goto_folder()

os.chdir(path)

writing_to_log_file(name_log, '***************************************')

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)
    
cnt_file = 0

c = os.listdir(os.getcwd())

for file in c:
    if file.endswith(".xlsx") or file.endswith(".xltx"):
        writing_to_log_file(name_log, f'Папка {path}')
        writing_to_log_file(name_log, f'Файл поступил - {file}')
        
        try:
            xl = write_file_object(file, name_log)
            chech_alarm = 0
        except Exception as e:
            text = f'произошла ошибка при вызове функции write_file_object() - {e}'
            alarm_log(mail, name_log, text)
            chech_alarm = 1            
        
        if chech_alarm == 0:
            try:
                xl = zdrav_milk_processing(xl, file)
                chech_alarm = 0
            except Exception as e:
                text = f'произошла ошибка при вызове функции zdrav_milk_processing() - {e}'
                alarm_log(mail, name_log, text)
                chech_alarm = 1            

        if chech_alarm == 0:
            try:
                chech_alarm = zdrav_milk_insert_temp(xl)
            except Exception as e:
                text = f'произошла ошибка при вызове функции zdrav_milk_insert_temp() - {e}'
                alarm_log(mail, name_log, text)
                chech_alarm = 1            

        if chech_alarm == 0:
            try:
                zdrav_milk_new()
                chech_alarm = 0
            except Exception as e:
                text = f'произошла ошибка при вызове функции zdrav_milk_new() - {e}'
                alarm_log(mail, name_log, text)
                chech_alarm = 1            
                
        if chech_alarm == 0:
            try:
                zdrav_milk_insert()
                chech_alarm = 0
            except Exception as e:
                text = f'произошла ошибка при вызове функции zdrav_milk_insert() - {e}'
                alarm_log(mail, name_log, text)
                chech_alarm = 1            

        if chech_alarm == 0:
            try:
                backup_file(test, file, name_log, name_def, path_backup, path)
                chech_alarm = 0
            except Exception as e:
                text = f'произошла ошибка при вызове функции backup_file() - {e}'
                alarm_log(mail, name_log, text)
                chech_alarm = 1

        if chech_alarm == 0:
            try:
                zdrav_milk_to_mo()
                chech_alarm = 0
            except Exception as e:
                text = f'произошла ошибка при вызове функции zdrav_milk_to_mo() - {e}'
                alarm_log(mail, name_log, text)
                chech_alarm = 1

        if chech_alarm == 0:
            writing_to_log_file(name_log, 'Обработка завершена')