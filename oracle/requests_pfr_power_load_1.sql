INSERT INTO uszn.r_pc_collection_items(collection_id, collection_region_id, pc_id, pc_region_id)
SELECT  71, 104, id, region_id
    FROM uszn.temp$_pfr_power t1
    WHERE t1.num BETWEEN 1 and (SELECT ceil(max(t2.num)/4) FROM uszn.temp$_pfr_power t2)