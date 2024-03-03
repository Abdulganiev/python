CREATE TABLE uszn.temp$_msk_all AS
SELECT 
     a.sv,
     a.MO_name,
     a.region_id,
     a.people_id,
     a.law2,
     a.summa_resh,
     a.directed,
     a.cat,
     a.snils,
     a.pay,
     (CASE
         WHEN law2='на третьего и последующих детей' AND pay=0 THEN 500000-a.summa_resh
         WHEN law2='на второго ребенка'  AND pay=0 THEN 150000-a.summa_resh
      ELSE 0 END) AS money_left
FROM

(
SELECT a2.sv, a2.MO_name, a2.region_id, a2.people_id, a2.law2, nvl(a1.summa_resh, 0) AS summa_resh, directed,
       uszn.pkCat.HasCategory(a2.people_id, a2.region_id, 18, 104, sysdate, null) AS cat,
       uszn.pkPerson.GetPersonalReq(a2.region_id, a2.people_id, 25) AS snils,
 ( CASE
   WHEN a1.law2='на третьего и последующих детей' AND a1.data_obr <  TO_DATE('01.01.2020') AND a1.summa_resh >= 350000 THEN 1
   WHEN a1.law2='на третьего и последующих детей' AND a1.data_obr >= TO_DATE('01.01.2020') AND a1.summa_resh >= 500000 THEN 1
   WHEN a1.law2='на второго ребенка' AND summa_resh >= 150000 THEN 1
   ELSE 0 END) AS pay
  FROM uszn.temp$_msk_cert a2
   LEFT JOIN
  ( SELECT t1.sv, t1.MO_sert, t1.law2,
       max(t1.data_obr) AS data_obr,
       sum(t1.summa_resh) AS summa_resh,
       uszn.StrCommaConcat(DISTINCT directed) AS directed
     FROM uszn.temp$_msk_resh t1
     WHERE t1.resh NOT LIKE '%Отказать%'
         AND (t1.data_obr BETWEEN TO_DATE('01.01.2000') AND TO_DATE('31.12.2020') AND t1.region_id=71
              OR
              t1.data_obr BETWEEN TO_DATE('01.01.2021') AND TO_DATE('31.12.2021') AND t1.region_id!=71)
    GROUP BY t1.sv, t1.MO_sert, t1.law2 ) a1
   ON a1.sv=a2.sv
      ) a 