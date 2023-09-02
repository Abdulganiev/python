DECLARE
	iiIDs        uszn.pkGen.TIntegers;
	iMO          uszn.pkGen.TIntegers;
BEGIN 
	-- заполнение таблицы
 	uszn.pkCat.FillCategoriesToCompute('(0, 1280)');
 
	SELECT id bulk collect INTO iMO
		FROM uszn.tsrv_regions WHERE owner_id=104 AND id not in (900, 71,72);
	
	FOR region in 1..iMO.count LOOP
	
		SELECT pka_people_coll_id bulk collect INTO iiIDs
         from uszn.all_asg_amounts t1
         where t1.region_id=iMO(region)
               and (t1.pka_kind_id, t1.pka_kind_region_id) in ((49,104)) and trunc(current_date, 'mm') between t1.rap_date_start and t1.rap_date_end
               and t1.amount>0 and t1.pka_is_enabled=1 and t1.pka_status_num=0;
	
	  	FOR i in 1..iiIDs.count LOOP
	  	    uszn.pkCat.ComputeCategories(iMO(region), iiIDs(i), 1);
	  	END LOOP;
	END LOOP;
END;