select
  To_Char(ADD_MONTHS(TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q'), 3)-1, 'DDMMY')||
  30||
  '.'||
(case {region_id}
  when 60 then '001'
  when 62 then '002'
  when 63 then '003'
  when 66 then '004'
  when 58 then '005'
  when 65 then '006'
  when 59 then '007'
  when 61 then '008'
  when 67 then '009'
  when 70 then '010'
  when 69 then '011'
  when 68 then '012'
  when 64 then '014'
  else '000'
end)
from dual
