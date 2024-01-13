select distinct pc.region_id
from (select region_id, pc_id as id from uszn.r_personal_docs where class_id=18899 group by region_id, pc_id having count(id)>1) q
     join uszn.v_people_and_colls pc
   on pc.region_id=q.region_id and pc.id=q.id