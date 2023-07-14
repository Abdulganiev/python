from generating_report_files import *

#***************************************************************
name_log = 'PFR_file_6531'
name_def = file_zip
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def PFR_file_request():
    with open('PFR_file_6531.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
def PFR_file_request_name():
    curs.execute("""select 
        '030'||To_Char(TRUNC(SYSDATE), 'y')||To_Char(TRUNC(SYSDATE), 'mm')||'1.000' 
        from dual""")
    return curs.fetchone()

#***************************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    file_name = PFR_file_request_name() # имя файла типа ЗАПРОС
except Exception as e:
    text = f'произошла ошибка при вызове функции PFR_file_request_name() - {e}'
    alarm_log(mail, name_log, text)

try:
    file_zip = f'Запрос 6_5_3_1 {file_name[0]}.zip' # имя архива
    os.remove(file_zip)
except:
    pass

try:
    data = PFR_file_request()
except Exception as e:
    text = f'произошла ошибка при вызове функции PFR_file_request() - {e}'
    alarm_log(mail, name_log, text)
    
path = f'{file_name[0]}' # путь к файлу
    
with open(path, 'w', encoding='IBM866') as f: # запись в файл первой строки
    text = 'В1.0       '
    f.write(text + '\n')
    
cnt = 0 # считаем строки
for row in data:
    with open(path, 'a+', encoding='IBM866') as f: # запись в файл строки
        f.write(row[0] + '\n')
    cnt += 1 # считаем строки
    
with zipfile.ZipFile(file_zip, 'a') as myzip:
    myzip.write(path)

text = f'Количество строк в файле - {cnt}'
    
generating_report_files_PFR_2(name_log, name_def, test, mail, text)