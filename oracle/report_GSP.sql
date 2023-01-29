select *
from
(	select pka_region_id,
        uszn.pkTSrv.GetRegionName(pka_region_id),
        poi_item_name,
        count(pka_people_coll_id),
        sum(pc_count_applied_to)
from
(select distinct
  case t1.poi_item_name
   when 'Государственная социальная помощь на одиноко проживающего гражданина' then 'Ежемесячная адресная социальная помощь на одиноко проживающего гражданина'
   when 'Государственная социальная помощь на учащегося ПТУ, ВУЗа' then 'Ежемесячная адресная социальная помощь на учащегося ПТУ, ВУЗа'
   when 'Государственная социальная помощь на члена семьи' then 'Ежемесячная адресная социальная помощь на члена семьи'
   else t1.poi_item_name end as poi_item_name
   ,
  t1.pka_region_id,
  t1.pka_people_coll_id,
  max(t1.pc_count_applied_to) as pc_count_applied_to
from uszn.all_po_amounts t1
where (t1.pka_kind_region_id, t1.pka_kind_id) in ((104, 279), (104, 83), (104, 84))
      -- and t1.payout_doc_doc_date between trunc(sysdate, 'yy') and trunc(sysdate, 'mm')-1
      and t1.payout_doc_doc_date between trunc(trunc(sysdate, 'mm')-1, 'yy') and trunc(sysdate, 'mm')-1
group by t1.poi_item_name, t1.pka_region_id, t1.pka_people_coll_id
order by 2, 3) t
group by pka_region_id, uszn.pkTSrv.GetRegionName(pka_region_id), poi_item_name
union
select 104,
        'ЯНАО',
        poi_item_name,
        count(pka_people_coll_id),
        sum(pc_count_applied_to)
from
(select distinct
  case t1.poi_item_name
   when 'Государственная социальная помощь на одиноко проживающего гражданина' then 'Ежемесячная адресная социальная помощь на одиноко проживающего гражданина'
   when 'Государственная социальная помощь на учащегося ПТУ, ВУЗа' then 'Ежемесячная адресная социальная помощь на учащегося ПТУ, ВУЗа'
   when 'Государственная социальная помощь на члена семьи' then 'Ежемесячная адресная социальная помощь на члена семьи'
   else t1.poi_item_name end as poi_item_name
   ,
  t1.pka_region_id,
  t1.pka_people_coll_id,
  max(t1.pc_count_applied_to) as pc_count_applied_to
from uszn.all_po_amounts t1
where (t1.pka_kind_region_id, t1.pka_kind_id) in ((104, 279), (104, 83), (104, 84))
      -- and t1.payout_doc_doc_date between trunc(sysdate, 'yy') and trunc(sysdate, 'mm')-1
      and t1.payout_doc_doc_date between trunc(trunc(sysdate, 'mm')-1, 'yy') and trunc(sysdate, 'mm')-1
group by t1.poi_item_name, t1.pka_region_id, t1.pka_people_coll_id
order by 2, 3) t
group by poi_item_name)