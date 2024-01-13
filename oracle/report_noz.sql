-- нозология
CREATE TABLE uszn.temp$_r_inv_noz as

select z.mo as region_id,
       uszn.pkTSrv.GetRegionName(z.mo) as mo,
       uszn.pkXMLUtils.GuidToStr(uszn.pkJUtil.GenerateGUIDv1(z.mo)) as people_guid,
       z.snils,
	   z.id,
	   z.fio,
	   z.noz, 
	   z.obsl_kv, 
	   z.prisp_kv, 
	   z.predst_kv, 
	   z.obsl_mkd, 
	   z.prisp_mkd,
	   z.comments
      from
(
select 58 as MO, t.* from uszn.temp$_inv_noz_058 t
union all
select 59 as MO, t.* from uszn.temp$_inv_noz_059 t
union all
select 60 as MO, t.* from uszn.temp$_inv_noz_060 t
union all
select 61 as MO, t.* from uszn.temp$_inv_noz_061 t
union all
select 62 as MO, t.* from uszn.temp$_inv_noz_062 t
union all
select 63 as MO, t.* from uszn.temp$_inv_noz_063 t
union all
select 64 as MO, t.* from uszn.temp$_inv_noz_064 t
union all
select 65 as MO, t.* from uszn.temp$_inv_noz_065 t
union all
select 66 as MO, t.* from uszn.temp$_inv_noz_066 t
union all
select 67 as MO, t.* from uszn.temp$_inv_noz_067 t
union all
select 68 as MO, t.* from uszn.temp$_inv_noz_068 t
union all
select 69 as MO, t.* from uszn.temp$_inv_noz_069 t
union all
select 70 as MO, t.* from uszn.temp$_inv_noz_070 t
) z