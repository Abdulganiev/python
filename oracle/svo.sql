create table uszn.temp$_svo
as
select
                           region_id, coll_id, doc_id,
                           (select uszn.StrCommaConcat(d.decoded_value) from uszn.all_personal_doc_reqs d
                               where d.class_id=20781 and d.region_id=c.region_id and d.pdoc_id=c.doc_id) as fam_charact,
                           (select uszn.StrCommaConcat(d.decoded_value) from uszn.all_personal_doc_reqs d
                               where d.class_id=20783 and d.region_id=c.region_id and d.pdoc_id=c.doc_id) as fam_cat,
                           (select uszn.StrCommaConcat(d.decoded_value) from uszn.all_personal_doc_reqs d
                               where d.class_id=20792 and d.region_id=c.region_id and d.pdoc_id=c.doc_id) as fam_fio,
                           (select count(d.decoded_value) from uszn.all_personal_doc_reqs d
                               where d.class_id=20792 and d.region_id=c.region_id and d.pdoc_id=c.doc_id) as fam_fio_cnt,
                           (select count(d.decoded_value) from uszn.all_personal_doc_reqs d
                               where d.class_id=20793 and d.region_id=c.region_id and d.pdoc_id=c.doc_id) as fam_fio_cnt_education,
                           (select count(d.decoded_value) from uszn.all_personal_doc_reqs d
                               where d.class_id=20795 and d.region_id=c.region_id and d.pdoc_id=c.doc_id) as fam_fio_cnt_power,
                           (select count(d.decoded_value) from uszn.all_personal_doc_reqs d
                               where d.class_id=20796 and d.region_id=c.region_id and d.pdoc_id=c.doc_id) as fam_fio_cnt_post,
                           (select count(d.decoded_value) from uszn.all_personal_doc_reqs d
                               where d.class_id=20802 and d.region_id=c.region_id and d.pdoc_id=c.doc_id) as fam_children_cnt,
                           (select count(d.decoded_value) from uszn.all_personal_doc_reqs d
                               where d.class_id=20803 and d.region_id=c.region_id and d.pdoc_id=c.doc_id) as fam_children_type,
                           (select count(d.decoded_value) from uszn.all_personal_doc_reqs d
                               where d.class_id=20803 and d.region_id=c.region_id and d.pdoc_id=c.doc_id) as fam_children_name,
                           uszn.pkPerson.GetDocReqValue(c.region_id, 20826, c.doc_id) as housing_type,
                           uszn.pkPerson.GetDocReqValue(c.region_id, 20827, c.doc_id) as housing_area,
                           uszn.pkPerson.GetDocReqValue(c.region_id, 20828, c.doc_id) as housing_cnt_room,
                           uszn.pkPerson.GetDocReqValue(c.region_id, 20829, c.doc_id) as housing_well_being,
                           uszn.pkPerson.GetDocReqValue(c.region_id, 20830, c.doc_id) as housing_condition,
                           uszn.pkPerson.GetDocReqValue(c.region_id, 20842, c.doc_id) as conclusion,
                           uszn.pkPerson.GetDocReqValue(c.region_id, 20843, c.doc_id) as special_marks,
                           snils, cat, cat1, cat2, cat3, From_To,
                           case when upper(member_r) like upper('%Супруг%') then id else null end as fam,

                           case when upper(member_r) like upper('%Супруг%') and id = passport_id then passport_id else null end as passport_fam,

                           case when upper(member_coll) like upper('%Супруг%') and upper(member_r) not like upper('%Супруг%') and
                                     (upper(member_coll) like upper('%Дочь%')      or upper(member_coll) like upper('%Сын%') and
									  upper(member_coll) like upper('%Падчерица%') or upper(member_coll) like upper('%Пасынок%')) and age < 18 then member_id else null end as fam_ch_nes,

                           case when upper(member_coll) like upper('%Супруг%') and upper(member_r) not like upper('%Супруг%') and
                                     (upper(member_coll) like upper('%Дочь%')      or upper(member_coll) like upper('%Сын%') and
									  upper(member_coll) like upper('%Падчерица%') or upper(member_coll) like upper('%Пасынок%')) and age < 23 then member_id else null end as fam_ch,

                           case when upper(member_coll) like upper('%Отец%') or upper(member_coll) like upper('%Мать%')  then id else null end as fam_parents,

                           case when upper(member_coll) like upper('%Отец%') or upper(member_coll) like upper('%Мать%')
                                     and id = passport_id then passport_id else null end as passport_fam_parents,

                           case when upper(member_coll) like upper('%Отец%') or upper(member_coll) like upper('%Мать%')  then member_id else null end as parents,

                           case when upper(member_coll) not like upper('%Мать%') and upper(member_coll) not like upper('%Отец%') and
                                     upper(member_coll) not like upper('%Супруг%') then id else null end as fam_old,

                           case when upper(member_coll) not like upper('%Мать%') and upper(member_coll) not like upper('%Отец%') and
                                     upper(member_coll) not like upper('%Супруг%') and id = passport_id then passport_id else null end as passport_fam_old,


                           case when upper(member_coll) not like upper('%Мать%') and upper(member_coll) not like upper('%Отец%') and
                                     upper(member_coll) not like upper('%Супруг%') and 
									 (upper(member_coll) like upper('%Дочь%') or upper(member_coll) like upper('%Сын%')) and age < 23 then member_id else null end as fam_ch_old,

                           case when upper(member_coll) not like upper('%Мать%') and upper(member_coll) not like upper('%Отец%') and
                                     upper(member_coll) not like upper('%Супруг%') and 
									 (upper(member_coll) like upper('%Дочь%') or upper(member_coll) like upper('%Сын%')) and age < 18 then member_id else null end as fam_ch_old_nes,
                           age,
						   case when age is null then coll_id else null end as loner,
                           member_r, 
						   member_coll
                        from
                          (select distinct t1.region_id, t1.coll_id, t3.doc_id, t1.region_id||'-'||t1.coll_id as id, t1.people_id, t1.snils,
                                  t1.cat, t1.cat1, t1.cat2, t1.cat3, t1.From_To,
                                  t2.age,
                                  case when t2.people_id is null then null else t1.region_id||'-'||t2.people_id end as member_id,
                                  case when t3.coll_id is null then null else t3.region_id||'-'||t3.coll_id end as passport_id,
                                  (select a.relation_name from uszn.v_pd_coll_role_relations a 
								    where a.region_id=t1.region_id and a.whom_id=t1.people_id and a.people_coll_id=t1.coll_id
                                          and a.who_id=t2.people_id) as member_r,
                                  (select uszn.StrCommaConcat(a.relation_name) from uszn.v_pd_coll_role_relations a 
								    where a.region_id=t1.region_id and a.whom_id=t1.people_id and a.people_coll_id=t1.coll_id) as member_coll
                           from
                              (select region_id, coll_id, people_id, snils, max(cat1) as cat1, max(cat2) as cat2, max(cat3) as cat3, max(From_To) as From_To, max(cat) as cat
                                from
                                (select a3.region_id, a3.coll_id, a3.people_id, a1.snils,
                                        uszn.pkCat.HasCategory(a1.id, a1.region_id, 282, 0, to_date('01.02.2022'), sysdate) as cat1,
                                        uszn.pkCat.HasCategory(a1.id, a1.region_id, 283, 0, to_date('01.02.2022'), sysdate) as cat2,
                                        uszn.pkCat.HasCategory(a1.id, a1.region_id, 284, 0, to_date('01.02.2022'), sysdate) as cat3,
                                        uszn.pkPerson.GetDocReqValueDate(a1.region_id, 20069, uszn.pkPerson.GetLastDocInstanceID(a1.region_id, a1.id, 20060)) as From_To,
										uszn.pkPerson.GetLastDocInstanceID(a1.region_id, a1.id, 20060) as doc_id,
                                        /*case uszn.pkPerson.GetPCReqValueInt(a1.region_id, a1.id, 20066)
                                          when 104000196 then 'Доброволец'
                                          when 104000197 then 'Участник отряда БАРС'
                                          when 104000198 then 'Мобилизованный'
                                          when 104000199 then 'Сотрудник силовых ведомств'
                                          else 'Контракт МВД ДНР'
                                        end*/ a2.pkaf_name as cat
                                  from  uszn.v_people_and_colls a1
                                        inner join
                                        uszn.all_po_amounts a2
                                    on  a1.region_id=a2.pka_region_id and a1.id=a2.pka_people_coll_id and --a1.region_id=59 and
                                        (a2.pka_kind_id, a2.pka_kind_region_id) in ((311,104)) and a2.status_id in (103,107,104,101,102)
                                        --and a1.snils_formatted is not null
                                        inner join
                                        uszn.v_coll_membership_periods a3
                                    on  a1.region_id=a3.region_id and a1.id=a3.people_id and a3.role_class_id=110
                                        inner join
                                        uszn.all_asg_amounts a4
                                    on  a1.region_id=a4.region_id and a2.pka_people_coll_id=a4.pka_people_coll_id
                                        and a2.pka_kind_id=a4.pka_kind_id and a2.pka_kind_region_id=a4.pka_kind_region_id and a4.amount>0 )
                                group by region_id, coll_id, people_id, snils) t1
                           left join
                           (select distinct region_id, coll_id, people_id, Floor(Months_Between(sysdate, uszn.pkPerson.GetBirthDate(region_id, people_id))/12) as age
						                 from uszn.v_coll_membership_periods
                             where role_class_id=111 and sysdate between date_start and date_end) t2
                           on t1.region_id=t2.region_id and t1.coll_id=t2.coll_id
                           left join
                           (select region_id, pc_id as coll_id, max(id) as doc_id  from uszn.all_personal_docs
                             where class_id=20775 group by region_id, pc_id) t3
                            on t1.region_id=t3.region_id and t1.coll_id=t3.coll_id) c