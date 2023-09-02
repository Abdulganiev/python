DECLARE
	iMO          uszn.pkGen.TIntegers;
begin
 	SELECT id bulk collect INTO iMO
		FROM uszn.tsrv_regions WHERE owner_id=104 AND id not in (900, 71,72);

	FOR region in 1..iMO.count LOOP
   insert into uszn.temp$_gkv_gu (num, region_id, pc_id, id)
    SELECT row_number() over(ORDER BY t1.amount_payee_pc_id) as num,
           t1.region_id,
           t1.amount_payee_pc_id,
           max(t2.id) as id
      FROM uszn.all_po_amounts t1
           INNER JOIN
           uszn.v_ssvc_requests t2
      ON t1.region_id=iMO(region)
         and t1.region_id=t2.region_id and t1.amount_payee_pc_id=t2.pc_id
         and t1.pka_kind_id=29 and t1.pka_kind_region_id=104
         and t1.status_id in (103,107,104,101,102)
         and t1.pka_is_enabled = 1 and t1.pka_status_num = 0
         and t1.poi_payout_date>=TRUNC(ADD_MONTHS(SYSDATE, -1), 'MM')
         and t2.state_svc_id=20 and t2.state_svc_region_id=104
         and t2.status_id in (20, 30, 40)
         and uszn.pkPerson.GetDeathDate(t2.region_id, t2.pc_id) is null
         and uszn.pkPerson.GetCloseDate(t2.region_id, t2.pc_id) is null
    GROUP BY t1.region_id, t1.amount_payee_pc_id;
  END LOOP;
end;