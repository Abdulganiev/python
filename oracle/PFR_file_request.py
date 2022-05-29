from generating_report_files import *

#***************************************************************
name_log = 'PFR_file_request'
test = 0
mail = 'IVAbdulganiev@yanao.ru,AVShashkov@yanao.ru'
root_path = 'PFR'

#***************************************************************
writing_to_log_file(name_log, f'***************************************************************')

curs = connect_oracle()
writing_to_log_file(name_log, f'к базе подключился')

#***************************************************************
def PFR_file_request_file(pccat_id):
    with open('PFR_file_request_file.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{pccat_id}', f'{pccat_id}')
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
def PFR_file_request(pccat_id):
    with open('PFR_file_request.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{pccat_id}', f'{pccat_id}')
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
def PFR_file_request_name():
    curs.execute("""select 
        '0302'||To_Char(TRUNC(LAST_DAY(SYSDATE))+1, 'y')||To_Char(TRUNC(LAST_DAY(SYSDATE))+1, 'mm')||'1.000' 
        from dual""")
    return curs.fetchone()

#***************************************************************
cats_id = [731,732,725,723,727,730,724,728,1108,729,726,1116,1109]
categories = {}
for cat_id in cats_id:
    cat_name_id = PFR_file_request_file(cat_id)
    if len(cat_name_id) != 0:
        name_cat, id = cat_name_id[0]
        categories[name_cat] = id
writing_to_log_file(name_log, f'категории считал')

#***************************************************************
try:
    shutil.rmtree(root_path, ignore_errors=False, onerror=None)
    writing_to_log_file(name_log, f'папку {root_path} удалил')
except Exception as e:
    writing_to_log_file(name_log, f'при удалении папки {root_path} произошла ошибка {e}')    
os.mkdir(root_path)
writing_to_log_file(name_log, f'папку {root_path} создал')

#***************************************************************
file_name = PFR_file_request_name() # имя файла типа ЗАПРОС
writing_to_log_file(name_log, f'получил имя файла - {file_name[0]}')

file_zip = f'РСД Запрос {file_name[0]}.zip' # имя архива
writing_to_log_file(name_log, f'получил имя архива - {file_zip}')

#***************************************************************
try:
    os.remove(file_zip)
    writing_to_log_file(name_log, f'если есть архив {file_zip}, то его удалил')
except Exception as e:
    writing_to_log_file(name_log, f'архива {file_zip} нет, удалять нечего - {e}')

#***************************************************************
report = {} # словарь для записи кол-ва строк для акта
for key, value in categories.items():
    data = PFR_file_request(value)
    log = key
    key = f'{root_path}/{key}'
    
    try:
        os.mkdir(key) # если каталога нет, то создаем
        writing_to_log_file(name_log, f'создал папку {key}')
    except Exception as e:
        writing_to_log_file(name_log, f'ошибка при создании папки {key} - {e}')
    
    path = f'{key}/{file_name[0]}' # путь к файлу
    
    with open(path, 'w', encoding='IBM866') as f: # запись в файл первой строки
        text = 'В6.2.4     030-001-005119ДЕПАРТАМЕНТ СОЦИАЛЬНОЙ ЗАЩИТЫ НАСЕЛЕНИЯ ЯНАО                                                        ЗАПРОС030-007-00000001'
        f.write(text + '\n')
    
    cnt = 0 # считаем строки
    for row in data:
        with open(path, 'a+', encoding='IBM866') as f: # запись в файл строки
            f.write(row[0] + '\n')
        cnt += 1 # считаем строки
    
    with zipfile.ZipFile(file_zip, 'a') as myzip:
        myzip.write(path)
        writing_to_log_file(name_log, f'добавляем {path} в {file_zip}, количество записей - {cnt}')

    report[log] = cnt

#***************************************************************
text_report = ''
for key, value in report.items():
    text_report += f'{key} - {value} записей\n'

writing_to_log_file(name_log, f'адрес для отправки - {mail}, file_zip - {file_zip}, test - {test}, \n text_report \n {text_report}')
writing_to_log_file(name_log, f'вызов функции "generating_report_files_PFR_2()"')
generating_report_files_PFR_2(name_log, file_zip, test, mail, text_report)