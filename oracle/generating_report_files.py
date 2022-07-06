import shutil, zipfile, os, jaydebeapi, json
import pandas as pd
from pandas.io.excel import ExcelWriter
from datetime import datetime
import datetime as dt

import smtplib # Импортируем библиотеку по работе с SMTP
# Добавляем необходимые подклассы - MIME-типы
import mimetypes # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders # Импортируем энкодер
from email.mime.base import MIMEBase # Общий тип
from email.mime.text import MIMEText # Текст/HTML
from email.mime.image import MIMEImage # Изображения
from email.mime.audio import MIMEAudio # Аудио
from email.mime.multipart import MIMEMultipart # Многокомпонентный объект

# *****************************************************************
def generating_list_GKV_kv(name_log, text, file_name, test, mail):
    today = dt.date.today()
    new_file_name = f'{today} - {file_name}'
    text = f'mail - {mail} \n{text}'

    send_email(mail, file_name, msg_text=text, files=[file_name])
    os.replace(file_name, f'backup/{new_file_name}') 
    writing_to_log_file(name_log, text)

# *****************************************************************
def generating_report_GKV_kv(df, name_log, name, region_id, test):
    data = pd.DataFrame(df)
    today = dt.date.today()
    mail = 'IVAbdulganiev@yanao.ru'
    file_name = f'отчет ЖКВ {name}.xlsx'
    text = f'{file_name} за МО - {region_id} на {today}'
    new_file_name = f'{today} - {file_name}'

    if region_id == '58':
        with ExcelWriter(file_name) as writer: 
            data.to_excel(writer, sheet_name=f'{region_id}', index=False)
    else:
        with ExcelWriter(file_name, engine='openpyxl', mode='a') as writer: 
            data.to_excel(writer, sheet_name=f'{region_id}', index=False)

    if test == 0 and region_id == '70':
        send_email(mail, text, msg_text=file_name, files=[file_name])
    if region_id == '70':
        os.replace(file_name, f'backup/{new_file_name}') 

    writing_to_log_file(name_log, text)

# *****************************************************************
def generating_report_GKV(df, name_log, name, test):
    data = pd.DataFrame(df)

    today = dt.date.today()
    first = today.replace(day=1)
    lastMonth = first - dt.timedelta(days=1)
    date_report = lastMonth.strftime('%m.%Y')
    file_name = f'отчет ЖКВ за {date_report} {name}.xlsx'
    
    data.to_excel(file_name, index=False)

    if test == 1:
        mail = 'IVAbdulganiev@yanao.ru'
    else:
        mail = 'IVAbdulganiev@yanao.ru, MSNesteruk@yanao.ru'

    text = f'{file_name} на {today}'

    send_email(mail, text, msg_text=file_name, files=[file_name])

    new_file_name = f'{today} - {file_name}'
    os.replace(file_name, f'backup/{new_file_name}') 

    writing_to_log_file(name_log, text)      

# *****************************************************************
def send_email(addr_to, msg_subj, msg_text='', files=[]):
    writing_to_log_file('smtp.txt', '*********************************************')
    writing_to_log_file('smtp.txt', 'Вызов функции send_email')
    writing_to_log_file('smtp.txt', f'Отправка письма {addr_to} с темой "{msg_subj}"')
    # '''Функция по отпрвке писем через smtp.yanao.ru. 
    #    Логин, пароль и сервер указываются в файле access_mail.txt.
    #    addr_to - указать адресата (обязательно).
    #    msg_subj - указать тему (обязательно).
    #    msg_text - указать текст письма (необязательно).
    #    files - указать файлы в виде ['файл 1', 'файл 2', и т.д.] (необязательно).
    # '''
    path = 'access_mail.txt'
    with open(path) as f:
        access = json.load(f)
    
    server = access['server'] # сервер отправки
    addr_from = access['user'] # Отправитель
    password  = access['passwd'] # Пароль

    msg = MIMEMultipart() # Создаем сообщение
    msg['From']    = addr_from # Адресат
    msg['To']      = addr_to # Получатель
    msg['Subject'] = msg_subj # Тема сообщения

    body = msg_text # Текст сообщения
    msg.attach(MIMEText(body, 'plain')) # Добавляем в сообщение текст

    process_attachement(msg, files)

    try:
        # подключаемся к почтовому сервису
        smtp = smtplib.SMTP(server) # Создаем объект SMTP
        writing_to_log_file('smtp.txt', f'Подлючение к серверу {server}')
