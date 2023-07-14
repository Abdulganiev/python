select t.pc_id, t.region_id, t.id, t.message_guid, t.adr, t.request_pdoc_id, t.smev_message_id, t.state_service_name,
 (case when upper(t.adr) like '%НОВЫЙ У%' then 58
       when upper(t.adr) like '%КРАСНОСЕЛЬКУП%' then 59
       when upper(t.adr) like '%САЛЕХАРД%' then 60
       when upper(t.adr) like '%ЛАБЫТНАНГ%' then 62
       when upper(t.adr) like '%ХАРП%' then 62
       when upper(t.adr) like '%ПРИУРАЛ%' then 61
       when upper(t.adr) like '%НАДЫМ%' then 63
	   when upper(t.adr) like UPPER('%Лонгьюган%') then 63
       when upper(t.adr) like '%ГУБК%' then 64
       when upper(t.adr) like '%ПУРПЕ%' then 64
       when upper(t.adr) like '%МУРАВ%' then 65
       when upper(t.adr) like '%НОЯБ%' then 66
       when upper(t.adr) like '%ПУРОВСК%' then 67
       when upper(t.adr) like '%ЯМАЛЬ%' then 68
       when upper(t.adr) like '%ШУРЫШ%' then 69
       when upper(t.adr) like '%МУЖИ%' then 69
       when upper(t.adr) like '%ТАЗ%' then 70
   else 0 end) as mo_out
from
(select
  r.region_id||'-'||r.pc_id as pc_id,
  r.region_id,
  r.id,
  uszn.pkXMLUtils.GUIDToStr(r.message_guid) as message_guid,

 case
  when uszn.pkPerson.GetPersonalReq(r.region_id, r.pc_id, 15) is not null
   then uszn.pkPerson.GetPersonalReq(r.region_id, r.pc_id, 15)

  when (select value from uszn.all_personal_doc_reqs q
          where q.region_id=r.region_id and q.pdoc_id=uszn.pkPerson.GetMainPersonIdentity(r.region_id, r.pc_id, 0) and class_id=8434) is not null
   then (select value from uszn.all_personal_doc_reqs q
          where q.region_id=r.region_id and q.pdoc_id=uszn.pkPerson.GetMainPersonIdentity(r.region_id, r.pc_id, 0) and class_id=8434)

  when (select uszn.StrCommaConcat(uszn.pkGen.StripRgnPrefix(decoded_value)) from uszn.all_personal_doc_reqs q
          where q.class_id=10367 and q.region_id=r.region_id and q.pdoc_id=r.request_pdoc_id) is not null
   then (select uszn.StrCommaConcat(uszn.pkGen.StripRgnPrefix(decoded_value)) from uszn.all_personal_doc_reqs q
          where q.class_id=10367 and q.region_id=r.region_id and q.pdoc_id=r.request_pdoc_id)

    end as adr,

 r.request_pdoc_id,
 r.smev_message_id,
 r.state_service_name

from
  uszn.all_ssvc_requests r
where
  r.region_id=71 and r.date_created>=To_Date('01.01.2022') and
  (r.state_svc_region_id,r.state_svc_id) in ((104, 3),(104, 5),(104, 6),(104, 7),(104, 8),(104,10),(104,11),(104,25),(104,16),
                                             (104,12),(104,20),(104,21),(104,24),(104,26),(104,28),
                                             (104,29),(104,34),(104,35),(104,37),(104,38),(104,39),(104,40),
                                             (104,13),(104,14))
  and r.request_origin_id in (2,5,1,4) and r.status_id not in (40,50)
  and r.smev3_inc_message_id is null
  and r.is_test_request=0
  and r.data_kind_id is null
  and upper(r.case_number) not like ('%TEST%')) t