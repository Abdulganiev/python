select uszn.pkTSrv.GetRegionName(region_id) as MO,
       'Ежемесячная выплата на 3-го ребенка' as name_kind,
       uszn.pkPerson.GetPersonalReq(region_id, payee_pc_id, 25) as payee_snils,
       uszn.pkPerson.DescribeManColl(region_id, payee_pc_id, 0) as payee,
       uszn.pkPerson.GetPersonalReq(region_id, people_id, 25) as baby_snils,
       uszn.pkPerson.DescribeManColl(region_id, people_id, 0) as baby,
       date_start, date_end, payout_date

from
(select   t2.region_id,
          t2.pka_people_coll_id as people_id,
          t2.pka_payee_pc_id as payee_pc_id,
          t2.pka_while_start_date as date_start,
          t2.pka_while_end_date as date_end,
          max(t2.poi_payout_date) as payout_date
      from   uszn.all_po_amounts t2
      where  t2.region_id in (58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70)
         and (t2.pka_kind_id, t2.pka_kind_region_id) in ((67,104)) and t2.status_id in (103,107,104,101,102) and t2.poi_payout_date >= To_Date('01.01.2023')
      group by t2.region_id, t2.pka_people_coll_id, t2.pka_payee_pc_id, t2.pka_while_start_date, t2.pka_while_end_date)
where Floor(Months_Between(sysdate, uszn.pkPerson.GetBirthDate(region_id, people_id))/12)<3