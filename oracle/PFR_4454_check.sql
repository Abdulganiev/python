select
    c.decision_date, -- Дата решения о назначении ЕП
    c.app_snils, -- СНИЛС получателя ЕП
    c.app_F, -- Фамилия получателя ЕП
    c.app_I, -- Имя получателя ЕП
    c.app_O, -- Отчество получателя ЕП
    c.app_DR,-- Дата рождения получателя ЕП
    c.baby_snils, -- СНИЛС (лица - основания) ЕП
    c.baby_F, -- Фамилия (лица - основания) ЕП
    c.baby_I, -- Имя (лица - основания) ЕП
    c.baby_O, -- Отчество (лица - основания) ЕП
    c.baby_DR, -- Дата рождения (лица - основания) ЕП
    c.date_from, -- Период, на который установлено ЕП С
    c.date_to, -- Период, на который установлена ЕП По
    c.amount, -- Размер назначения ЕП
    c.pka_kind_name, -- вид выплаты в УСЗН
    '0'||c.region_id||' - '||uszn.pkTSrv.GetRegionName(c.region_id)||' - сверка с ПФР детские пособия'

from (
select distinct pk.region_id as region_id, pk.pka_people_coll_id as id, pka_kind_name, pka_people_coll_desc, baby, snils,
       pfr.app_date, pfr.app_snils, pfr.app_F, pfr.app_I, pfr.app_O, pfr.app_DR,
       pfr.baby_snils, pfr.baby_F, pfr.baby_I, pfr.baby_O, pfr.baby_DR,
       pfr.decision_date, pfr.decision, pfr.decision_status,pfr.date_from, pfr.date_to, pfr.amount,pfr.date_upload
from (select pk.*, uszn.pkPerson.GetPersonalReq(pk.region_id, pk.pka_people_coll_id, 25) as snils
        from uszn.all_asg_periods pk
        where (pk.pka_kind_id, pk.pka_kind_region_id) in ((67,104),(211,104)) -- and trunc(sysdate, 'mm') between pk.date_start and pk.date_end
              and pk.pka_status_num in (0,1)) pk
     inner join
     (select t.*, baby_F||' '||baby_I||' '||baby_O||' '||baby_dr as baby from uszn.temp$_pfr_check t) pfr
   on pfr.baby_SNILS=pk.SNILS and pfr.date_from < pk.date_end

union

select distinct pk.region_id as region_id, pk.pka_people_coll_id as id, pka_kind_name, pka_people_coll_desc, baby, snils,
       pfr.app_date, pfr.app_snils, pfr.app_F, pfr.app_I, pfr.app_O, pfr.app_DR,
       pfr.baby_snils, pfr.baby_F, pfr.baby_I, pfr.baby_O, pfr.baby_DR,
       pfr.decision_date, pfr.decision, pfr.decision_status,pfr.date_from, pfr.date_to, pfr.amount,pfr.date_upload
from (select pk.*, uszn.pkPerson.GetPersonalReq(pk.region_id, pk.pka_people_coll_id, 25) as snils,
       replace(
       upper(uszn.pkPerson.GetPersonalReq(pk.region_id, pk.pka_people_coll_id, 0)||
             uszn.pkPerson.GetPersonalReq(pk.region_id, pk.pka_people_coll_id, 1)||
             uszn.pkPerson.GetPersonalReq(pk.region_id, pk.pka_people_coll_id, 2)||
             uszn.pkPerson.GetPersonalReq(pk.region_id, pk.pka_people_coll_id, 3))
             , 'Ё', 'Е') as desc_baby
        from uszn.all_asg_periods pk
        where (pk.pka_kind_id, pk.pka_kind_region_id) in ((67,104),(211,104)) -- and trunc(sysdate, 'mm') between pk.date_start and pk.date_end
              and pk.pka_status_num in (0,1)) pk
     inner join
     (select t.*, replace(upper(baby_F||baby_I||baby_O||baby_dr), 'Ё', 'Е') as desc_baby,
             baby_F||' '||baby_I||' '||baby_O||' '||baby_dr as baby
             from uszn.temp$_pfr_check t) pfr
   on pfr.desc_baby=pk.desc_baby and pfr.date_from < pk.date_end) c