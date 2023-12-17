select
        region_id,
        '0'||region_id||' - '||uszn.pkTSrv.GetRegionName(region_id)||' - Удостоверение многодетные неправильная организация - '||count(distinct coll_id) over(partition BY region_id) as name,
    	'0'||region_id||' - '||uszn.pkTSrv.GetRegionName(region_id) as MO,
        region_id||'-'||coll_id,
        uszn.pkPerson.DescribeManColl(region_id, coll_id, 0) as coll_desc,
        org

from
(select distinct region_id, coll_id, org
  from uszn.temp$_reestr_large_family
   where org is not null
         and org not in ('58','59','60','61','62','63','64','65','66','67','68','69','70')
         and date_to > to_date('01.01.2022'))