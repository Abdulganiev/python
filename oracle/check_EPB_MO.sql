select distinct region_id
from
( select t1.region_id
   from uszn.temp$_r_EPB t1 join
        (select snils from uszn.temp$_r_EPB
          where snils is not null group by snils having count(*)>1) t2
       on t1.snils=t2.SNILS
   union all
  select t1.region_id
   from uszn.temp$_r_EPB t1 join
        (select pers_id from uszn.temp$_r_EPB
          where pers_id is not null group by pers_id having count(*)>1) t2
       on t1.pers_id=t2.pers_id)