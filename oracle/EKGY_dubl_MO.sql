select  uszn.pkTSrv.GetRegionName(a1.pd_region_id) as MO,
       a1.pd_region_id||'-'||a1.pd_pc_id as id,
       a1.pd_pc_desc,
       a1.value
    from uszn.all_personal_doc_reqs a1 join
  (select t1.region_id, t1.value from uszn.r_personal_doc_reqs t1
    where t1.class_id=18900 group by t1.region_id, t1.value having count(t1.value)>1 ) a2
  on a1.region_id=a2.region_id and a1.value=a2.value
     and a1.class_id=18900