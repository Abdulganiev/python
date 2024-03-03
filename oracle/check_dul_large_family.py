from generating_report_files import *

#***************************************************************
name_log = 'check_dul_large_family'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'У многодетных неправильный ДУЛ'
check = 0

#***************************************************************
def check_dul_large_family(curs):
    with open('check_dul_large_family.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)

    data = {
         'id района' : [],
         'name' : [] ,
         'Наименование района' : [],
         'id человека' : [] ,
         'ФИО др' : [] ,
         'Тип ДУЛ' : [] ,
         'Описание ДУЛ' : [] ,
            }
    for row in curs.fetchall():
        data['id района'].append(row[0])
        data['name'].append(row[1])
        data['Наименование района'].append(row[2])
        data['id человека'].append(row[3])
        data['ФИО др'].append(row[4])
        data['Тип ДУЛ'].append(row[5])
        data['Описание ДУЛ'].append(row[6])

    return data

#***************************************************************
goto_folder()

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
        data = pd.DataFrame(check_dul_large_family(curs))
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_dul_large_family() - {e}'
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