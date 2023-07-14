INSERT INTO uszn.r_ssvc_rq_collection_items(collection_id, collection_region_id, request_id, request_region_id)
    SELECT 
    DISTINCT (SELECT v2.id 
        FROM uszn.r_ssvc_request_collections v2 
        WHERE v2.name={name_collection} and 
              v2.region_id=t1.region_id),
        t1.region_id, 
        t1.id, 
        t1.region_id
    FROM uszn.temp$_gkv_gu t1
    WHERE t1.region_id={region_id} 
	     and t1.num BETWEEN 1 and (SELECT ceil(max(t2.num)/3) FROM uszn.temp$_gkv_gu t2 WHERE t2.region_id=t1.region_id)