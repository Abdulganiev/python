select 'Отчет ГСП за период с '||to_char(trunc(sysdate, 'yy'))||' по '||to_char(trunc(sysdate, 'mm')-1) from dual