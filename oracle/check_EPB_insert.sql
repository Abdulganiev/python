insert into uszn.temp$_r_EPB

select aa.region_id,
       aa.pka_people_coll_id as people_id,
       uszn.pkPerson.GetPersonalReq(aa.region_id, aa.pka_people_coll_id, 25) as snils,
       uszn.pkPerson.GetPCReqValue(aa.region_id, aa.pka_people_coll_id, 18900) as pers_id
   from uszn.all_asg_amounts aa
   where aa.pka_kind_region_id=104 and aa.pka_kind_id=310
         and aa.rai_item_region_id=104 and aa.rai_item_id=696
         and Trunc(SysDate, 'dd') between aa.rap_date_start and aa.rap_date_end
         and aa.region_id={region}