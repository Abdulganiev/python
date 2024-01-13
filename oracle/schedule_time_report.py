import schedule, time, subprocess
from generating_report_files import *

#***************************************************************
name_log = 'schedule_time_report'
mail = 'IVAbdulganiev@yanao.ru'

writing_to_log_file(name_log, f'**************************************************************')
writing_to_log_file(name_log, f'Запуск schedule_time_report')

#***************************************************************
def report_milk_malo(): # временная таблица малоимущие для ЭС молочка
    try:
        writing_to_log_file(name_log, f'Запуск процесса report_milk_malo')
        subprocess.call("python d:/python/schedule/report_milk_malo.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции report_milk_malo - {e}'
        writing_to_log_file(name_log, text)

try:
    writing_to_log_file(name_log, f'Запуск процесса report_milk_malo')
    schedule.every().day.at("06:15").do(report_milk_malo)
    schedule.every().day.at("13:05").do(report_milk_malo)
except Exception as e:
    text = f'Произошла ошибка при вызове функции report_milk_malo - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************
def report_milk_age_3(): # временная таблица дети до 3 лет для ЭС молочка
    try:
        writing_to_log_file(name_log, f'Запуск процесса report_milk_age_3')
        subprocess.call("python d:/python/schedule/report_milk_age_3.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции report_milk_age_3 - {e}'
        writing_to_log_file(name_log, text)

try:
    writing_to_log_file(name_log, f'Запуск процесса report_milk_age_3')
    schedule.every().day.at("07:15").do(report_milk_age_3)
    schedule.every().day.at("13:15").do(report_milk_age_3)
except Exception as e:
    text = f'Произошла ошибка при вызове функции report_milk_age_3 - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************
def report_bi_svo(): # временная таблица по выплатам УСВО для РСУД
    try:
        writing_to_log_file(name_log, f'Запуск процесса report_bi_svo')
        subprocess.call("python d:/python/schedule/report_bi_svo.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции report_bi_svo - {e}'
        writing_to_log_file(name_log, text)

try:
    writing_to_log_file(name_log, f'Запуск процесса report_bi_svo')
    schedule.every().day.at("09:15").do(report_bi_svo)
    schedule.every().day.at("13:15").do(report_bi_svo)
    schedule.every().day.at("17:15").do(report_bi_svo)
except Exception as e:
    text = f'Произошла ошибка при вызове функции report_bi_svo - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************
def svo(): # временная таблица СВО
    try:
        writing_to_log_file(name_log, f'Запуск процесса svo')
        subprocess.call("python d:/python/schedule/svo.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции svo() - {e}'
        writing_to_log_file(name_log, text)

try:
    writing_to_log_file(name_log, f'Запуск процесса svo')
    schedule.every().day.at("07:30").do(svo)
    schedule.every().day.at("13:30").do(svo)
except Exception as e:
    text = f'Произошла ошибка при вызове функции svo - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************
def report_ES(): # временная таблица реестр по ЭС
    try:
        writing_to_log_file(name_log, f'Запуск процесса report_ES')
        subprocess.call("python d:/python/schedule/report_ES.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции report_ES() - {e}'
        writing_to_log_file(name_log, text)

try:
    writing_to_log_file(name_log, f'Запуск процесса report_ES')
    schedule.every().day.at("07:00").do(report_ES)
    schedule.every().day.at("11:00").do(report_ES)
    schedule.every().day.at("13:30").do(report_ES)
    schedule.every().day.at("17:00").do(report_ES)
except Exception as e:
    text = f'Произошла ошибка при вызове функции report_ES - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************
def report_large_family(): # реестр многодетных
    try:
        writing_to_log_file(name_log, f'Запуск процесса report_large_family')        
        subprocess.call("python d:/python/schedule/report_large_family.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции report_large_family() - {e}'
        writing_to_log_file(name_log, text)

try:
    writing_to_log_file(name_log, f'Запуск процесса report_large_family')
    schedule.every().day.at("07:00").do(report_large_family)
    schedule.every().day.at("12:30").do(report_large_family)
except Exception as e:
    text = f'Произошла ошибка при вызове функции report_large_family - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************
#***************************************************************
#***************************************************************
# нужно иметь свой цикл для запуска планировщика с периодом в 1 секунду:
while True:
    schedule.run_pending()
    time.sleep(1)

#***************************************************************
# schedule.every(10).minutes.do(job) 
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

# schedule.every(10).minutes.do(job) # спланируй.каждые(10).минут.сделать(работу)

# schedule.every().day.at("10:30").do(job) # спланируй.каждый().день.в(10:30).сделать(работу)

#########################################################
# В задания можно передавать параметры вот так:
# def greet(name):
#     print('Hello', name)

# schedule.every(2).seconds.do(greet, name='Alice')

#########################################################
# Если по какой-то причине нужно отменить задание, это делается так:

# def job1():
#     # возвращаем такой токен, и это задание снимается с выполнения в будущем
#     return schedule.CancelJob
# schedule.every().day.at('22:30').do(job1)

#########################################################
# Если нужно отменить группу заданий, то к ним добавляют тэги:

# schedule.every().day.do(greet, 'Monica').tag('daily-tasks')
# schedule.every().day.do(greet, 'Derek').tag('daily-tasks')
# schedule.clear('daily-tasks')  # массовая отмена по тэгу



# Run job every 3 second/minute/hour/day/week,
# Starting 3 second/minute/hour/day/week from now
# schedule.every(3).seconds.do(job)
# schedule.every(3).minutes.do(job)
# schedule.every(3).hours.do(job)
# schedule.every(3).days.do(job)
# schedule.every(3).weeks.do(job)

# Run job every minute at the 23rd second
# Запускайте задание каждую минуту на 23-й секунде
# schedule.every().minute.at(":23").do(job)

# Run job every hour at the 42nd minute
# Запускайте задание каждый час на 42-й минуте
# schedule.every().hour.at(":42").do(job)

# Run jobs every 5th hour, 20 minutes and 30 seconds in. Выполняйте задания каждые 5 часов, 20 минут и 30 секунд.
# If current time is 02:00, first execution is at 06:20:30 - Если текущее время равно 02:00, то первое выполнение произойдет в 06:20:30
# schedule.every(5).hours.at("20:30").do(job)

# Run job every day at specific HH:MM and next HH:MM:SS
# Выполняйте задание каждый день в определенное время ЧЧ:ММ и в следующее ЧЧ:ММ:СС
# schedule.every().day.at("10:30").do(job)
# schedule.every().day.at("10:30:42").do(job)
# schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)

# Run job on a specific day of the week
# Выполнить задание в определенный день недели
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)    

# run job until a 18:30 today
# выполняйте задание до 18:30 сегодняшнего дня
# schedule.every(1).hours.until("18:30").do(job)

# run job until a 2030-01-01 18:33 today
# выполняйте задание до 2030-01-01 18:33 сегодня
# schedule.every(1).hours.until("2030-01-01 18:33").do(job)

# Schedule a job to run for the next 8 hours
# Запланируйте выполнение задания на следующие 8 часов
# schedule.every(1).hours.until(timedelta(hours=8)).do(job)

# Run my_job until today 11:33:42
# Запускайте my_job до сегодняшнего дня 11:33:42
# schedule.every(1).hours.until(time(11, 33, 42)).do(job)

# run job until a specific datetime
# запускать задание до определенной даты времени
# schedule.every(1).hours.until(datetime(2020, 5, 17, 11, 36, 20)).do(job)

