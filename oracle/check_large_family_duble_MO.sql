SELECT distinct t1.pc_region_id
 from uszn.r_categories_assigned t1
      inner join
     (select uszn.pkPerson.GetPersonalReq(pk.pc_region_id, pk.pc_id, 26) as SNILS
        from uszn.r_categories_assigned pk
        where pk.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
             and (pk.pccat_region_id, pk.pccat_id) in ((0, 1058))
             and sysdate between pk.date_start and pk.date_end
             and uszn.pkPerson.GetPersonalReq(pk.pc_region_id, pk.pc_id, 26) is not null
        group by uszn.pkPerson.GetPersonalReq(pk.pc_region_id, pk.pc_id, 26)
        having Count(*)>1) t2
 on uszn.pkPerson.GetPersonalReq(t1.pc_region_id, t1.pc_id, 26)=t2.SNILS
    and t1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
    and (t1.pccat_region_id, t1.pccat_id) in ((0, 1058))
    and sysdate between t1.date_start and t1.date_end