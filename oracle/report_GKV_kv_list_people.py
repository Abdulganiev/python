from generating_report_files import *

#***************************************************************
name_log = 'report_GKV_kv_list_people'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
root_path = 'PFR_kv'

#***************************************************************
writing_to_log_file(name_log, f'***************************************************************')

curs = connect_oracle()
writing_to_log_file(name_log, f'к базе подключился')

#***************************************************************
def report_GKV_kv_list_people_file(region_id):
    with open('report_GKV_kv_list_people_file.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{region_id}', f'{region_id}')
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
def report_GKV_kv_list_people_B():
    with open('report_GKV_kv_list_people_B.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
def report_GKV_kv_list_people_O(region_id):
    with open('report_GKV_kv_list_people_O.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{region_id}', f'{region_id}')
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
def report_GKV_kv_list_people_J(region_id, people_id):
    with open('report_GKV_kv_list_people_J.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{region_id}', f'{region_id}')
    sql = sql.replace('{people_id}', f'{people_id}')
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
def report_GKV_name():
    curs.execute("SELECT to_char(TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q'),'Q')||' кв '||to_char(TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q'),'YYYY') FROM dual")
    return curs.fetchone()

#***************************************************************
goto_folder()

try: # очистка временной папки
    shutil.rmtree(root_path, ignore_errors=False, onerror=None)
    writing_to_log_file(name_log, f'папку {root_path} удалил')
except Exception as e:
    writing_to_log_file(name_log, f'при удалении папки {root_path} произошла ошибка {e}')    
os.mkdir(root_path)
writing_to_log_file(name_log, f'папку {root_path} создал')

#***************************************************************
file_zip = report_GKV_name()
file_zip = f'ЖКВ реестр за {file_zip[0]}.zip' # имя архива

#***************************************************************
report = {} # словарь для записи кол-ва строк

if test == 0:
    range_ = range(58, 71)
else:
    range_ = range(59, 60)

for region_id in range_:

    file_name = report_GKV_kv_list_people_file(region_id) # имя файла типа ЗАПРОС
    file_name = file_name[0][0]
    writing_to_log_file(name_log, f'получил имя файла - {file_name}')
    path = f'{root_path}/{file_name}' # путь к файлу
    writing_to_log_file(name_log, f'путь к файлу - {path}')
    with open(path, 'w', encoding='IBM866') as f: # запись в файл первой строки
        text = report_GKV_kv_list_people_B()
        text = text[0][0]
        f.write(text + '\n')

    data_O = report_GKV_kv_list_people_O(region_id)
    cnt = 0 # считаем строки
    for row in data_O:
        with open(path, 'a+', encoding='IBM866') as f: # запись в файл строки
            f.write(row[0] + '\n')
            people_id = row[1]
            data_J = report_GKV_kv_list_people_J(region_id, people_id)
            for J in data_J:
                f.write(J[0] + '\n')
        cnt += 1 # считаем строки
    report[region_id] = cnt

    with zipfile.ZipFile(file_zip, 'a') as myzip:
        myzip.write(path)
        writing_to_log_file(name_log, f'добавляем {path} в {file_zip}, количество записей - {cnt}')

#***************************************************************

text_report = ''
for key, value in report.items():
    text_report += f'{key} - {value} записей\n'

generating_list_GKV_kv(name_log, text_report, file_zip, test, mail)
