DECLARE
	iiIDs        uszn.pkGen.TIntegers;
	iMO          uszn.pkGen.TIntegers;
BEGIN 
	-- заполнение таблицы
 	uszn.pkCat.FillCategoriesToCompute('(104,229),(104,196),(104,213),(104,197),(104,226),(104,198),(104,199),(104,230),(104,219),(104,220),(104,221),(104,227),(104,222),(104,223),(104,231),(104,208),(104,212),(104,209),(104,225),(104,210),(104,211),(104,232),(104,215),(104,214),(104,216),(104,228),(104,217),(104,218)');
 
	SELECT id BULK COLLECT INTO iMO
		FROM uszn.tsrv_regions WHERE owner_id=104 AND id NOT IN (900, 71,72);
	
	FOR region in 1..iMO.count LOOP
	
		SELECT pc.people_id BULK COLLECT INTO iiIDs
		     FROM uszn.r_people_in_colls pc
             WHERE pc.region_id=iMO(region) AND pc.coll_role_class_id IN (110,111);
	
	  	FOR i in 1..iiIDs.count LOOP
	  	    uszn.pkCat.ComputeCategories(iMO(region), iiIDs(i), 0);
	  	END LOOP;
	END LOOP;
END;