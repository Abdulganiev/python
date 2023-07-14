select
  '0'||pc.region_id||' - Дубликатов по ФИО и др на '||sysdate||' - '||count(1) over(ORDER BY pc.region_id) as name_mo,
  uszn.pkTSrv.GetRegionName(pc.region_id) as mo,
  pc.region_id||'-'||pc.id as id,
  pc.pc_desc
from
  uszn.v_people_and_colls pc,
  (select Upper(first_name) as ufn, Upper(middle_name) as umn, Upper(last_name) as uln, birth_date
    from uszn.r_people_and_colls
     where region_id={region_id} and is_coll_instance=0
    group by Upper(first_name), Upper(middle_name), Upper(last_name), birth_date
    having Count(*)>1) d
where pc.region_id={region_id} and
  Upper(pc.first_name)=d.ufn and Upper(pc.last_name)=d.uln and
  ((pc.middle_name is null and d.umn is null) or Upper(pc.middle_name)=d.umn) and
  pc.birth_date=d.birth_date
order by pc.pc_desc asc nulls last