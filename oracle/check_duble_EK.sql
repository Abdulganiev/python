select
  pc.region_id,
  uszn.pkTSrv.GetRegionName(pc.region_id) as mo,
  pc.region_id||'-'||pc.id as pc_id,
  pc.pc_desc,
  uszn.pkPerson.GetPersonalReq(pc.region_id, pc.id, 25) as SNILS
from
  (select region_id, pc_id as id from uszn.r_personal_docs where class_id=18899 group by region_id, pc_id having count(id)>1) q
   join uszn.v_people_and_colls pc
on pc.region_id=q.region_id and pc.id=q.id