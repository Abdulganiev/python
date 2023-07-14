CREATE TABLE uszn.temp$_gkv_gu
as
SELECT row_number() over(partition by t2.region_id ORDER BY t2.pc_id) as num,
       t2.region_id,
       t2.pc_id,
       max(t2.id) as id
  FROM uszn.all_po_amounts t1
       INNER JOIN 
       uszn.all_ssvc_requests t2
  ON t1.region_id not in (71, 72, 104)
     and t1.region_id=t2.region_id and t1.amount_payee_pc_id=t2.pc_id 
     and (t1.pka_kind_id, t1.pka_kind_region_id) in ((29,104)) 
     and t1.status_id in (103,107,104,101,102) 
     and t1.pka_is_enabled = 1 and t1.pka_status_num = 0 
     and t1.poi_payout_date>=TRUNC(ADD_MONTHS(SYSDATE, -1), 'MM')
     and (state_svc_id,state_svc_region_id) in ((20,104)) 
     and t2.status_id in (20, 30, 40) 
     and uszn.pkPerson.GetDeathDate(t2.region_id, t2.pc_id) is null 
     and uszn.pkPerson.GetCloseDate(t2.region_id, t2.pc_id) is null
GROUP BY t2.region_id, t2.pc_id