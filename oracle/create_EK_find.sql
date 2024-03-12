select region_id, id as people_id, ek
  from (
select t1.region_id, t1.id, t1.snils
   from (select region_id, id, snils from uszn.r_people_and_colls t1 where is_coll_instance=0 and death_date is null and snils is not null and close_date is null) t1
        left join
        (select region_id, pc_id from uszn.v_personal_docs where class_id=18899) t2
    on  t1.region_id=t2.region_id and t1.id=t2.pc_id
       where t2.pc_id is null
  ) t1
       join
       (
 select uszn.pkPerson.GetPersonalReq(rq.region_id, pd.pc_id, 26) as snils, rq.value as ek
  from uszn.v_personal_docs pd join uszn.v_personal_doc_reqs rq
   on rq.region_id=pd.region_id and rq.pdoc_id=pd.id and pd.class_id=18899 and rq.class_id=18900
      and uszn.pkPerson.GetPersonalReq(rq.region_id, pd.pc_id, 25) is not null
       ) t2
   on t1.snils=t2.snils and t1.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)