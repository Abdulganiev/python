from generating_report_files import *
import re

#***************************************************************
name_log = 'egr_zagz'
name_def = 'Данные ЕГР ЗАГС'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def dat(x):
    try:
        x = str(x).replace(' 00:00:00', '')
        return re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3.\2.\1', x)
    except:
        return x

#***************************************************************
def zags_sm(curs):
    # with open('egr_zagz_preliminary.sql', 'r', encoding='utf8') as f:
    #     sql = f.read()
    # curs.execute(sql)

    with open('egr_zagz_find.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

    data = {
         'name' : [],
         'id+МО' : [] ,
         'ФИО и д.р' : [] ,
         'ФИО и д.р из свидетельства о смерти' : [],
         'Дата смерти из свидетельства о смерти' : [],
         'Дата смерти 2 из свидетельства о смерти' : [],
         'Дата акта записи' : [],
         'Номер акта записи' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['id+МО'].append(row[1])
        data['ФИО и д.р'].append(row[3])
        data['ФИО и д.р из свидетельства о смерти'].append(row[6])
        data['Дата смерти из свидетельства о смерти'].append(dat(row[7]))
        data['Дата смерти 2 из свидетельства о смерти'].append(row[8])
        data['Дата акта записи'].append(dat(row[9]))
        data['Номер акта записи'].append(row[10])
    
    return data

#***************************************************************
writing_to_log_file(name_log, f'******start***********************************')

try:
    curs = connect_oracle()
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    data = zags_sm(curs)
except Exception as e:    
    text = f'произошла ошибка при вызове функции zags_sm() - {e}'
    alarm_log(mail, name_log, text)

try:
    generating_report_files(data, name_log, name_def, test, mail)
    # writing_to_log_file(name_log, f'{data}')
except Exception as e:    
    text = f'произошла ошибка при вызове функции generating_report_files() - {e}'
    # text = f'произошла ошибка при вызове функции generating_report_files() - {e} \n {data}'
    alarm_log(mail, name_log, text)   

writing_to_log_file(name_log, f'******end************************************')