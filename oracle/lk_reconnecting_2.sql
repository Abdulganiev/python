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
  end;