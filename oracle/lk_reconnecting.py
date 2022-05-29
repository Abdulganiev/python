from generating_report_files import *

#***************************************************************

def lk_reconnecting():
    curs.execute('''
declare
  iiIDs uszn.pkGen.TIntegers;
  i$ Pls_Integer;
begin
    select esia_id bulk collect into iiIDs
from
(select esia_id, snils
  from uszn.all_lk_account_pc_links
  group by esia_id, snils
  having count(region_id)=1) t1
  inner join uszn.v_people_and_colls t2
on t1.snils = t2.snils
  inner join uszn.v_people_and_colls t3
on t2.pc_desc = t3.pc_desc and t2.snils=t3.snils
group by esia_id, t2.pc_desc, t3.pc_desc
having count(t2.region_id)>1;
  for i in 1..iiIDs.count loop
    begin
      uszn.pkLk.AccLinkPersons(iiIDs(i));
    end;
  end loop;
end;''')

    curs.execute('''
  declare
    iiIDs uszn.pkGen.TIntegers;
    i$ Pls_Integer;
  begin
      select t1.esia_id bulk collect into iiIDs
  from uszn.all_lk_accounts t1
       left join
       uszn.all_lk_account_pc_links t2
    on
       t1.esia_id=t2.esia_id
    where t2.esia_id is null;
    for i in 1..iiIDs.count loop
      begin
        uszn.pkLk.AccLinkPersons(iiIDs(i));
      end;
    end loop;
  end;''')

#***************************************************************

curs = connect_oracle()

lk_reconnecting()

writing_to_log_file('lk_reconnecting', 'скрипт отработан')
