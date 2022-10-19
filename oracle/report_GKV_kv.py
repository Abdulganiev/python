from generating_report_files import *

# *****************************************************************
curs = connect_oracle()

# *****************************************************************
def report_GKV_kv(region_id):
    with open('report_GKV_kv.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{region_id}', f'{region_id}')
    curs.execute(sql)
    return curs.fetchall()

# *****************************************************************
def report_GKV_kv_data(d):
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
    curs.execute("SELECT to_char(TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q'),'Q')||' кв '||to_char(TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q'),'YYYY') FROM dual")
    return curs.fetchone()

# *****************************************************************
def report_GKV_mo(region_id):
    sql = f'SELECT uszn.pkTSrv.GetRegionName({region_id}) FROM dual'
    curs.execute(sql)
    return curs.fetchone()

# *****************************************************************
def report_GKV_mail(region_id, mail, ):
    sql = f'SELECT uszn.pkTSrv.GetRegionName({region_id}) FROM dual'
    curs.execute(sql)
    return curs.fetchone()

# *****************************************************************
log = 'report_GKV_kv'
test = 0
period = report_GKV_name()[0]
name = f'отчет ЖКВ за {period}'

if test == 1:
    mail = 'IVAbdulganiev@yanao.ru'
else:
    mail = 'IVAbdulganiev@yanao.ru'

# *****************************************************************
writing_to_log_file(log, '********************************************')

for region_id in range(58, 71):
    mo = report_GKV_mo(region_id)[0]
    name_mo = f'{name} в {mo}'
    mail_mo = generating_mail_mo(region_id, mail, test)

    data = report_GKV_kv_data(report_GKV_kv(region_id))
    generating_report_GKV_kv(data, log, name, str(region_id), mail)
    generating_report_GKV(data, log, name_mo, mail_mo)