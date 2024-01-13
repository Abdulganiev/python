select
   t1.region_id,
   '0'||t1.region_id||' '||uszn.pkTSrv.GetRegionName(t1.region_id)||' - неверный номер карты МИР для электронного сертификата' as name,
   uszn.pkTSrv.GetRegionName(t1.region_id) as mo,
   t1.cert_kind_name,
   t1.person_id,
   t1.person_desc,
   uszn.pkPerson.GetDocInstancePC(t1.app_pdoc_id, t1.region_id) as people_id,
   uszn.pkPerson.DescribeManColl(t1.region_id, uszn.pkPerson.GetDocInstancePC(t1.app_pdoc_id, t1.region_id), 0) as people_desc,
   t1.status_name,
   t2.status_notes,
   t2.status_date_time
 from uszn.all_fk_ecerts t1
      join
      (select a1.region_id, a1.ecert_id, a1.status_notes, a1.status_date_time
         from uszn.all_fk_ecert_status_history a1 join
              (select t1.region_id, t1.ecert_id, max(status_date_time) as max_status_date_time
                from uszn.all_fk_ecert_status_history t1 where t1.status_id=1 group by t1.region_id, t1.ecert_id) a2
           on a1.region_id=a2.region_id and a1.ecert_id=a2.ecert_id and a1.status_date_time=a2.max_status_date_time) t2
       on t1.region_id=t2.region_id and t1.id=t2.ecert_id
 where t1.status_id=1 and sysdate < t1.date_end and t2.status_notes='Неверный номер карты'
order by t2.status_notes