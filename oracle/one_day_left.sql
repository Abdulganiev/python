select
    (case obr.region_id
  when 71 then
    (case obr.reg_org_short_name
      when 'ГКУ ЯНАО «Центр социальных технологий Ямало-Ненецкого автономного округа»'
         then '0'||obr.region_id||'-'||obr.reg_org_short_name||'-'||to_char(SysDate,'yyyy-mm-dd')||' нарушение сроков'
      else '0'||obr.region_id||'-'||obr.state_svc_region_id||'-'||obr.state_svc_id||'-'||to_char(SysDate,'yyyy-mm-dd')||' нарушение сроков' end)
  else '0'||obr.region_id||'-'||obr.reg_org_short_name||'-'||to_char(SysDate,'yyyy-mm-dd')||' нарушение сроков' end) as name,
    
    '0'||obr.region_id||'-'||obr.reg_org_name,
    obr.region_id||'-'||obr.pc_id,
    obr.pc_desc,
    obr.id,
    obr.request_pdoc_id,
    obr.state_svc_variant_name,
    obr.state_service_name,
    (case to_char(obr.sender_region_id||'-'||obr.sender_id)
          when '0-1' then 'ЕПГУ'
          when '0-2' then 'ЕПГУ'
          when '0-3' then 'ЕПГУ'
          when '0-9' then 'ЕПГУ'
          when '104-4' then 'МФЦ'
          else 'Личное посещение' end),
    to_date(obr.reg_date),    
    (case when gu.power_day is not null
          then (gu.power_day - uszn.temp$_PowerDaysCount(obr.reg_date, sysdate))
          else (gu.cal_day-round(sysdate-obr.reg_date, 0)) end),
    gu.cal_day,
    round(sysdate-obr.reg_date, 0),
    gu.power_day,    
    uszn.temp$_PowerDaysCount(obr.reg_date, sysdate)
  from uszn.all_ssvc_requests obr,
       uszn.temp$_check_GU_new GU
 where obr.reg_date>to_date('01.03.2021') and obr.status_is_final=0 and obr.region_id not in (104,72) and
       obr.case_number not like ('%test%') and
       upper(obr.reg_user) not like 'ADMIN__' and
       obr.state_svc_region_id=gu.region_id and obr.state_svc_variant_id=gu.id and obr.state_svc_id=gu.SSVC_ID and obr.is_test_request=0 and
       (obr.state_svc_region_id, obr.state_svc_id) in ((104,38),(104,37),(104,24),(104,35),(104,6),(104,25),(104,40),(104,8),(104,29),(104,4),(104,3),(104,28),
                                           (104,26),/*(104,1),*/(104,16),(104,39),(104,23),(104,2),/*(104,18),*/(104,27),(104,30),(104,5),(104,21),(104,9),
                                           (104,11),(104,31),(104,34),(104,13),(104,14),(104,7),(104,20),(104,15),(104,12),(104,10),(104,22),(104,19),
                                           (104,32),(104,17),(104,36))
      and (case when gu.power_day is not null
            then (gu.power_day - uszn.temp$_PowerDaysCount(obr.reg_date, sysdate))
            else (gu.cal_day-round(sysdate-obr.reg_date, 0)) end)<1