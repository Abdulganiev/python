from generating_report_files import *
import pandas as pd

# *****************************************************************
name_def = 'create_EK'
name_log = 'create_EK'
mail = 'IVAbdulganiev@yanao.ru'
alarm_flag = 0

patchs = get_platform()
trek = patchs['trek']

# *****************************************************************
def create_EK_find():
    with open(f'{trek}/create_EK_find.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

# *****************************************************************
def create_EK(data):
    for row in data.itertuples(index=False):
        try:
            with open(f'{trek}/create_EK.sql', 'r', encoding='utf8') as f:
                sql = f.read()
            sql = sql.replace('{region_id}', str(row[0]))
            sql = sql.replace('{people_id}', str(row[1]))
            sql = sql.replace('{ek}', str(row[2]))
            curs.execute(sql)
        except Exception as e:    
            text = f'произошла ошибка при вызове функции create_EK() - {e} - \n {row}'
            writing_to_log_file(name_log, text)

# *****************************************************************
writing_to_log_file(name_log, '***********start**************')

try:
    curs = connect_oracle()
    alarm_flag = 0
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    writing_to_log_file(name_log, text)
    alarm_flag = 1

if alarm_flag == 0:
    try:
        find_ek = create_EK_find()
        alarm_flag = 0
    except Exception as e:    
        text = f'произошла ошибка при вызове функции create_EK_find() - {e}'
        writing_to_log_file(name_log, text)
        alarm_flag = 1

if alarm_flag == 0:
    data = pd.DataFrame(find_ek)

    if len(data) > 0:
        create_EK(data)