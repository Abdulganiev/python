select DISTINCT
	uszn.pkOutDocCol.GetPCCatListOnDate(c.region_id, c.people_id, t2.pccat_id, TRUNC(LAST_DAY(SYSDATE))+1),
	t2.pccat_id
from
(select region_id,
        pka_people_coll_id as people_id
       from uszn.all_asg_amounts
       where --region_id = 62
			 region_id not in (71,72,104)
             and pka_kind_region_id=104 and pka_kind_id=49 and pka_status_num=0
             and TRUNC(LAST_DAY(SYSDATE))+1 between rap_date_start and rap_date_end
       group by region_id,pka_people_coll_id
    union
 select region_id,
        people_coll_id as people_id
       from uszn.all_pk_assigned
       where --region_id = 62 
			 region_id not in (71,72,104)
             and kind_id=49 and kind_region_id=104 and status_num=1
             and ceasing_reason_id in (3,6,8,9,10,11,12) and cease_date>=To_Date('01.01.2019')
             and uszn.pkPerson.GetDeathDate(region_id,people_coll_id) is not null
             and uszn.pkPerson.GetCloseDate(region_id,people_coll_id) is not null
       group by region_id,people_coll_id) c
  inner join
  uszn.r_categories_assigned t2
on t2.pc_region_id=c.region_id and t2.pc_id=c.people_id
   and TRUNC(LAST_DAY(SYSDATE))+1 between t2.date_start and t2.date_end
   and t2.pccat_region_id=0 and t2.pccat_id = {pccat_id}