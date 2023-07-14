select
  '0'||r.region_id||' - '||uszn.pkTSrv.GetRegionName(r.region_id)||' ошибки при отправке в ГИС ЖКХ в '||to_char(sysdate, 'yyyy-mm') as name,
  r.region_id||'-'||r.request_subject_id as pc_id,
  trim(
  uszn.pkPerson.GetDocReqValue(r.region_id, 18410, r.request_pdoc_id)||' '||
  uszn.pkPerson.GetDocReqValue(r.region_id, 18411, r.request_pdoc_id)||' '||
  uszn.pkPerson.GetDocReqValue(r.region_id, 18412, r.request_pdoc_id)) as FIO,
  uszn.pkPerson.GetDocReqValue(r.region_id, 18415, r.request_pdoc_id) as adr,
  r.status_message
from
  uszn.all_interdept_requests r
where
  r.region_id in (select id from uszn.v_filter_regions_down where filter_region_id=104) and
  r.date_created between trunc(sysdate, 'mm') and trunc(sysdate, 'dd')-10 and
  (r.data_kind_region_id,r.data_kind_id) in ((0,71)) and
  r.status_id in (7,5)