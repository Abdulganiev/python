from generating_report_files import *
import pandas as pd

#***************************************************************
name_log = 'check_tickets'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'Нет права на авиабилет'
check = 0

#***************************************************************
def check_tickets_category(curs):
    with open('check_tickets_category.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return 0

#***************************************************************
def check_tickets(curs):
    with open('check_tickets.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    data = {
         'id района' : [],
         'name' : [] ,
         'Наименование района' : [],
         'id человека' : [] ,
         'ФИО др' : [] ,
         'Возраст' : [] ,
         'Дата окончания права на покупку билета' : [] ,
         'Дата окончания - Ребёнок до 18 лет (учащ. до 23 лет) в составе семьи «Дети-родители» или «Опекаемые-опекуны» с 3 и более детьми до 18 лет, учащ. до 23 лет' : [] ,
            }
    for row in curs.fetchall():
        data['id района'].append(row[0])
        data['name'].append(row[1])
        data['Наименование района'].append(row[2])
        data['id человека'].append(row[3])
        data['ФИО др'].append(row[4])
        data['Возраст'].append(row[5])
        data['Дата окончания права на покупку билета'].append(row[6])
        data['Дата окончания - Ребёнок до 18 лет (учащ. до 23 лет) в составе семьи «Дети-родители» или «Опекаемые-опекуны» с 3 и более детьми до 18 лет, учащ. до 23 лет'].append(row[7])

    return data

#***************************************************************
goto_folder()

writing_to_log_file(name_log, f'***************************************************************')

try:
    curs = connect_oracle()
    check = 0
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)
    check = 1

if check == 0:
    try:
        check_tickets_category(curs)
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_tickets_category() - {e}'
        alarm_log(mail, name_log, text)
        check = 1

if check == 0:
    try:
        data = pd.DataFrame(check_tickets(curs))
        check = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_tickets() - {e}'
        alarm_log(mail, name_log, text)
        check = 1
    
    if check == 0:
        writing_to_log_file(name_log, f'Количество записей - {len(data)}')
    
        for mo in sorted(set(data['name'])):
            cnt = data[data['name'].isin([mo])].count()[0]
            text = f'{mo} - {cnt} строк'
            writing_to_log_file(name_log, text)
            
        generating_report_files(data, name_log, name_def, test, mail)