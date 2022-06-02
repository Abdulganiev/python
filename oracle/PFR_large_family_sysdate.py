import datetime as dt
from generating_report_files import *

#***************************************************************
def PFR_large_family_sysdate():
    curs.execute('''
select 
    ROW_NUMBER() OVER(ORDER BY date_start) as num,
    m_desc as mother,
    m_snils as mother_snils,
    f_desc as father,
    f_snils as father_snils,
    children,
    'Да' as yes,
    date_start
from
(select t1.region_id, t1.coll_id,
       t3.people_id as m_id, t3.people_desc as m_desc, uszn.pkPerson.GetPersonalReq(t3.region_id, t3.people_id, 25) as m_snils,
       t4.people_id as f_id, t4.people_desc as f_desc, uszn.pkPerson.GetPersonalReq(t4.region_id, t4.people_id, 25) as f_snils,
       uszn.StrCommaConcat(distinct t5.people_desc||', '||uszn.pkPerson.GetPersonalReq(t5.region_id, t5.people_id, 25)||CHR(10)) as children
      , min(t2.date_start) as date_start
 from uszn.v_coll_membership_periods t1
      inner join
      uszn.r_categories_assigned t2
   on  t1.region_id not in (71, 72, 104)
       and t1.coll_class_id=6 and
       t1.region_id=t2.pc_region_id and t1.coll_id=t2.pc_id
       and sysdate between t2.date_start and t2.date_end and
       (t2.pccat_region_id, t2.pccat_id) in ((0, 661), (0, 515))
      left join
      uszn.v_coll_membership_periods t3
   on t1.region_id=t3.region_id and t1.coll_id=t3.coll_id and
      t3.role_class_id = 8 and sysdate between t3.date_start and t3.date_end
      left join
      uszn.v_coll_membership_periods t4
   on t1.region_id=t4.region_id and t1.coll_id=t4.coll_id and
      t4.role_class_id = 9 and sysdate between t4.date_start and t4.date_end
      inner join
      uszn.v_coll_membership_periods t5
   on t1.region_id=t5.region_id and t1.coll_id=t5.coll_id and
      t5.role_class_id = 10 and sysdate between t5.date_start and t5.date_end
      inner join
      uszn.r_categories_assigned t6
   on t5.region_id=t6.pc_region_id and t5.people_id=t6.pc_id
      and sysdate between t6.date_start and t2.date_end and
      (t6.pccat_region_id, t6.pccat_id) in ((0, 485), (0, 1059))
group by t1.region_id, t1.coll_id,
       t3.people_id, t3.people_desc, uszn.pkPerson.GetPersonalReq(t3.region_id, t3.people_id, 25),
       t4.people_id, t4.people_desc, uszn.pkPerson.GetPersonalReq(t4.region_id, t4.people_id, 25))''')
    
    data = {
         '№ п.п' : [],
         'ФИО и дата рождения матери' : [] ,
         'СНИЛС матери' : [] ,
         'ФИО и дата рождения отца' : [] ,
         'СНИЛС отца' : [] ,
         'Данные о детях' : [] ,
         'Статус "Многодетная"' : [] ,
         'Дата присвоения статуса "Многодетная"' : [] ,
        }
    
    for row in curs.fetchall():
        data['№ п.п'].append(row[0])
        data['ФИО и дата рождения матери'].append(row[1])
        data['СНИЛС матери'].append(row[2])
        data['ФИО и дата рождения отца'].append(row[3])
        data['СНИЛС отца'].append(row[4])
        data['Данные о детях'].append(row[5])
        data['Статус "Многодетная"'].append(row[6])
        data['Дата присвоения статуса "Многодетная"'].append(row[7])

    return data

#***************************************************************
name_log = 'PFR_large_family_sysdate'
dt = datetime.now().strftime('%d')
name_def = f'DSZN_030_{dt}-' 
test = 0
mail = 'IVAbdulganiev@yanao.ru'
cnt_curs = 0
cnt_data = 0

#***************************************************************
writing_to_log_file(name_log, '***********************************')

try:
    curs = connect_oracle()
except Exception as e:
    writing_to_log_file(name_log, f'ошибка подключения к базе \n {e}')
else:
    writing_to_log_file(name_log, 'К базе подключился')
    cnt_curs = 1

if cnt_curs == 1:
    try:
        data = PFR_large_family_sysdate()
    except Exception as e:
        writing_to_log_file(name_log, f'ошибка функции PFR_large_family_sysdate \n {e}')
else:
    cnt_curs = 1

if cnt_curs == 1:
    try:
        generating_report_files_PFR(data, name_log, name_def, test, mail)
    except Exception as e:
        writing_to_log_file(name_log, f'ошибка функции generating_report_files_PFR \n {e}')