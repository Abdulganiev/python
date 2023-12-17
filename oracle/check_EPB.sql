select
    distinct t1.region_id,
             uszn.pkTSrv.GetRegionName(t1.region_id) as mo,
             t1.region_id||'-'||t1.id as pc_id,
             t1.pka_people_coll_desc,
             uszn.pkPerson.GetPersonalReq(t1.region_id, t1.pka_people_coll_id, 25) as SNILS
 from uszn.all_asg_periods t1
      inner join
 (select uszn.pkPerson.GetPersonalReq(pk.region_id, pk.pka_people_coll_id, 25) as snils
        from uszn.all_asg_periods pk
        where pk.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
             and (pk.pka_kind_id, pk.pka_kind_region_id) in ((310,104))
             and trunc(sysdate,'mm') between pk.date_start and pk.date_end
            and uszn.pkPerson.GetPersonalReq(pk.region_id, pk.pka_people_coll_id, 25) is not null
        group by uszn.pkPerson.GetPersonalReq(pk.region_id, pk.pka_people_coll_id, 25)
        having Count(*)>1) t2
 on uszn.pkPerson.GetPersonalReq(t1.region_id, t1.pka_people_coll_id, 25)=t2.SNILS
    and t1.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
    and (t1.pka_kind_id, t1.pka_kind_region_id) in ((310,104))
    and trunc(sysdate,'mm') between t1.date_start and t1.date_end
 order by uszn.pkPerson.GetPersonalReq(t1.region_id, t1.pka_people_coll_id, 25)