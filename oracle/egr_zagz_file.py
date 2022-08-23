from generating_report_files import *
import os, shutil
import pandas as pd

#***************************************************************
name_log = 'egr_zagz_file'
name_def = 'Данные ЕГР ЗАГС файл'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
file_name = name_log + '.xml' # имя файла

#***************************************************************
def zags_sm(curs):
    with open('egr_zagz_file_find.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
writing_to_log_file(name_log, f'********start*********************************')

try:
    curs = connect_oracle()
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    df = pd.DataFrame(zags_sm(curs))
except Exception as e:    
    text = f'произошла ошибка при вызове функции zags_sm() - {e}'
    alarm_log(mail, name_log, text)
    cnt = 0

try:
    cnt = len(df)
except Exception as e:    
    text = f'произошла ошибка cnt = len(df) - {e}'
    writing_to_log_file(name_log, text)
    cnt = 0

if cnt > 0:
    with open(file_name, 'w', encoding='utf8') as f: # запись в файл первых строки
        text = '<?xml version="1.0" encoding="UTF-8" ?>'
        f.write(text + '\n')
        text = '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">'
        f.write(text + '\n')
    
    for row in df.itertuples(index=False):
        with open('egr_zagz_file_text.xml', 'r', encoding='utf8') as f:
            text = f.read()
        text = text.replace('{last_name}', row[0])
        text = text.replace('{first_name}', row[1])
        text = text.replace('{middle_name}', row[2])
        text = text.replace('{birth_date}', row[3])
        text = text.replace('{death_date_egisso}', row[4])
        text = text.replace('{az_date}', row[5])
        text = text.replace('{az_num}', row[6])
        text = text.replace('{zagz_status}', row[7])
        text = text.replace('{ZAGZ}', row[8])
        text = text.replace('{sv_ser}', row[9])
        text = text.replace('{sv_num}', row[10])
        text = text.replace('{sv_date}', row[11])
        text = text.replace('{death_place}', row[12])                
        with open(file_name, 'a+', encoding='utf8') as f: # запись в файл текста
            f.write(text + '\n')

    with open(file_name, 'a+', encoding='utf8') as f: # запись в файл последней строки
        text = '</SOAP-ENV:Envelope>'
        f.write(text)

    try:
        os.remove(f'y:/{file_name}')
    except Exception as e:
        text = f'os.remove - {e}'
        writing_to_log_file(name_log, text)

    try:
        shutil.move(file_name, 'y:/')
    except Exception as e:
        text = f'произошла ошибка shutil.move - {e}'
        writing_to_log_file(name_log, text)

writing_to_log_file(name_log, f'количество записей - {cnt}')
writing_to_log_file(name_log, 'end')