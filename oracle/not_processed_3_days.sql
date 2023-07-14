    select
  '0'||t1.region_id||'-'||uszn.pkTSrv.GetRegionName(t1.region_id)||'-'||to_char(SysDate,'yyyy-mm-dd')||' - '||'не обработанные гос_услуги' as name,
  t1.region_id||'-'||t1.pc_id as pc_id, -- ID человека
  t1.pc_desc, -- Описание заявителя
  t1.id, -- ID заявления
  ' '||to_char(t1.date_created,'dd.mm.yyyy'), -- Дата подачи
  t1.state_service_name, -- Гос_услуга
  t1.status_name, -- Статус
  t1.sender_display_name -- Откуда пришло заявление
from
  uszn.all_ssvc_requests t1
  inner join
  uszn.all_state_services t2
on
  t1.region_id in (select id from uszn.tsrv_regions where owner_id=104 and id not in (71, 72) )
  and t1.state_svc_region_id=t2.region_id and t1.state_svc_id=t2.id
  and (sysdate-t1.date_created)>3 and t1.status_id in (1,2,10)
  and t1.date_created>to_date('01.01.2020')
  and t2.folder_region_id=104 and t2.folder_id=2