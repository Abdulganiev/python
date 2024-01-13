select
 '0'||region_id||' - '||uszn.pkTSrv.GetRegionName(region_id)||' - молочка от здрав' as name,
 HOSPITAL,
 SNILS, last_name||' '||first_name||' '||middle_name||' '||birth_date as pc_desc,
 DUL_TYPE||' сер. '||DUL_SER||' № '||DUL_NOM||' место рожд. '||DUL_PLACE||' выдан '||DUL_KEM||' дата выдачи '||DUL_DATE||' код подразд. '||DUL_CODE as DUL,
 BABY_SNILS, BABY_last_name||' '||BABY_first_name||' '||BABY_middle_name||' '||BABY_birth_date as BABY_pc_desc,
 case when BABY_last_name is null then null
      else BABY_DUL_TYPE||' сер. '||BABY_DUL_SER||' № '||BABY_DUL_NOM||' место рожд. '||BABY_DUL_PLACE||' выдан '||BABY_DUL_KEM||' дата выдачи '||BABY_DUL_DATE end as BABY_DUL,
 ADR_MO||' '||ADR_FULL as adr,
 CONTACT, CAT, DATE_START, DATE_END
from uszn.temp$_zdrav_milk_new