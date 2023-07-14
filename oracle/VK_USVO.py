import pandas as pd
import os
from generating_report_files import *

#***************************************************************
log = 'VK_USVO'
mail = 'IVAbdulganiev@yanao.ru'
path = r'd:/python/schedule/vk_usvo/'
test = 1

#***************************************************************    
def vk_insert_temp(xl):
    table = 'uszn.temp$_vk_temp'
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

#****************************************************************************************************
writing_to_log_file(log, '***************************************')
cnt_file = 0
os.chdir(path)
c = os.listdir(os.getcwd())
for file in c:
    if file.endswith(".xlsx") or file.endswith(".xltx"):
        writing_to_log_file(log, f'Файл поступил - {file}')
#         print(file)
        xl = write_file(file)
        try:
            backup_file(test, file, log, log)
        except Exception as e:
            text = f'произошла ошибка при вызове функции backup_file() - {e}'
            alarm_log(mail, log, text)
        cnt_file += 1
        
#****************************************************************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, log, text)

#****************************************************************************************************    
if cnt_file > 0:
    col = ['NOM', 'HOSPITAL', 'SNILS', 'F', 'I', 'O', 'DR', 
            'DUL_TYPE', 'DUL_SER', 'DUL_NOM', 'DUL_PLACE', 'DUL_KEM', 'DUL_DATE', 'DUL_CODE', 
            'BABY_DR', 'ADR_MO', 'ADR_FULL', 'CONTACT', 'REASON']

    xl.columns = col

    xl['DR'] = xl['DR'].apply(dat)
    xl['DUL_DATE'] = xl['DUL_DATE'].apply(dat)
    xl['BABY_DR'] = xl['BABY_DR'].apply(dat)
    xl['F'] = xl['F'].apply(up)
    xl['I'] = xl['I'].apply(up)
    xl['O'] = xl['O'].apply(up)
    xl['REGION_ID'] = xl['ADR_MO'].apply(mo_id)
    
    xl = xl.fillna(0)