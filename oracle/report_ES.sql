create table uszn.temp$_r_ecert as

select
       t1.region_id,
	     uszn.pkTSrv.GetRegionName(t1.region_id) as MO,
       NVL(uszn.pkPCAddr.GetPCAddress(t1.region_id, t1.person_id, 1, null, t1.date_start, 0), uszn.pkTSrv.GetRegionName(t1.region_id)) as np,
       uszn.pkPerson.GetPersonalReq(t1.region_id, t1.person_id, 25) as people_guid,
       uszn.pkPerson.GetPersonalReq(t1.region_id, uszn.pkPerson.GetDocInstancePC(t1.app_pdoc_id, t1.region_id), 25) as baby_guid,
       Floor(Months_Between(sysdate, uszn.pkPerson.GetBirthDate(t1.region_id, t1.person_id))/12) as age,
       uszn.pkPerson.GetSex(t1.region_id, t1.person_id) as gender,
       uszn.pkCat.HasCategory(t1.person_id, t1.region_id, 325,   0, t1.date_start) as invalid,
       uszn.pkCat.HasCategory(t1.person_id, t1.region_id,  18, 104, t1.date_start) as maloim,
       uszn.pkCat.HasCategory(t1.person_id, t1.region_id, 1058,  0, t1.date_start) as mnogo,
       case
         when uszn.pkPIC.GetCollByRole(t1.region_id, t1.person_id, 9, sysdate) is not null then 'father'
         when uszn.pkPIC.GetCollByRole(t1.region_id, t1.person_id, 8, sysdate) is not null then 'mother'
        end as role_class_name,
       t1.cert_number, 
	     t1.cert_kind_name,
	     t5.rai_pkaf_name as recipient_category,
	   
	     t1.total_amount,
       t1.current_amount,
       t1.date_start,
       t1.date_end,
       t1.status_name,
       t1.status_reason_name,
       t1.block_reason_name,
       t3.id as transact_id,
       t3.op_type_name,
       t3.seller_full_name,
       t3.address_address as seller_address,
       t3.op_date_time,
       t3.amount as transact_amount,
       t3.full_amount as transact_full_amount,
       t4.transact_id as transact_id_shop,
       t4.code, t4.name,
       t4.amount as amount,
       t4.full_amount as full_amount,
       t4.qty
       
from uszn.all_fk_ecerts t1
     inner join uszn.v_asg_amounts t5
       on t1.region_id=t5.region_id and t1.asg_amount_id=t5.id
     left join uszn.r_fk_ecert_to_transacts t2
       on t1.region_id=t2.region_id and t1.id=t2.ecert_id
     left join uszn.all_fk_ecert_transactions t3
       on t2.transact_id=t3.id
     left join uszn.all_fk_ecert_transact_goods t4
       on t2.transact_id=t4.transact_id and t2.region_id=t4.region_id and t2.ecert_id=t4.ecert_id