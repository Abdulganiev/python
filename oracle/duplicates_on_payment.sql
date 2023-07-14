select 
    t1.region_id,
    uszn.pkTSrv.GetRegionName(t1.region_id),
    t1.pka_people_coll_desc,
    t1.pka_kind_name,
    t1.SNILS
from
(select
    distinct t1.region_id,
             t1.pka_people_coll_desc,
             t1.pka_kind_name,
             uszn.pkPerson.GetPersonalReq(t1.region_id, t1.pka_people_coll_id, 25) as SNILS
 from uszn.all_asg_periods t1
      inner join
 (select pk.pka_people_coll_desc, pk.pka_kind_name
        from uszn.all_asg_periods pk
        where pk.region_id not in (104, 71, 72) and pk.pka_is_enabled = 1 and pk.pka_status_num = 0 and
   (pk.pka_kind_id, pk.pka_kind_region_id) in
   ((133,0),(22,0),(134,0),(147,0),(132,0),(104,0),(76,104),(21,104),(80,104),(23,104),(78,104),(81,104),(14,104),(141,0),(140,0),(139,0),(99,0),(103,0),
   (98,0),(102,0),(138,0),(175,0),(150,0),(202,104),(203,104),(204,104),(205,104),(160,0),(142,0),(137,0),(9,59),(10,59),(29,104),(53,104),(75,104),
   (58,104),(57,104),(51,0),(165,0),(201,0),(164,0),(170,0),(58,0),(161,0),(48,0),(122,0),(112,104),(63,104),(61,104),(206,104),(66,104),(88,104),
   (89,104),(11,104),(51,104),(50,104),(136,0),(110,0),(149,0),(151,0),(179,0),(37,0),(24,0),(224,0),(119,0),(46,0),(178,0),(40,0),(38,0),(207,0),
   (2,0),(2,58),(17,60),(67,104),(47,104),(56,104),(153,0),(112,0),(152,0),(101,0),(14,60),(2,69),(210,104),(4,69),(1,69),(9,104),(18,104),(24,104),
   (25,104),(20,104),(19,104),(84,104),(5,104),(16,104),(83,104),(15,104),(70,104),(69,104),(49,104),(60,104),(55,104),(54,104),(28,104),(27,104),
   (13,104),(52,104),(10,104),(4,104),(2,104),(7,104),(48,104),(166,0),(155,0),(135,0),(172,0),(173,0),(176,0),(205,0),(167,0),(177,0),(148,0),(157,0),
   (129,0),(168,0),(77,104),(12,104),(32,104),(31,104),(30,104),(62,104),(26,104),(207,104),(17,104),(6,104)) and
   trunc(sysdate,'mm') between pk.date_start and pk.date_end and uszn.pkPerson.IsColl(pk.region_id, pk.pka_people_coll_id, 0)=0
 group by pk.pka_people_coll_desc, pk.pka_kind_name
 having Count(*)>1) t2
 on t1.pka_people_coll_desc=t2.pka_people_coll_desc and t1.pka_kind_name=t2.pka_kind_name) t1