select
'П'||
-- страховой номер
RPad(Nvl(c.snils_formatted, '   -   -      '), 14, ' ')||
-- фамилия
RPad(Nvl(Upper(c.last_name), ' '), 40, ' ')||
-- имя
RPad(Nvl(Upper(c.first_name), ' '), 40, ' ')||
-- отчество
RPad(Nvl(Upper(c.middle_name), ' '), 40, ' ')||
-- дата рождения
RPad(Nvl(To_Char(c.birth_date, 'yyyy/mm/dd'), ' '), 10, ' ')
from
(select
  pc.region_id, pc.id as people_id,
  pc.last_name, pc.first_name, pc.middle_name, pc.birth_date, pc.sex_full, pc.snils_formatted
from
 ((select distinct t1.pc_region_id as region_id, t1.pc_id as id
    from uszn.r_categories_assigned t1
    where t1.pc_region_id in (select id from uszn.tsrv_regions where owner_id=104 and id not in (71, 72))
          and sysdate between t1.date_start and t1.date_end
          and (t1.pccat_id, t1.pccat_region_id) in ((800,0),(1131,0))
    union
   select distinct d1.region_id, d1.pd_pc_id
    from uszn.all_personal_doc_reqs d1
    where d1.region_id in (select id from uszn.tsrv_regions where owner_id=104 and id not in (71, 72))
          and d1.pd_class_id=8604 and d1.class_id=10482
          and uszn.ToIntDef(d1.value)!='0'
          and Floor(Months_Between(sysdate, uszn.pkPerson.GetBirthDate(d1.region_id,d1.pd_pc_id))/12) < 18
          and d1.pd_date_created > TRUNC(ADD_MONTHS(SYSDATE, -1), 'MM'))
  minus
  select distinct d2.region_id, d2.people_coll_id
   from uszn.r_payment_kinds_assigned d2
   where d2.region_id in (select id from uszn.tsrv_regions where owner_id=104 and id not in (71, 72))
         and (kind_id, kind_region_id) in ((47,104))
         and sysdate between while_start_date and while_end_date
         and is_enabled=1 and status_num=0) c,
  uszn.v_people_and_colls pc
where pc.region_id=c.region_id and pc.id=c.id) c