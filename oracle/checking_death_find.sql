select d1.region_id, d1.pd_id
         from uszn.all_personal_doc_reqs d1
         where d1.region_id=71 and d1.pd_class_id=18331 and d1.class_id=18356 and d1.value is not null
               and date_created between trunc(sysdate - 1, 'dd') and trunc(sysdate, 'dd')