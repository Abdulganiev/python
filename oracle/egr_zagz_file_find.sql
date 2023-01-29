select distinct
    t3.last_name,
    t3.first_name,
    NVL(t3.middle_name, ' ') as middle_name,
    uszn.DateToCharISO(t3.birth_date),
    t3.death_date_egisso,
    t3.az_date,
    t3.az_num,
    t3.zagz_status,
    uszn.pkXML.Escape(t3.zagz) as zagz,
    t3.sv_ser,
    t3.sv_num,
    t3.sv_date,
    NVL(uszn.pkXML.Escape(t3.death_place), ' ') as death_place
from
 uszn.v_people_and_colls t1
 inner join
 uszn.temp$_death t3
on Translate(UPPER(t1.last_name), 'Ё', 'Е')   = Translate(UPPER(t3.last_name), 'Ё', 'Е')   and
   Translate(UPPER(t1.first_name), 'Ё', 'Е')  = Translate(UPPER(t3.first_name), 'Ё', 'Е')  and
   --Translate(UPPER(t1.middle_name), 'Ё', 'Е') = Translate(UPPER(t3.middle_name), 'Ё', 'Е') and
   t1.birth_date = uszn.ToDateDef(t3.birth_date) and
   t1.death_date is null and
   t3.last_name is not null and
   t3.first_name is not null and
   t3.birth_date is not null and
   t3.death_date_egisso is not null and
   t3.az_date is not null and
   t3.az_num is not null and
   t3.sv_ser is not null and
   t3.sv_num is not null and
   t3.sv_date is not null and
   (replace(t3.dul_nom, ' ', '') = replace(uszn.pkPerson.GetPersonalReq(t1.region_id, t1.id, 19)||uszn.pkPerson.GetPersonalReq(t1.region_id, t1.id, 20), ' ', '')
    or
    replace(t3.snils, ' ', '') = uszn.pkPerson.GetPersonalReq(t1.region_id, t1.id, 26))

   -- and t3.date_information > (sysdate - 30)
   -- and t1.region_id=65