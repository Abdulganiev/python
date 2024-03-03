insert into uszn.temp$_r_EPB

select aa.region_id,
       aa.pka_people_coll_id as people_id,
       uszn.pkPerson.GetPersonalReq(aa.region_id, aa.pka_people_coll_id, 25) as snils,
       pd.value as pers_id
   from uszn.all_asg_amounts aa
        left join
        (select pd.region_id, pd.pc_id, rq.value from uszn.v_personal_docs pd join uszn.v_personal_doc_reqs rq
           on rq.region_id=pd.region_id and rq.pdoc_id=pd.id and pd.class_id=18899 and rq.class_id=18900) pd
   on aa.region_id=pd.region_id and aa.pka_people_coll_id=pd.pc_id
   where aa.pka_kind_region_id=104 and aa.pka_kind_id=310
         and aa.rai_item_region_id=104 and aa.rai_item_id=696
         and Trunc(SysDate, 'dd') between aa.rap_date_start and aa.rap_date_end
         and aa.region_id={region}