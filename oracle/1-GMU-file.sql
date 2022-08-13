select to_char(TRUNC(SYSDATE, 'MM') - 1, 'yyyy-mm')||' - '||RTRIM(RPAD(name, 70))
  from uszn.dic_state_services
  where region_id=104 and id={SERVICE}