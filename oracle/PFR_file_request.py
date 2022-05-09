import jaydebeapi
import json
from generating_report_files import *


path = "access_report.txt"
with open(path) as f:
    access = json.load(f)
    
driver = 'ojdbc14.jar'
path_base = access['path_base']
password = access['password']
login = access['login']
port = access['port']
sid = access['sid']

conn = jaydebeapi.connect(
    'oracle.jdbc.driver.OracleDriver',
    f'jdbc:oracle:thin:{login}/{password}@{path_base}:{port}/{sid}',
    [login, password],
    driver)

curs = conn.cursor()


#***************************************************************
def PFR_file_request_file(pccat_id):
    with open('PFR_file_request_file.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{pccat_id}', f'{pccat_id}')
    curs.execute(sql)
    return curs.fetchall()

def PFR_file_request(pccat_id):
    with open('PFR_file_request.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{pccat_id}', f'{pccat_id}')
    curs.execute(sql)
    return curs.fetchall()

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


root_path = 'PFR'
try:
    shutil.rmtree(root_path, ignore_errors=False, onerror=None)
except:
    pass    
os.mkdir(root_path)


file_name = PFR_file_request_name() # имя файла типа ЗАПРОС
file_zip = f'РСД Запрос {file_name[0]}.zip' # имя архива
report = {} # словарь для записи кол-ва строк для акта

try:
    os.remove(file_zip)
except:
    pass

for key, value in categories.items():
    data = PFR_file_request(value)
    log = key
    key = f'{root_path}/{key}'
    
    try:
        os.mkdir(key) # если каталога нет, то создаем
    except:
        pass
    
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

    report[log] = cnt

text_report = ''
for key, value in report.items():
    text_report += f'{key} - {value} записей\n'

name_log = 'PFR_file_request'
name_def = file_zip
test = 0
mail = 'IVAbdulganiev@yanao.ru'
    
generating_report_files_PFR_2(name_log, name_def, test, mail, text_report)