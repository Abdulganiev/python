from keyboard import press_and_release
from time import sleep
import pyperclip
import pyautogui as pag

def paste(text: str):    
    pyperclip.copy(text)
    press_and_release('ctrl + v')


def type(text: str, interval=0.0):    
    buffer = pyperclip.paste()
    if not interval:
        paste(text)
    else:
        for char in text:
            paste(char)
            sleep(interval)
    pyperclip.copy(buffer)
    
    
def okno():
	# '''функция переключения на другое окно'''
    pag.keyDown("altleft")
    pag.press("tab")
    pag.keyUp("altleft")
    pag.press("enter")

def hom(text, o=1):
	# """
	# Функция
	# параметр o по умолчанию равен 1, т.е. обязательно
	# """
    pag.press("home")
    pag.moveTo(1200, 340, 4)
    pag.click()
    pag.moveTo(590, 385, 4)
    pag.click()

    past(text)
    pag.press("esc")

    if o == 1: # обязательный или нет
        pag.moveTo(565, 512, 1.5)
        pag.click()
    else:
        pag.moveTo(1200, 490, 1.5)
        pag.click()
    
    pag.press("end")
    
    pag.moveTo(580, 490, 1.5)
    pag.click()
    
def display_results():	# '''снятие или включение чек-бокса "Отображать в списке результатов в личном кабинете"'''
	pag.moveTo(566, 812, 1)
	pag.click()

def gu_str(text, o):
    hom(text, o)
    type('11', 1.5)
    pag.press("enter")
    display_results()
    pag.press('enter')
    
def gu_dat(text, o):
    hom(text, o)
    type('3', 1.5)
    pag.press("enter")
    pag.press('enter')
    
def gu_num(text, o):
    hom(text, o)
    type('14', 1.5)
    pag.press("enter")
    pag.press('enter')    
    
def gu_mail(text, o):
    hom(text, o)
    type('1', 1.5)
    pag.press("enter")
    pag.press('enter')
    
def gu_com(text, o):
    hom(text,  0)
    type('12', 1.5)
    pag.press("enter")
    pag.press('enter')
    
def gu_mesto(text, o):
    hom(text,  o)
    text2 = 'указываются на основании записи в документе, удостоверяющем личность, или ином документе, подтверждающем постоянное проживание заявителя на территории Ямало-Ненецкого автономного округа'
    pag.moveTo(565, 450, 1.5)
    pag.click()
    past(text2)

    pag.moveTo(580, 490, 1.5)
    pag.click()
    type('11', 1.5)
    pag.press("enter")
    pag.moveTo(565, 815, 1.5)
    pag.click()
    pag.press('enter')
    
def variant1(text, t1='Да'):
    hom(text,  1)
    type('6', 2)
    pag.press("enter")
    pag.moveTo(565, 560, 1.5)
    pag.click()
    pag.moveTo(565, 595, 1.5)
    pag.click()
    past(t1)
    pag.press("enter")
    
def variant2(text, t1, t2):
    hom(text,  1)
    type('6', 1)
    pag.press("enter")
    pag.moveTo(565, 560, 1.5)
    pag.click()
    pag.moveTo(565, 595, 1.5)
    pag.click()
    past(t1)
    pag.press("esc")
    
    pag.moveTo(565, 705, 1.5)
    pag.click()        
    pag.moveTo(565, 745, 1.5)
    pag.click()
    past(t2)
    pag.press("enter")
    
def variant3(text, t1, t2, t3):
    hom(text,  1)
    type('6', 1)
    pag.press("enter")
    pag.moveTo(565, 560, 1.5)
    pag.click()
    pag.moveTo(565, 595, 1.5)
    pag.click()
    past(t1)
    pag.press("esc")
    
    pag.moveTo(565, 705, 1.5)
    pag.click()        
    pag.moveTo(565, 745, 1.5)
    pag.click()
    past(t2)
    pag.press("esc")
    
    pag.moveTo(565, 845, 1.5)
    pag.click()
    pag.press("end")
    pag.moveTo(575, 280, 1.5)
    pag.click()
    past(t3)
    pag.press("enter")

def past(text):
    pyperclip.copy(text)
    pag.hotkey('ctrl', 'v')

def in_file(text, o):
    hom(text,  o)
    type('4', 1)
    pag.press("enter")
    pag.press("enter")
    
def end():
    pag.moveTo(431, 285, 1.5)

def zayav(x=0):
    pag.moveTo(1244, 345-x, 3.5)
    pag.click()
    pag.moveTo(560, 390-x, 3.5)
    pag.click()
    text = 'Данные заявления'
    past(text)
    pag.press("enter")
    pag.moveTo(1245, 405-x, 3.5)
    pag.click()

def forma(text1, text2):
    pag.moveTo(1235, 330, 1.5)
    pag.click()
    pag.moveTo(559, 372, 3.5)
    pag.click()
    past(text1)
    pag.moveTo(572, 443, 1)
    pag.click()
    pag.moveTo(578, 504, 1)
    pag.click()
    pag.moveTo(565, 476, 1)
    pag.click()
    pag.moveTo(567, 511, 1)
    pag.click()
    pag.press("end")
    pag.moveTo(613, 345, 1)
    pag.click()
    pag.click()
    pag.press("esc")
    past('ivabdulganiev@yanao.ru')
    pag.moveTo(617, 395, 1)
    pag.click()
    pag.click()
    pag.press("esc")
    past('ISZaguzin@yanao.ru')
    pag.moveTo(617, 443, 1)
    pag.click()
    pag.click()
    pag.press("esc")
    past(text2)
    pag.press("enter")

def forma2():
    sleep(2)
    pag.press("home")
    pag.moveTo(1237, 572, 1)
    pag.click()    

def gragd():
    text = 'Сведения о принадлежности к гражданству:'
    t1 = 'Гражданин Российской Федерации'
    t2 = 'Иностранный гражданин'
    t3 = 'Лицо без гражданства'
    variant3(text, t1, t2, t3)

def dul(text):
    gu_com(text, 0)
    gu_str('Наименование документа, удостоверяющего личность', 1)
    gu_str('Серия и номер', 1)
    gu_str('Кем выдан', 1)
    gu_dat('Когда выдан', 1)
    gu_str('Код подразделения', 1)
    gu_str('Место рождения', 1)
    pag.click()