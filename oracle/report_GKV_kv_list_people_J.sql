select
 -- тип записи
'Ж'||
 -- категория
To_Char(Nvl(uszn.pkOutDocCol.GetPFRF_Cat(r.region_id, r.people_id, r.pkaf_region_id, r.pkaf_id, r.date_from, r.date_to), 0), 'fm000')||
 -- наименование документа
RPad(Nvl(uszn.pkOutDocCol.GetPFRF_DPK_Req(r.region_id, r.people_id, r.exp_kind_region_id, r.exp_kind_id, r.pkaf_region_id, r.pkaf_id, 1, r.date_from, r.date_to), ' '), 80)||
 -- серия документа
RPad(Nvl(uszn.pkOutDocCol.GetPFRF_DPK_Req(r.region_id, r.people_id, r.exp_kind_region_id, r.exp_kind_id, r.pkaf_region_id, r.pkaf_id, 2, r.date_from, r.date_to), ' '), 8)||
 -- номер документа
RPad(Nvl(To_Char(uszn.ToIntDef(uszn.pkOutDocCol.GetPFRF_DPK_Req(r.region_id, r.people_id, r.exp_kind_region_id, r.exp_kind_id, r.pkaf_region_id, r.pkaf_id, 3, r.date_from, r.date_to))), ' '), 8)||
 -- дата выдачи документа
RPad(Nvl(To_Char(uszn.ToDateDef(uszn.pkOutDocCol.GetPFRF_DPK_Req(r.region_id, r.people_id, r.exp_kind_region_id, r.exp_kind_id, r.pkaf_region_id, r.pkaf_id, 4, r.date_from, r.date_to)), 'yyyy/mm/dd'), ' '), 10)||
 -- наименование органа, выдавшего документ
RPad(Nvl(uszn.pkOutDocCol.GetPFRF_DPK_Req(r.region_id, r.people_id, r.exp_kind_region_id, r.exp_kind_id, r.pkaf_region_id, r.pkaf_id, 5, r.date_from, r.date_to), ' '), 80)||
 -- дата приобретения гражданином права на отнесение к соответствующей категории
RPad(Nvl(To_Char(uszn.ToDateDef(uszn.pkOutDocCol.GetPFRF_DPK_Req(r.region_id, r.people_id, r.exp_kind_region_id, r.exp_kind_id, r.pkaf_region_id, r.pkaf_id, 6, r.date_from, r.date_to)), 'yyyy/mm/dd'), ' '), 10)||
 -- дата утраты гражданином права на получение мер социальной поддержки по оплате жилищно-коммунальных услуг
RPad(Nvl(To_Char(uszn.ToDateDef(uszn.pkOutDocCol.GetPFRF_DPK_Req(r.region_id, r.people_id, r.exp_kind_region_id, r.exp_kind_id, r.pkaf_region_id, r.pkaf_id, 7, r.date_from, r.date_to)), 'yyyy/mm/dd'), ' '), 10)
as record_J

from (
  with
    -- признаки учёта, имеющиеся в справочнике соответствия данных для обмена
    mapped_pkafs as (
      select
          int_region_id as pkaf_region_id,
          int_id as pkaf_id,
          uszn.ToIntDef(ext_code) as cat_code
        from uszn.dic_data_exchange_mappings
        where
          -- вид соответствия: PrivRegCats_PKAF
          kind_id=70 and
          -- фильтр района внешнего ключа по району
          ext_region_id in (select parent_id from uszn.tsrv_flat_regions where child_id={region_id}) and
          -- исключаем:
          -- (040) «Участник ВОВ не в составе действующей армии (пп. з, п. 1, ст. 2, 5-ФЗ)»
          -- (050) «Лицо, награждённое знаком «Жителю блокадного Ленинграда»
          uszn.ToIntDef(ext_code) not in (40, 50) and
          ( -- федеральный регистр
            (uszn.ToIntDef(ext_code) between 10 and 150) or
            -- члены семей умерших от радиации
            (uszn.ToIntDef(ext_code) between 340 and 351)
          ))
  select
      pa.region_id,
      pa.pka_people_coll_id as people_id,
      pa.pkaf_region_id,
      pa.pkaf_id,
      TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q') as date_from,
      ADD_MONTHS(TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q'), 3)-1 as date_to,
      104 as exp_kind_region_id,
      1 as exp_kind_id
    from uszn.all_po_amounts_ex pa
    where
      -- фильтр по району
      pa.region_id={region_id} and
      -- виды выплат, заданные в параметрах выходного документа
      (pa.pka_kind_region_id, pa.pka_kind_id) in ((104,29),(104,29)) and
      -- источник финансирования - федеральный бюджет
      pa.finsrc_region_id=0 and pa.finsrc_id=1 and
      -- оплачено
      pa.st_kind_id=2 and
      -- за период выборки
      pa.poi_payout_date between TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q') and ADD_MONTHS(TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q'), 3)-1 and
      ( -- фильтр по признакам учёта
        ( -- признак учёта присутствует в параметрах перекодировки признаков учёта для заданного в параметрах выходного документа вида перекодиовки
          (pa.pkaf_region_id, pa.pkaf_id) in
            (select pkaf_region_id, pkaf_id
              from uszn.dic_exp_pkaf_params
              where (exp_kind_region_id, exp_kind_id) in ((104,1)))
        ) or
        ( -- признак учёта "Наличие документа «Сведения о получении льгот на ЖКУ на декабрь 2008 года»"
          (pa.pkaf_region_id, pa.pkaf_id) in ((104, 339)) and
          -- наличие соответствия в справочнике соответствия данных для обмена
          -- для льготного основания, указанного  в сведениях о получении льгот
          Exists(
            select 1
              from uszn.r_personal_doc_instances d, mapped_pkafs m
              where
                d.region_id=pa.region_id and d.people_coll_id=pa.pka_people_coll_id and
                -- реквизит "Правовое основание"
                d.class_id=7116 and
                -- slurp-ключ признака учёта ищем в персональном документе "Сведения о получении льгот..."
                m.pkaf_region_id*1000000+m.pkaf_id=uszn.ToIntDef(d.value)
          )
        ) or
        -- остальные признаки учёта, при наличии соответствия в справочнике
        (pa.pkaf_region_id, pa.pkaf_id) in (select pkaf_region_id, pkaf_id from mapped_pkafs)
      ) /* фильтр по признакам учёта */
    group by
      pa.region_id, pa.pka_people_coll_id,
      pa.pkaf_region_id, pa.pkaf_id
) r
where r.region_id={region_id}
      and r.people_id={people_id}
