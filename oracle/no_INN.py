from generating_report_files import *

#***************************************************************
curs = connect_oracle()

#***************************************************************
def no_INN():
    curs.execute('''
select distinct
      '0'||pka_region_id||'-'||uszn.pkTSrv.GetRegionName(pka_region_id)||' - '||to_char(SysDate,'yyyy-mm-dd')||' - '||'нет ИНН' as name,
      t1.pka_region_id||'-'||nvl(t1.pka_payee_pc_id, pka_people_coll_id) as pc_id,
      nvl(t1.pka_payee_pc_desc, t1.pka_people_coll_desc) as pc_desc
  from uszn.all_asg_periods t1
       inner join
       (select region_id, id
          from uszn.all_payment_kinds
          where (owner_region_id, owner_id) in ((0, 214), (0, 71), (0, 215), (0, 4), (0, 6), (0, 185), (0, 1), (104, 85), (104, 82), (104, 284), (104, 86))
                and is_assignable=1 and upper(name) not like ('%ОТМЕНЕН%') and region_id in (0, 104)) t2
     on
     t1.region_id in (select id from uszn.tsrv_regions where owner_id=104 and id not in (71, 72) )
     and t1.pka_kind_region_id=t2.region_id and t1.pka_kind_id=t2.id
     and trunc(sysdate,'mm') between t1.date_start and t1.date_end and t1.pka_is_enabled=1 and t1.pka_status_num=0 and t1.pka_is_external=0
     left join
     uszn.all_personal_docs t3
     on
     t3.region_id=t1.pka_region_id and t3.pc_id=t1.pka_payee_pc_id and t3.class_id=4275
where t3.pdc_name is null    
    ''')
    
    data = {
         'name' : [],
         'ID человека' : [],
         'Описание' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['ID человека'].append(row[1])
        data['Описание'].append(row[2])
    
    return data

#***************************************************************

data = no_INN()
name_log = 'no_INN'
name_def = 'Нет ИНН'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

generating_report_files(data, name_log, name_def, test, mail)
