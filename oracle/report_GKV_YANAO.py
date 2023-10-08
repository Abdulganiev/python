from generating_report_files import *

# *****************************************************************
log = 'report_GKV_YANAO'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

# *****************************************************************
curs = connect_oracle()

# *****************************************************************
def report_GKV_YANAO():
    with open('report_GKV_YANAO.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    
    curs.execute(sql)
    return curs.fetchall()

# *****************************************************************
def report_GKV_YANAO_data(d):
    data = {
             '№ п/п' : [],
             'Категории получателей мер социальной поддержки' : [],
             'Количество лиц, которым предоставлена социальная поддержка по оплате жилищно-коммунальных услуг (по сведениям органа государственной власти субъекта Российской Федерации), всего' : [],
             'в том числе носители льгот' : [],
             'Размер занимаемой общей площади' : [],
            }

    cnt = 0
    for el in range(1, len(d[0])+1):
        if el % 5 == 0 and el != 0:
            data['Размер занимаемой общей площади'].append(d[0][el-1])
            cnt = 0
        else:
            if cnt == 0:
                data['№ п/п'].append(d[0][el-1])
            elif cnt == 1:
                data['Категории получателей мер социальной поддержки'].append(d[0][el-1])
            elif cnt == 2:
                data['Количество лиц, которым предоставлена социальная поддержка по оплате жилищно-коммунальных услуг (по сведениям органа государственной власти субъекта Российской Федерации), всего'].append(d[0][el-1])
            elif cnt == 3:
                data['в том числе носители льгот'].append(d[0][el-1])
            cnt += 1
    return data

# *****************************************************************
def report_GKV_name():
    curs.execute("select to_char(TRUNC(ADD_MONTHS(SYSDATE,-1),'MM'), 'mm.yyyy') from dual")
    return curs.fetchone()

# *****************************************************************

data = report_GKV_YANAO_data(report_GKV_YANAO())

period = report_GKV_name()[0]

name = f'отчет ЖКВ за {period} в ЯНАО'

if test == 0:
    mail = 'IVAbdulganiev@yanao.ru, OVKolpakova@yanao.ru, NMShcherbinina@yanao.ru'

generating_report_GKV(data, log, name, mail)