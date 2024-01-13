from generating_report_files import *

#***************************************************************
name_log = 'check_ES_alarm_MIR'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'Неверный номер карты МИР для ЭС'
check = 0

#***************************************************************
def check_ES_alarm_MIR(curs):
    with open('check_ES_alarm_MIR.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

    data = {
         'id района' : [],
         'name' : [] ,
         'Наименование района' : [],
         'Тип сертификата' : [],
         'id получателя' : [] ,
         'Описание получателя' : [] ,
         'id субъекта' : [] ,
         'Описание субъекта' : [] ,
         'Статус сертификата' : [] ,
         'Описание ошибки' : [] ,
         'Дата ошибки' : [] ,
            }

    for row in curs.fetchall():
        data['id района'].append(row[0])
        data['name'].append(row[1])
        data['Наименование района'].append(row[2])
        data['Тип сертификата'].append(row[3])
        data['id получателя'].append(row[4])
        data['Описание получателя'].append(row[5])
        data['id субъекта'].append(row[6])
        data['Описание субъекта'].append(row[7])
        data['Статус сертификата'].append(row[8])
        data['Описание ошибки'].append(row[9])
        data['Дата ошибки'].append(row[10])
        
    return data

#***************************************************************
writing_to_log_file(name_log, f'************************start***************************************')
try:
    curs = connect_oracle()
    check = 0
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)
    check = 1

if check == 0:
    try:
        data = pd.DataFrame(check_ES_alarm_MIR(curs))
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_ES_alarm_MIR() - {e}'
        alarm_log(mail, name_log, text)
        check == 1
        
    if check == 0:
        writing_to_log_file(name_log, f'Количество записей - {len(data)}')
    
        for mo in sorted(set(data['name'])):
            cnt = data[data['name'].isin([mo])].count()[0]
            text = f'{mo} - {cnt} строк'
            writing_to_log_file(name_log, text)
            
        generating_report_files(data, name_log, name_def, test, mail)

writing_to_log_file(name_log, f'************************end****************************************')