select t.pc_id, t.region_id, t.id, t.message_guid, t.adr, t.request_pdoc_id, t.smev_message_id, t.state_service_name,
 (case when upper(t.adr) like '%НОВЫЙ У%' then 58
       when upper(t.adr) like '%КРАСНОСЕЛЬКУП%' then 59
       when upper(t.adr) like '%САЛЕХАРД%' then 60
       when upper(t.adr) like '%ЛАБЫТНАНГ%' then 62
       when upper(t.adr) like '%ХАРП%' then 62
       when upper(t.adr) like '%ПРИУРАЛ%' then 61
       when upper(t.adr) like '%НАДЫМ%' then 63
       when upper(t.adr) like '%ГУБК%' then 64
       when upper(t.adr) like '%ПУРПЕ%' then 64
       when upper(t.adr) like '%МУРАВ%' then 65
       when upper(t.adr) like '%НОЯБ%' then 66
       when upper(t.adr) like '%ПУРОВСК%' then 67
       when upper(t.adr) like '%ЯМАЛЬ%' then 68
       when upper(t.adr) like '%ШУРЫШ%' then 69
       when upper(t.adr) like '%ТАЗ%' then 70
   else 0 end) as mo_out
from
(select
  r.region_id||'-'||r.pc_id as pc_id,
  r.region_id,
  r.id,
  uszn.pkXMLUtils.GUIDToStr(r.message_guid) as message_guid,

  (case
    when uszn.pkPerson.GetPersonalReq(r.region_id, r.pc_id, 15) is not null
      then uszn.pkPerson.GetPersonalReq(r.region_id, r.pc_id, 15)

    when (select uszn.StrCommaConcat(value) from uszn.all_personal_doc_reqs q
           where q.region_id=r.region_id and q.pdoc_id=uszn.pkPerson.GetMainPersonIdentity(r.region_id, r.pc_id, 0) and class_id=8434) is not null
      then (select uszn.StrCommaConcat(value) from uszn.all_personal_doc_reqs q
             where q.region_id=r.region_id and q.pdoc_id=uszn.pkPerson.GetMainPersonIdentity(r.region_id, r.pc_id, 0) and class_id=8434)

    when (select uszn.StrCommaConcat(uszn.pkGen.StripRgnPrefix(decoded_value)) from uszn.all_personal_doc_reqs q
           where q.class_id=14531 and q.region_id=r.region_id and q.pdoc_id=r.request_pdoc_id) is not null
      then (select uszn.StrCommaConcat(uszn.pkGen.StripRgnPrefix(decoded_value)) from uszn.all_personal_doc_reqs q
             where q.class_id=14531 and q.region_id=r.region_id and q.pdoc_id=r.request_pdoc_id)

    when (select uszn.StrCommaConcat(uszn.pkGen.StripRgnPrefix(decoded_value)) from uszn.all_personal_doc_reqs q
           where q.class_id=18784 and q.region_id=r.region_id and q.pdoc_id=r.request_pdoc_id) is not null
      then (select uszn.StrCommaConcat(uszn.pkGen.StripRgnPrefix(decoded_value)) from uszn.all_personal_doc_reqs q
             where q.class_id=18784 and q.region_id=r.region_id and q.pdoc_id=r.request_pdoc_id)

    when (select uszn.StrCommaConcat(uszn.pkGen.StripRgnPrefix(decoded_value)) from uszn.all_personal_doc_reqs q
           where q.class_id=18854 and q.region_id=r.region_id and q.pdoc_id=r.request_pdoc_id) is not null
      then (select uszn.StrCommaConcat(uszn.pkGen.StripRgnPrefix(decoded_value)) from uszn.all_personal_doc_reqs q
             where q.class_id=18854 and q.region_id=r.region_id and q.pdoc_id=r.request_pdoc_id)
             
    end) as adr,

 r.request_pdoc_id,
 r.smev3_inc_message_id as smev_message_id,
 r.state_service_name

from
  uszn.all_ssvc_requests r
  inner join
  uszn.all_smev3_data_kinds t2
on
  r.region_id=71 and r.date_created>=To_Date('01.01.2022') and
  r.data_kind_region_id=t2.region_id and r.data_kind_id=t2.id
  and r.status_id in (1, 2, 3, 4, 10, 20, 30, 40)
  and (r.region_id, r.id) not in
      ((104, 1), (104, 2), (104, 18), (104, 27), (104, 30), (104, 9),
       (104, 31), (104, 13), (104, 14), (104, 15), (104, 19), (104, 17), (104, 32))
  and pc_id != 140264) t