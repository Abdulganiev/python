select
TRUNC(SYSDATE, 'MM'),
'Численность лиц, которым установлена РСД всего - '||
(select count(distinct t1.pka_region_id||'-'||t1.pka_people_coll_id)
        from uszn.all_asg_amounts t1
             inner join
             uszn.r_categories_assigned t2
        on t1.region_id in (select child_id from uszn.tsrv_flat_regions where parent_id=104)
              and t1.region_id=t2.pc_region_id and t1.pka_people_coll_id=t2.pc_id
              and t1.pka_is_enabled=1 and t1.pka_status_num=0
              and (t1.pka_kind_id, t1.pka_kind_region_id) in ((49,104)) and TRUNC(SYSDATE, 'MM') between t1.rap_date_start and t1.rap_date_end and t1.amount > 0
              and TRUNC(SYSDATE, 'MM') between t2.date_start and t2.date_end and (t2.pccat_id, t2.pccat_region_id) in ((354,0))
             inner join
             uszn.r_categories_assigned t3
           on t2.pc_region_id=t3.pc_region_id and t2.pc_id=t3.pc_id
              and TRUNC(SYSDATE, 'MM') between t3.date_start and t3.date_end and (t3.pccat_id, t3.pccat_region_id) in ((1180,0)) ) as rsd_all,
'Выплата РСД которым приостановлена в связи с трудоустройством - '||
(select count(distinct t1.region_id||'-'||t1.people_coll_id)
 from uszn.all_pk_assigned t1
      inner join
      uszn.r_categories_assigned t2
   on t1.region_id in (select child_id from uszn.tsrv_flat_regions where parent_id=104)
      and (t1.kind_id, t1.kind_region_id) in ((49,104)) and t1.status_num=1 and t1.ceasing_reason_id=6
      and t1.region_id=t2.pc_region_id and t1.people_coll_id=t2.pc_id
      and TRUNC(SYSDATE, 'MM') between t2.date_start and t2.date_end and (t2.pccat_id, t2.pccat_region_id) in ((354,0))
      inner join
      uszn.r_categories_assigned t3
   on t2.pc_region_id=t3.pc_region_id and t2.pc_id=t3.pc_id
      and TRUNC(SYSDATE, 'MM') between t3.date_start and t3.date_end and (t3.pccat_id, t3.pccat_region_id) in ((1180,0)) ) as rsd_zan
              
from dual