DECLARE
	iiIDs        uszn.pkGen.TIntegers;
	iMO          uszn.pkGen.TIntegers;
BEGIN 
	-- заполнение таблицы
 	uszn.pkCat.FillCategoriesToCompute('(0,1280)');
 
	SELECT id BULK COLLECT INTO iMO
		FROM uszn.tsrv_regions WHERE owner_id=104 AND id NOT IN (900, 71,72);
	
	FOR region in 1..iMO.COUNT LOOP
	
      SELECT t1.pc_id BULK COLLECT INTO iiIDs
		  FROM uszn.r_personal_docs t1
			   join
			   uszn.v_people_and_colls t2
			ON t1.region_id=t2.region_id AND t1.pc_id=t2.id
			   AND t1.region_id=iMO(region)
			   AND t1.class_id=7119
			   AND t2.death_date IS NOT NULL AND t2.close_date IS NOT NULL;
	
	  	FOR i IN 1..iiIDs.count LOOP
	  	    uszn.pkCat.ComputeCategories(iMO(region), iiIDs(i), 0);
	  	END LOOP;
	END LOOP;
END;