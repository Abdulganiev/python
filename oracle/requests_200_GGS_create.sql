CREATE TABLE uszn.temp$_200_GGS
as
SELECT row_number() over(partition by t2.region_id ORDER BY t2.pc_id) as num,
       t2.region_id,
       t2.pc_id,
       max(t2.id) as id
             FROM uszn.all_po_amounts t1
                  INNER JOIN uszn.all_ssvc_requests t2
             ON t1.region_id = 71
                and t1.region_id=t2.region_id and t1.amount_payee_pc_id=t2.pc_id and
                   (t1.pka_kind_id, t1.pka_kind_region_id) in ((89,104),(11,104),(51,104),(50,104),(80,104),(78,104),(81,104)) and
                   t1.status_id in (103,107,104,101,102) and
                   t1.pka_is_enabled = 1 and t1.pka_status_num = 0 and
                   t1.poi_payout_date>=TRUNC(ADD_MONTHS(SYSDATE, -2), 'MM')
                   and (state_svc_id,state_svc_region_id) in ((1,104),(9,104)) and
                   t2.status_id in (20, 30, 40)
GROUP BY t2.region_id, t2.pc_id