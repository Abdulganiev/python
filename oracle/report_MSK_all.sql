CREATE TABLE uszn.temp$_msk_all 
as
select a.*,
( case
   when law2='на третьего и последующих детей' and pay=0 then 500000-a.summa_resh 
   when law2='на второго ребенка'  and pay=0 then 150000-a.summa_resh
   else 0 end) as money_left
from

(
select a2.sv, a2.MO_name, a2.region_id, a2.people_id, a2.law2, nvl(a1.summa_resh, 0) as summa_resh, directed,
       uszn.pkCat.HasCategory(a2.people_id, a2.region_id, 18, 104, sysdate, null) as cat,
       uszn.pkPerson.GetPersonalReq(a2.region_id, a2.people_id, 25) as snils,
 ( case
   when a1.law2='на третьего и последующих детей' and a1.data_obr<to_date('01.01.2020') and a1.summa_resh >='350000' then 1
   when a1.law2='на третьего и последующих детей' and a1.data_obr>=to_date('01.01.2020') and a1.summa_resh >='500000' then 1
   when a1.law2='на второго ребенка' and summa_resh >= '150000' then 1
   else 0 end) as pay
  from

  ( select t1.sv, t1.MO_sert, t1.law2,
       max(t1.data_obr) as data_obr,
       sum(t1.summa_resh) as summa_resh,
       uszn.StrCommaConcat(distinct directed) as directed
     from uszn.temp$_msk_resh t1
     where t1.resh not like '%Отказать%'
         and (t1.data_obr between to_date('01.01.2000') and to_date('31.12.2020') and t1.region_id=71
              or
              t1.data_obr between to_date('01.01.2021') and to_date('31.12.2021') and t1.region_id!=71)
    group by t1.sv, t1.MO_sert, t1.law2 ) a1

     right join uszn.temp$_msk_cert a2
      on a1.sv=a2.sv
      ) a