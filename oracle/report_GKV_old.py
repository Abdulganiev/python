import pandas as pd
import jaydebeapi
import json
import datetime as dt
import os
from smtp import *

path = "access_report.txt"
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

def GKH():
    curs.execute('''
select region_id,
       uszn.pkTSrv.GetRegionName(region_id),
       sum(fam_memb),
       sum(cnt),
       sum(area)
from
(select region_id,
       --n_row,
       Ceil(Sum(pc_count)) as fam_memb,
       Count(*) as cnt,
       Max(area) as area
   from (
     select data.region_id,
            data.coll_id,
            data.pc_count,
            case when levels.lvl=3 then 41 end as n_row,
            uszn.ToNumberDef(uszn.pkPerson.GetRawPCReqValueOnDate(data.region_id, data.coll_id, 3760, 3845, null, data.payout_date), 0) as area
        from (
          select id as lvl
            from uszn.u_dummy
            where id<=3) levels,
         (with mapped_pkafs as
             (select int_region_id as pkaf_region_id,
                     int_id as pkaf_id,
                     uszn.ToIntDef(ext_code) as cat_code
                 from uszn.dic_data_exchange_mappings
                 where kind_id=70 and
                       ext_region_id not in (71, 72) and
                       uszn.ToIntDef(ext_code) not in (40, 50) and
                       ((uszn.ToIntDef(ext_code) between 10 and 150) or (uszn.ToIntDef(ext_code) between 340 and 351) ))
select a.region_id,
    a.pka_people_coll_id as people_id,
    a.poi_payout_date as payout_date,
    a.pc_count_applied_to as pc_count,
    uszn.pkOutDocCol.GetPFRF_Cat( a.region_id, a.pka_people_coll_id, a.pkaf_region_id, a.pkaf_id, Trunc(a.poi_payout_date, 'mm'),
    Last_Day(a.poi_payout_date)) as n_cat, uszn.pkPic.GetCollByRole(a.region_id, a.pka_people_coll_id, 46, a.poi_payout_date, 0, 0) as coll_id
 from uszn.all_po_amounts a
 where (a.region_id, a.id) in (
    select a.region_id,
           First_Value(a.id) over (partition by a.region_id, a.poi_assigned_id order by a.poi_payout_date desc, a.pc_count_applied_to desc, a.income_date desc, a.id) as amount_id
        from uszn.all_po_amounts a
        where a.region_id not in (71, 72) and
              (a.pka_kind_region_id, a.pka_kind_id) in ((104,29)) and
              a.finsrc_region_id=0 and a.finsrc_id=1 and a.status_kind_id=2 and
              a.poi_payout_date between TRUNC(ADD_MONTHS(SYSDATE,-1),'MM') and TRUNC(SYSDATE,'MM')-1 and
              (((a.pkaf_region_id, a.pkaf_id) in ((104, 339)) and
              Exists( select 1
                        from uszn.r_personal_doc_instances d,
                             mapped_pkafs m
                           where d.region_id=a.region_id and d.people_coll_id=a.pka_people_coll_id and
                                 d.class_id=7116 and m.pkaf_region_id*1000000+m.pkaf_id=uszn.ToIntDef(d.value) ))
                                 or
                                 (a.pkaf_region_id, a.pkaf_id) in (select pkaf_region_id, pkaf_id from mapped_pkafs) )))data)
                                 where n_row is not null
                                 group by n_row,
                                       region_id, coll_id)
group by region_id''')

    data = {
         'id МО' : [] ,
         'Название МО' : [] ,
         'Всего' : [] ,
         'в том числе льготники' : [] ,
         'площадь' : []             
        }
    for row in curs.fetchall():
        data['id МО'].append(row[0])
        data['Название МО'].append(row[1])
        data['Всего'].append(row[2])
        data['в том числе льготники'].append(row[3])
        data['площадь'].append(row[4])
        
    df = pd.DataFrame(data)
    
    today = dt.date.today()
    first = today.replace(day=1)
    lastMonth = first - dt.timedelta(days=1)
    date_report = lastMonth.strftime('%m.%Y')
    
    file_name = f'отчет ЖКВ за {date_report} в разрезе МО'+ '.xlsx'
    df.to_excel(file_name, index=False)

    return file_name

today = dt.date.today()
file_name = GKH()

send_email('IVAbdulganiev@yanao.ru, MSNesteruk@yanao.ru', f'{file_name} на {today}', msg_text='', files=[file_name])

new_file_name = f'{today} - {file_name}'

os.replace(file_name, f'backup/{new_file_name}') 