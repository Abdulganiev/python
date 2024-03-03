from generating_report_files import *

#***************************************************************
name_log = 'duplicates_people'
name_def = 'Дубликаты людей'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
cnt = 0

#***************************************************************
def duplicates_people(region_id):
    with open('duplicates_people.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{region_id}', f'{region_id}')
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
goto_folder()

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)    

writing_to_log_file(name_log, f'***************************************')
writing_to_log_file(name_log, f'Подключение к базе')

data = {
    'name' : [],
    'МО' : [],
    'id' : [],
    'Описание человека' : []
    }

for region_id in range(58, 71):
    try:
        d = duplicates_people(region_id)
    except:
        text = f'произошла ошибка при вызове функции duplicates_people - {e}'
        alarm_log(mail, name_log, text)

    for row in d:
        data['name'].append(row[0])
        data['МО'].append(row[1])
        data['id'].append(row[2])
        data['Описание человека'].append(row[3])
        cnt += 1

if cnt > 0:
    generating_report_files(data, name_log, name_def, test, mail)