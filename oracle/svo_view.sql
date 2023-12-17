create or replace view uszn.temp$_v_svo
as
SELECT
  v1.REGION_ID,
  v1.COLL_ID,
  v1.DOC_ID,
  v1.FAM_CHARACT,
  v1.FAM_CAT,
  v1.FAM_FIO_CNT,
  v1.FAM_FIO_CNT_EDUCATION,
  v1.FAM_FIO_CNT_POWER,
  v1.FAM_FIO_CNT_POST,
  v1.FAM_CHILDREN_CNT,
  v1.FAM_CHILDREN_TYPE,
  v1.FAM_CHILDREN_NAME,
  v1.HOUSING_TYPE,
  v1.HOUSING_AREA,
  v1.HOUSING_CNT_ROOM,
  v1.HOUSING_WELL_BEING,
  v1.HOUSING_CONDITION,
  v1.CONCLUSION,
  v1.SPECIAL_MARKS,
  v1.SNILS,
  Floor(Months_Between(sysdate, v2.birth_date)/12) as age_usvo,
  v1.cat,
  count(distinct v1.FAM) as FAM,
  count(distinct v1.PASSPORT_FAM) as PASSPORT_FAM,
  COUNT(distinct v1.FAM_CH_NES) as FAM_CH_NES,
  COUNT(distinct v1.FAM_CH) as FAM_CH_23,
  COUNT(distinct v1.FAM_CH)+count(distinct FAM) as FAM_CH,
  COUNT(distinct (case when v1.age < 7               then FAM_CH else null end)) as nl_to7,
  COUNT(distinct (case when v1.age between  7 and 17 then FAM_CH else null end)) as nl_to7_18,
  COUNT(distinct (case when v1.age between  3 and 17 then FAM_CH else null end)) as nl_to3_18,
  COUNT(distinct (case when v1.age between  2 and 17 then FAM_CH else null end)) as nl_to2_18,
  COUNT(distinct (case when v1.age between 18 and 22 then FAM_CH else null end)) as st,
  COUNT(distinct v1.FAM_PARENTS) as FAM_PARENTS,
  COUNT(distinct v1.PASSPORT_FAM_PARENTS) as PASSPORT_FAM_PARENTS,
  COUNT(distinct v1.PARENTS) as PARENTS,
  count(distinct v1.FAM_OLD) as FAM_OLD,
  count(distinct v1.PASSPORT_FAM_OLD) as PASSPORT_FAM_OLD,
  COUNT(distinct v1.FAM_CH_OLD) as FAM_CH_OLD,
  COUNT(distinct v1.FAM_CH_OLD_NES) as FAM_CH_NES_OLD,
  COUNT(distinct v1.FAM_CH_OLD_NES_23) as FAM_CH_NES_OLD_23,
  COUNT(distinct (case when v1.age < 7               then v1.FAM_CH_OLD else null end)) as nl_to7_old,
  COUNT(distinct (case when v1.age between  7 and 17 then v1.FAM_CH_OLD else null end)) as nl_to7_18_old,
  COUNT(distinct (case when v1.age between  3 and 17 then v1.FAM_CH_OLD else null end)) as nl_to3_18_old,
  COUNT(distinct (case when v1.age between  2 and 17 then v1.FAM_CH_OLD else null end)) as nl_to2_18_old,
  COUNT(distinct (case when v1.age between 18 and 22 then v1.FAM_CH_OLD else null end)) as st_old,
  count(v1.loner) as loner
FROM uszn.temp$_svo v1 join uszn.v_people_and_colls v2
     on v1.snils=v2.snils
GROUP BY
    v1.REGION_ID,
    v1.COLL_ID,
    v1.DOC_ID,
    v1.FAM_CHARACT,
    v1.FAM_CAT,
    v1.FAM_FIO_CNT,
    v1.FAM_FIO_CNT_EDUCATION,
    v1.FAM_FIO_CNT_POWER,
    v1.FAM_FIO_CNT_POST,
    v1.FAM_CHILDREN_CNT,
    v1.FAM_CHILDREN_TYPE,
    v1.FAM_CHILDREN_NAME,
    v1.HOUSING_TYPE,
    v1.HOUSING_AREA,
    v1.HOUSING_CNT_ROOM,
    v1.HOUSING_WELL_BEING,
    v1.HOUSING_CONDITION,
    v1.CONCLUSION,
    v1.SPECIAL_MARKS,
    v1.SNILS,
    v1.cat,
    v2.birth_date