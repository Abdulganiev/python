import schedule, time, subprocess
# from schedule_time_job import *
from generating_report_files import *

#***************************************************************
name_log = 'schedule_time_one'
mail = 'IVAbdulganiev@yanao.ru'

writing_to_log_file(name_log, f'**************************************************************')
writing_to_log_file(name_log, f'Запуск schedule_time_one')

#***************************************************************
def movi_file_share():
    try:
        subprocess.call("python d:/python/schedule/movi_file_share.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции movi_file_share() - {e}'
        writing_to_log_file(name_log, text)

try:
    writing_to_log_file(name_log, f'Запуск процесса movi_file_share')
    schedule.every(10).seconds.do(movi_file_share)
except Exception as e:
    text = f'Произошла ошибка при вызове функции movi_file_share - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************
def unlock_user_iszn(): # разблокировка пользователей в исзн
    try:
        subprocess.call("python d:/python/schedule/unlock_user_iszn.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции unlock_user_iszn() - {e}'
        writing_to_log_file(name_log, text)

try:
    writing_to_log_file(name_log, f'Запуск процесса unlock_user_iszn')
    schedule.every(15).minutes.do(unlock_user_iszn)
except Exception as e:
    text = f'Произошла ошибка при вызове функции unlock_user_iszn - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************
def signature_error():
    try:
        writing_to_log_file(name_log, f'Запуск процесса signature_error')
        subprocess.call("python d:/python/schedule/signature_error.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции signature_error() - {e}'
        writing_to_log_file(name_log, text)

try:
    writing_to_log_file(name_log, f'Запуск процесса signature_error')
    schedule.every(6).hours.do(signature_error)
except Exception as e:
    text = f'Произошла ошибка при вызове функции signature_error - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************
def lk_reconnecting():
    try:
        writing_to_log_file(name_log, f'Запуск процесса lk_reconnecting')
        subprocess.call("python d:/python/schedule/lk_reconnecting.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции lk_reconnecting() - {e}'
        writing_to_log_file(name_log, text)

try:
    writing_to_log_file(name_log, f'Запуск процесса lk_reconnecting')
    schedule.every().day.at("07:10").do(lk_reconnecting)
    schedule.every().day.at("13:10").do(lk_reconnecting)
except Exception as e:
    text = f'Произошла ошибка при вызове функции lk_reconnecting - {e}'
    writing_to_log_file(name_log, text)

#***************************************************************
def not_correct_GU():
    try:
        writing_to_log_file(name_log, f'Запуск процесса not_correct_GU')
        subprocess.call("python d:/python/schedule/not_correct_GU_MSP.py", shell=True)
        subprocess.call("python d:/python/schedule/not_correct_GU_PGS.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции not_correct_GU() - {e}'
        writing_to_log_file(name_log, text)

try:
    writing_to_log_file(name_log, f'Запуск процесса not_correct_GU')
    schedule.every(4).hours.do(not_correct_GU)
except Exception as e:
    text = f'Произошла ошибка при вызове функции not_correct_GU - {e}'
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

