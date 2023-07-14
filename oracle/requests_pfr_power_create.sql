CREATE TABLE uszn.temp$_pfr_power
as
select row_number() over(ORDER BY id) as num,
       region_id, id, snils, date_start, date_end
from (
     select region_id, pka_people_coll_id as id, uszn.pkPerson.GetPersonalReq(region_id, pka_people_coll_id, 25) as snils,
            min(rap_date_start) as date_start,
            max(rap_date_end) as date_end
           from uszn.all_asg_amounts
           where region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
                 --region_id in 59
                 and (pka_kind_id, pka_kind_region_id) in ((29,104),(9,104),(2,104),(148,0))
                 and trunc(current_date, 'mm') between rap_date_start and rap_date_end
                 and (rai_pkaf_id, rai_pkaf_region_id) in ((806,104),(  59,104),(807,104),( 165,104),(808,104),( 809,104),(416,104),(52,104),
                                                           ( 77,104),(1007,104),(  3,104),(1008,104),(805,104),(1009,104),(2,104))
                 and amount>0 and pka_is_enabled=1 and pka_status_num=0
                 and uszn.pkPerson.GetDeathDate(region_id, pka_people_coll_id) is null
                 and uszn.pkPerson.GetCloseDate(region_id, pka_people_coll_id) is null
     group by region_id, pka_people_coll_id)