#         smtp.set_debuglevel(1) # журнал, при необходимости включаем
#         smtp.set_debuglevel(True) # Включаем режим отладки, если не нужен - можно закомментировать
        smtp.starttls() # Начинаем шифрованный обмен по TLS
        smtp.ehlo()
        # логинимся на почтовом сервере
        smtp.login(addr_from, password) # Получаем доступ
        smtp.send_message(msg) # Отправляем сообщение
        writing_to_log_file('smtp.txt', 'Письмо отправлено')
    except smtplib.SMTPException as err:
        writing_to_log_file('smtp.txt', f'Ошибка подлючения к серверу {server} - {err}')
        # print('Что - то пошло не так...')
        raise err
    finally:
        smtp.quit()


def process_attachement(msg, files):                        # Функция по обработке списка, добавляемых к сообщению файлов
    writing_to_log_file('smtp.txt', 'Вызов функции process_attachement')
    # '''Функция по обработке списка, добавляемых к сообщению файлов'''
    for f in files:
        if os.path.isfile(f):                               # Если файл существует
            attach_file(msg, f)                             # Добавляем файл к сообщению
        elif os.path.exists(f):                             # Если путь не файл и существует, значит - папка
            dir = os.listdir(f)                             # Получаем список файлов в папке
            for file in dir:                                # Перебираем все файлы и...
                attach_file(msg, f+"/"+file)                # ...добавляем каждый файл к сообщению



def attach_file(msg, filepath):                             # Функция по добавлению конкретного файла к сообщению
    writing_to_log_file('smtp.txt', 'Вызов функции attach_file')
    # '''Функция по добавлению конкретного файла к сообщению'''
    filename = os.path.basename(filepath)                   # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
    
    if ctype is None or encoding is not None:               # Если тип файла не определяется
        ctype = 'application/octet-stream'                  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)                 # Получаем тип и подтип
    
    if maintype == 'text':                                  # Если текстовый файл
        with open(filepath) as fp:                          # Открываем файл для чтения
            file = MIMEText(fp.read(), _subtype=subtype)    # Используем тип MIMEText
            fp.close()                                      # После использования файл обязательно нужно закрыть
    elif maintype == 'image':                               # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':                               # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:                                                   # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
            file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()
            encoders.encode_base64(file)                    # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
    msg.attach(file)                                        # Присоединяем файл к сообщению

# *****************************************************************
def writing_to_log_file(file, text):
    # '''функция создания лог файла и записи в него информации'''
    dt = datetime.now().strftime('%Y-%m-%d %X')
    log_file = file + '.log'
    path = 'log/' + log_file

    with open(path, 'a+') as file_log:
        log = f'{dt} : {text} \n'
        file_log.write(log)

# *****************************************************************
def connect_oracle():
    path = 'access_report.txt'
    with open(path) as f:
        access = json.load(f)
    
    driver = 'ojdbc14.jar'
    path_base = access['path_base']
    password = access['password']
    login = access['login']
    port = access['port']
    sid = access['sid']

    conn = jaydebeapi.connect(
        'oracle.jdbc.driver.OracleDriver',
        f'jdbc:oracle:thin:{login}/{password}@{path_base}:{port}/{sid}',
        [login, password],
        driver)

    curs = conn.cursor()

    return curs

# *****************************************************************
def generating_report_files(df, name_log, name_def, test, mail):
    data = pd.DataFrame(df)
    files = ''
    mo = set(data['name'])
    if len(mo) > 0:
        for row in mo:
            file = row + '.xlsx'
            data[data['name'].isin([row])].to_excel(file, index=False)
            if test == 1:
                path = 'c:/VipoNet_out1/'
            else:
                path = 'c:/VipoNet_out/'
            try:
              shutil.move(file, path)
            except:
              send_email('IVAbdulganiev@yanao.ru', f'{name_def} - ошибка переноса файла', msg_text=file)
              text = f'{name_def} - ошибка переноса файла {file} в папку {path}'
              writing_to_log_file(name_log, text)      
            files += file + '\n'

        writing_to_log_file(name_log, '\n'+files)
        send_email(mail, f'{name_def} в МО отправлены', msg_text=files)
    else:
        text = 'файлов нет'
        writing_to_log_file(name_log, text)
        send_email(mail, f'{name_def} - {text}', msg_text='')

