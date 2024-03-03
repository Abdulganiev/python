create table uszn.temp$_malo55_2024_01_01 as

select distinct 1 as kind_id, v1.region_id, v1.people_id as id
from uszn.v_coll_membership_periods v1 inner join
  (select region_id, people_id as coll_id
    from
     (select t1.region_id, uszn.pkPerson.GetDocInstancePC(t1.pdoc_id, t1.region_id) as people_id
      from uszn.r_personal_doc_reqs t1 inner join uszn.r_personal_doc_reqs t2
      on t1.region_id=t2.region_id and t1.pdoc_id=t2.pdoc_id and t1.order_num=t2.order_num
         and t1.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
         and t1.class_id=10556 and t2.class_id=10557 and t2.value in (1, 2)
         and ADD_MONTHS(uszn.ToDateDef(t1.value), 11) >= TRUNC(TRUNC(SYSDATE, 'mm')-1, 'mm')
         and ADD_MONTHS(uszn.ToDateDef(t1.value), 1)  <= TRUNC(SYSDATE, 'mm')-1
       union all
     select t1.region_id, uszn.pkPerson.GetDocInstancePC(t1.pdoc_id, t1.region_id) as people_id
      from uszn.r_personal_doc_reqs t1 inner join uszn.r_personal_doc_reqs t2
      on t1.region_id=t2.region_id and t1.pdoc_id=t2.pdoc_id and t1.order_num=t2.order_num
         and t1.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
         and t1.class_id=17998 and t2.class_id=17999 and uszn.ToIntDef(t2.value)=1
         and ADD_MONTHS(uszn.ToDateDef(t1.value), 11) >= TRUNC(TRUNC(SYSDATE, 'mm')-1, 'mm')
         and ADD_MONTHS(uszn.ToDateDef(t1.value), 1)  <= TRUNC(SYSDATE, 'mm')-1
       union all
     select t1.region_id, uszn.pkPerson.GetDocInstancePC(t1.pdoc_id, t1.region_id) as people_id
      from uszn.r_personal_doc_reqs t1 inner join uszn.r_personal_doc_reqs t2
      on t1.region_id=t2.region_id and t1.pdoc_id=t2.pdoc_id and t1.order_num=t2.order_num
         and t1.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
         and t2.class_id=18060 and t1.class_id=18059 and uszn.ToIntDef(t2.value)=1
         and ADD_MONTHS(uszn.ToDateDef(t1.value), 11) >= TRUNC(TRUNC(SYSDATE, 'mm')-1, 'mm')
         and ADD_MONTHS(uszn.ToDateDef(t1.value), 1)  <= TRUNC(SYSDATE, 'mm')-1
         )
     group by region_id, people_id) v2
     on v1.region_id=v2.region_id and v1.coll_id=v2.coll_id
where TRUNC(SYSDATE, 'mm') between v1.date_start and v1.date_end
      and uszn.pkPerson.GetDeathDate(v1.region_id, v1.people_id) is null
      and uszn.pkPerson.GetCloseDate(v1.region_id, v1.people_id) is null