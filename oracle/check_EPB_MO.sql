select distinct t1.region_id
 from uszn.all_asg_periods t1
      inner join
 (select uszn.pkPerson.GetPersonalReq(pk1.region_id, pk1.pka_people_coll_id, 25) as snils
from uszn.all_asg_periods pk1 join uszn.all_asg_amounts pk2
  on pk1.id=pk2.rai_period_id and pk1.region_id=pk2.region_id
     and pk1.pka_kind_id=310 and pk1.pka_kind_region_id=104
     and trunc(sysdate,'dd') between pk1.date_start and pk1.date_end
     and pk2.rai_item_region_id=104 and pk2.rai_item_id=696
     and uszn.pkPerson.GetCloseDate(pk1.pka_region_id, pk1.pka_people_coll_id) is null
     and uszn.pkPerson.GetDeathDate(pk1.pka_region_id, pk1.pka_people_coll_id) is null
     and uszn.pkPerson.GetPersonalReq(pk1.region_id, pk1.pka_people_coll_id, 25) is not null
     and pk1.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
group by uszn.pkPerson.GetPersonalReq(pk1.region_id, pk1.pka_people_coll_id, 25)
having count(*)>1) t2
 on uszn.pkPerson.GetPersonalReq(t1.region_id, t1.pka_people_coll_id, 25)=t2.SNILS
    and t1.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
    and (t1.pka_kind_id, t1.pka_kind_region_id) in ((310,104))
    and trunc(sysdate,'dd') between t1.date_start and t1.date_end