# *****************************************************************

def generating_report_files_PFR(df, name_log, name_def, test, mail):
    data = pd.DataFrame(df)
    dt = datetime.now().strftime('%m-%Y')
    file = f'{name_def}{dt}.xlsx'
    data.to_excel(file, index=False)
    writing_to_log_file(name_log, f'создали файл {file}')

    if test == 1:
        path = 'c:/VipoNet_out1/'
        writing_to_log_file(name_log, f'path {path}')
    else:
        path = 'c:/VipoNet_out/'
        writing_to_log_file(name_log, f'path {path}')
    try:
        path_backup = 'd:/python/schedule/backup/'
        writing_to_log_file(name_log, f'path_backup {path_backup}')
        
        try:
            new_file = file + '.zip'
            writing_to_log_file(name_log, f'архирование файла {new_file}')
            zipFile = zipfile.ZipFile(new_file, 'w', zipfile.ZIP_DEFLATED)
            zipFile.write(file)
            zipFile.close()
        except:
            writing_to_log_file(name_log, 'ошибка архивирования файла {file} в {new_file}')
        
        try:
            shutil.move(new_file, path)
            writing_to_log_file(name_log, f'перенесли {new_file} в {path}')
        except:
            writing_to_log_file(name_log, f'ошибка переноса {new_file} в {path}')

        try:
            shutil.move(file, path_backup)
            writing_to_log_file(name_log, f'перенесли {file} в {path_backup}')
        except:
            writing_to_log_file(name_log, f'ошибка переноса {file} в {path_backup}')

        writing_to_log_file(name_log, new_file)

        send_email(mail, f'{name_def} в ПФР отправлен', msg_text=new_file)
        writing_to_log_file(name_log, f'{name_def} в ПФР отправлен')
    except Exception as e:
        text = f'{name_def} - ошибка'
        send_email(mail, f'{name_def} - ошибка ', msg_text=text)
        writing_to_log_file(name_log, text)      

# *****************************************************************

def generating_report_files_PFR_2(name_log, name_def, test, mail, text):
    dt = datetime.now().strftime('%m-%Y')
    new_file = name_def
    path_backup = 'd:/python/schedule/backup/'

    if test == 1:
        path = 'c:/VipoNet_out1/'
    else:
        path = 'c:/VipoNet_out/'

    writing_to_log_file(name_log, f'выбран режим {test} - {path}')

    try:
        os.remove(f'{path}{new_file}')
        writing_to_log_file(name_log, f'{path}{new_file} удален')
    except Exception as e:
        writing_to_log_file(name_log, f'сбой при удалении {path}{new_file}, ошибка {e}')

    try:
        os.remove(f'{path_backup}{new_file}')
        writing_to_log_file(name_log, f'{path_backup}{new_file} удален')
    except Exception as e:
        writing_to_log_file(name_log, f'сбой при удалении {path_backup}{new_file}, ошибка {e}')
    
    cnt = 0 # счетчик для отправки

    try:
        shutil.copy(new_file, path)
        writing_to_log_file(name_log, f'Файл {new_file} скопирован в {path}')
        cnt += 1
    except Exception as e:
        text = f'{name_def} - ошибка копирования файла {new_file} в папку {path}, ошибка - {e}'
        send_email(mail, f'{new_file} - ошибка переноса файла', msg_text=text)
        writing_to_log_file(name_log, text)

    try:
        shutil.move(new_file, path_backup)
        writing_to_log_file(name_log, f'Файл {new_file} перемещен в {path_backup}')
        cnt += 1
    except Exception as e:
        text = f'{name_def} - ошибка переноса файла {new_file} в папку {path_backup}, ошибка - {e}'
        send_email(mail, f'{new_file} - ошибка переноса файла', msg_text=text)
        writing_to_log_file(name_log, text)

    if cnt == 2:
        send_email(mail, f'{name_def} в ПФР отправлен', msg_text=text)
        writing_to_log_file(name_log, f'Письмо отправлено с текстом - {text}')
    else:
        send_email(mail, f'Alarm {name_def}', msg_text=text)
        writing_to_log_file(name_log, 'Письмо "Alarm" отправлено')