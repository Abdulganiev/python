from generating_report_files import *
import pandas as pd
import time

#**************************************************
name_log = 'pfr_work'
mail = 'IVAbdulganiev@yanao.ru'

#**************************************************
def search_messages(curs):
    with open('pfr_work_find.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    df = curs.fetchall()
    return df

#**************************************************
def processing(curs, region_id, id):
    with open('pfr_work_check.sql', 'r', encoding='utf8') as f:
        sql = f.read()
        sql = sql.replace('{id}', f'{id}')
    curs.execute(sql)    
    
    cnt = int(curs.fetchall()[0][0])
    
    if cnt == 0:
        with open('pfr_work_preliminary.sql', 'r', encoding='utf8') as f:
            sql = f.read()
        sql = sql.replace('{region_id}', f'{region_id}')
        sql = sql.replace('{id}', f'{id}')
        curs.execute(sql)

        with open('pfr_work_insert.sql', 'r', encoding='utf8') as f:
            sql = f.read()
        curs.execute(sql)
        return 1
    return 0

#**************************************************        
def pfr_work_cnt(curs):
    with open('pfr_work_cnt.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return int(curs.fetchall()[0][0])

#*********************************************
goto_folder()

writing_to_log_file(name_log, '*******start*************************************')

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)    

try:
    data = pd.DataFrame(search_messages(curs))
except Exception as e:    
    text = f'произошла ошибка при вызове функции search_messages() - {e}'
    alarm_log(mail, name_log, text)    

cnt_data = len(data)

try:
    dt = pfr_work_cnt(curs)
except Exception as e:    
    text = f'произошла ошибка при вызове функции pfr_work_cnt() - {e}'
    alarm_log(mail, name_log, text)    

text = f'{cnt_data} - {dt}'
writing_to_log_file(name_log, text)

#*********************************************
i = 0
cnt = 0
start_time = time.time()
start_time_1 = time.time()

#*********************************************
for row in data.itertuples(index=False):
    try:
        cnt += processing(curs, row[0], row[1])
    except Exception as e:
        text = f'произошла ошибка при вызове функции processing() - {e}'
        alarm_log(mail, name_log, text)
    i += 1
    if i == 100:
        time_delta_sec = time.time() - start_time
        time_delta_min = time_delta_sec / 60
        text = f'--- {time_delta_sec} sec --- {time_delta_min} min ---'
        writing_to_log_file(name_log, text)
        
        try:
            dt = pfr_work_cnt(curs)
        except Exception as e:    
            text = f'произошла ошибка при вызове функции pfr_work_cnt() - {e}'
            alarm_log(mail, name_log, text)    

        text = f'{i} - {dt}'
        writing_to_log_file(name_log, text)
        
        i = 0
        start_time = time.time()
        
#*********************************************
time_delta_sec = time.time() - start_time
time_delta_min = time_delta_sec / 60
text = f'--- {time_delta_sec} sec --- {time_delta_min} min ---'
writing_to_log_file(name_log, text)      

cnt_data = len(data)

try:
    dt = pfr_work_cnt(curs)
except Exception as e:    
    text = f'произошла ошибка при вызове функции pfr_work_cnt() - {e}'
    alarm_log(mail, name_log, text)    

text = f'{cnt_data} - {dt}. Обработано {cnt} сообщений'
writing_to_log_file(name_log, text)

writing_to_log_file(name_log, 'end')