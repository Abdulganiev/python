declare
  iRegionID Pls_Integer;

  -- вставить значение в r$_stats_rkeys
  procedure PutValue(iRegionID Pls_Integer, iKindID Pls_Integer, iValue Pls_Integer := 1) is
  begin
    update uszn.r$_stats_rkeys set id=id+iValue where kind_id=iKindID and region_id=iRegionID;
    if sql%rowcount=0 then
      insert into uszn.r$_stats_rkeys(kind_id, region_id, id) values (iKindID, iRegionID, iValue);
    end if;
  end;

begin
  -- ќчистка и заполнение r$_stats_rkeys
  delete from uszn.r$_stats_rkeys;
  -- ÷икл
  for app in
      (select *
         from uszn.all_ssvc_requests
         where (state_svc_region_id, state_svc_id) in
                 (select region_id, id from uszn.dic_state_services
                      where folder_id=2 and folder_region_id=104 and id NOT IN (17, 68) and is_actual=1)
		       and date_modified BETWEEN TRUNC(ADD_MONTHS(SYSDATE, -1), 'MM') and TRUNC(SYSDATE, 'MM')
		       --and reg_user not like 'ADMIN__'
		       and is_test_request=0
      )
  loop
    iRegionID := app.region_id;
    case
      when app.sender_region_id=0 and app.sender_id in (1, 2, 3, 9) or app.request_origin_id=5  then -- ≈ѕ√”
        PutValue(iRegionID, 3); -- (3)  ол-во за¤в. (запросов) о предостав. гос. (муниц.) услуги, поступивших от за¤вителей Ц физических лиц, через ≈ѕ√”
      when app.request_origin_id=3  then -- источник обращени¤ личное
        PutValue(iRegionID, 1); -- (3)  ол-во за¤в. (запросов) о предостав. гос. (муниц.) услуги, поступивших от за¤вителей Ц физических лиц, непосредственно в орган, предоставл¤ющий гос. (муниц.) услугу
      when app.request_origin_id=6  then -- источник обращени¤ сайт
        PutValue(iRegionID, 5); -- (3)  ол-во за¤в. (запросов) о предостав. гос. (муниц.) услуги, поступивших от за¤вителей Ц физических лиц, через официальный сайт органа, предоставл¤ющего гос. (муниц.) услугу
      when app.sender_region_id=104 and app.sender_id in (4) then -- ћ‘÷
        PutValue(iRegionID, 2); -- (2)  ол-во за¤в. (запросов) о предостав. гос. (муниц.) услуги, поступивших от за¤вителей Ц физических лиц, через ћ‘÷
      else -- (7)  ол-во за¤в. (запросов) о предостав. гос. (муниц.) услуги, поступивших от за¤вителей Ц физических лиц, иным способом
        PutValue(iRegionID, 7);
    end case;
    if app.status_id in (40) then
      -- (15) ќбщее количество положительных решений, прин¤тых по результатам предоставлени¤ гос. (муниц.) услуги, в отношении за¤вителей - физических лиц
      PutValue(iRegionID, 15);
    end if;
    if app.status_id in (50) then
      -- (19) ќбщее количество отказов, прин¤тых по результатам рассмотрени¤ за¤влений о предоставлении гос. (муниц.) услуги, в отношении за¤вителей Ц физических лиц
      PutValue(iRegionID, 19);
    end if;
  end loop;
end;
