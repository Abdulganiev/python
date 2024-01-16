select distinct
             t1.region_id,
             uszn.pkTSrv.GetRegionName(t1.region_id) as mo,
             t1.region_id||'-'||t1.people_id as pc_id,
             uszn.pkPerson.DescribeManColl(t1.region_id, t1.people_id, 0) as people_desc,
             t1.SNILS
from
(select t1.region_id, t1.people_id, t1.SNILS
  from uszn.temp$_r_EPB t1 join
       (select pers_id from uszn.temp$_r_EPB
         where pers_id is not null group by pers_id having count(*)>1) t2
    on t1.pers_id=t2.pers_id
  union all
 select t1.region_id, t1.people_id, t1.SNILS
  from uszn.temp$_r_EPB t1 join
       (select snils from uszn.temp$_r_EPB
         where snils is not null group by snils having count(*)>1) t2
    on t1.snils=t2.SNILS) t1