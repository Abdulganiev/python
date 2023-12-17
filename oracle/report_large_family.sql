create table uszn.temp$_r_large_family as

select distinct t1.pc_region_id as region_id, --t1.pc_id as coll_id,
       --uszn.pkPCAddr.GetPCAddress(t1.pc_region_id, t1.pc_id, 1, null, sysdate, 0) as coll_adr,
       uszn.pkXMLUtils.GuidToStr(uszn.pkJUtil.GetGUIDRAW(t1.pc_region_id*1000000 + t1.pc_id)) as coll_guid,
       case when uszn.pkPIC.GetPersonByRole(t1.pc_region_id, t1.pc_id, 9, sysdate) is not null then 1 else 0 end as father,
       case when uszn.pkPIC.GetPersonByRole(t1.pc_region_id, t1.pc_id, 8, sysdate) is not null then 1 else 0 end as mother,
       uszn.pkCat.HasCategory(t1.pc_id, t1.pc_region_id, 515, 0, sysdate) as children_3,
       uszn.pkCat.HasCategory(t1.pc_id, t1.pc_region_id, 516, 0, sysdate) as children_4,
       uszn.pkCat.HasCategory(t1.pc_id, t1.pc_region_id, 517, 0, sysdate) as children_5,
       uszn.pkCat.HasCategory(t1.pc_id, t1.pc_region_id, 518, 0, sysdate) as children_6,
       uszn.pkCat.HasCategory(t1.pc_id, t1.pc_region_id, 519, 0, sysdate) as children_7,
       uszn.pkCat.HasCategory(t1.pc_id, t1.pc_region_id, 910, 0, sysdate) as children_8to,
       uszn.pkCat.HasCategory(t1.pc_id, t1.pc_region_id, 1172, 0, sysdate) as young_family,
       uszn.pkCat.HasCategory(t1.pc_id, t1.pc_region_id, 19, 104, sysdate) as poor_family,
       --t2.people_id,
       uszn.pkXMLUtils.GuidToStr(uszn.pkJUtil.GetGUIDRAW(t2.region_id*1000000 + t2.people_id)) as people_guid,
       t2.role_class_name,
       Floor(Months_Between(sysdate, uszn.pkPerson.GetBirthDate(t2.region_id, t2.people_id))/12) as age,
       uszn.pkPerson.GetSex(t1.pc_id, t1.pc_region_id) as gender,
       case when uszn.pkCat.HasCategory(t2.people_id, t2.region_id, 905, 0, sysdate)=1 and
                 uszn.pkCat.HasCategory(t2.people_id, t2.region_id, 1091, 0, sysdate)=1 then 1 else 0 end as student,
       uszn.pkCat.HasCategory(t2.people_id, t2.region_id, 325, 0, sysdate) as invalid
       
from uszn.r_categories_assigned t1
     inner join
     uszn.v_coll_membership_periods t2
  on --t1.pc_region_id=63
     t1.pc_region_id in  (58,59,60,61,62,63,64,65,66,67,68,69,70)
     and t1.pc_region_id=t2.region_id and t1.pc_id=t2.coll_id
     and sysdate between t1.date_start and t1.date_end and (t1.pccat_id, t1.pccat_region_id) in ((515,0))
     and sysdate between t2.date_start and t2.date_end and t2.coll_class_id=6 --and t2.role_class_id in (8, 9)