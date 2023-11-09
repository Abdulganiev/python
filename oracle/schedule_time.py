import schedule
import time, subprocess

#***************************************************************
name_log = 'schedule_time'
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def movi_file():
    try:
        subprocess.call("python d:/python/schedule/movi_file.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции movi_file() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def unlock_user_iszn():
    try:
        subprocess.call("python d:/python/schedule/unlock_user_iszn.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции unlock_user_iszn() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def seetable_trud_stac():
    try:
        subprocess.call("python d:/python/schedule/seetable_trud_stac.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции seetable_trud_stac() - {e}'
        writing_to_log_file(name_log, text)


#***************************************************************
schedule.every(10).seconds.do(movi_file)

schedule.every(15).minutes.do(unlock_user_iszn)

schedule.every(60).minutes.do(seetable_trud_stac)

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


# нужно иметь свой цикл для запуска планировщика с периодом в 1 секунду:
while True:
    schedule.run_pending()
    time.sleep(1)