import json
import os
from writing_to_log_file import *
import smtplib # Импортируем библиотеку по работе с SMTP

# Добавляем необходимые подклассы - MIME-типы
import mimetypes # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders # Импортируем энкодер
from email.mime.base import MIMEBase # Общий тип
from email.mime.text import MIMEText # Текст/HTML
from email.mime.image import MIMEImage # Изображения
from email.mime.audio import MIMEAudio # Аудио
from email.mime.multipart import MIMEMultipart # Многокомпонентный объект


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