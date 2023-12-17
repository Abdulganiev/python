select distinct pc_region_id
from (
select t1.pc_region_id from uszn.r_categories_assigned t1 join
     (select uszn.pkPerson.DescribeManColl(pk.pc_region_id, pk.pc_id, 0) as pc_desc
        from uszn.r_categories_assigned pk
        where pk.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
             and (pk.pccat_region_id, pk.pccat_id) in ((104, 11)) and sysdate between pk.date_start and pk.date_end
        group by uszn.pkPerson.DescribeManColl(pk.pc_region_id, pk.pc_id, 0)
        having Count(*)>1) t2
 on uszn.pkPerson.DescribeManColl(t1.pc_region_id, t1.pc_id, 0)=t2.pc_desc
    and t1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
    and (t1.pccat_region_id, t1.pccat_id) in ((104, 11)) and sysdate between t1.date_start and t1.date_end
 union all
select t1.pc_region_id from uszn.r_categories_assigned t1 join
     (select uszn.pkPerson.DescribeManColl(pk.pc_region_id, pk.pc_id, 0) as pc_desc
        from uszn.r_categories_assigned pk
        where pk.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
             and (pk.pccat_region_id, pk.pccat_id) in ((0, 242)) and sysdate between pk.date_start and pk.date_end
        group by uszn.pkPerson.DescribeManColl(pk.pc_region_id, pk.pc_id, 0)
        having Count(*)>1) t2
 on uszn.pkPerson.DescribeManColl(t1.pc_region_id, t1.pc_id, 0)=t2.pc_desc
    and t1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
    and (t1.pccat_region_id, t1.pccat_id) in ((0, 242)) and sysdate between t1.date_start and t1.date_end
)