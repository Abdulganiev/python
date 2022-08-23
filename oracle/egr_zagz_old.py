from generating_report_files import *

#***************************************************************
name_log = 'zags_sm'
name_def = 'Данные ЕГР ЗАГС'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def zags_sm(curs):
    with open('egr_zagz_preliminary.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

    with open('egr_zagz_find.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

    data = {
         'name' : [],
         'id+МО' : [] ,
         'id человека' : [] ,
         'ФИО и д.р' : [] ,
         'Дата смерти' : [] ,
         'Дата снятия с учёта' : [],
         'ФИО и д.р из свидетельства' : [],
         'Дата смерти из свидетельства' : [],
         'Дата смерти 2 из свидетельства' : [],
         'Дата акта свидетельства' : [],
         'Номер акта свидетельства' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['id+МО'].append(row[1])
        data['id человека'].append(row[2])
        data['ФИО и д.р'].append(row[3])
        data['Дата смерти'].append(row[4])
        data['Дата снятия с учёта'].append(row[5])
        data['ФИО и д.р из свидетельства'].append(row[6])
        data['Дата смерти из свидетельства'].append(row[7])
        data['Дата смерти 2 из свидетельства'].append(row[8])
        data['Дата акта свидетельства'].append(row[9])
        data['Номер акта свидетельства'].append(row[10])
    
    return data

#***************************************************************
writing_to_log_file(name_log, f'*********************************************')

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
except Exception as e:    
    text = f'произошла ошибка при вызове функции generating_report_files() - {e}'
    alarm_log(mail, name_log, text)   
