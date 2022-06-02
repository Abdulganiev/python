select *

from (
  with
    -- �������� �����, ��������� � ����������� ������������ ������ ��� ������
    mapped_pkafs as (
      select
          int_region_id as pkaf_region_id,
          int_id as pkaf_id,
          uszn.ToIntDef(ext_code) as cat_code
        from uszn.dic_data_exchange_mappings
        where
          -- ��� ������������: PrivRegCats_PKAF
          kind_id=70 and
          -- ������ ������ �������� ����� �� ������
          ext_region_id in (select parent_id from uszn.tsrv_flat_regions where child_id=59) and
          -- ���������:
          -- (040) ��������� ��� �� � ������� ����������� ����� (��. �, �. 1, ��. 2, 5-��)�
          -- (050) �����, ����������� ������ ������� ���������� ����������
          uszn.ToIntDef(ext_code) not in (40, 50) and
          ( -- ����������� �������
            (uszn.ToIntDef(ext_code) between 10 and 150) or
            -- ����� ����� ������� �� ��������
            (uszn.ToIntDef(ext_code) between 340 and 351)
          ))
  select
      pa.region_id,
      pa.pka_people_coll_id as people_id,
      -- �������� ������: ���������� �������, �� ������� ���������������� ������
      Nvl(
        Ceil(Max(
          case
            when
              (pa.poi_item_region_id=0 and pa.poi_item_id in (2, 3, 4, 12, 13)) or
              (pa.poi_item_region_id=104 and pa.poi_item_id=72)
            then pa.pc_count_applied_to
          end)),
        0) as pc_house,
      -- ������������ ������: ���������� �������, �� ������� ���������������� ������
      Nvl(
        Ceil(Max(
          case
            when
              (pa.poi_item_region_id=0 and pa.poi_item_id not in (2, 3, 4, 12, 13)) or
              (pa.poi_item_region_id=104 and pa.poi_item_id in (73, 194))
            then pa.pc_count_applied_to
          end)),
        0) as pc_srv,
      -- ���������� �������� ���������
      Count(distinct uszn.pkGen.EncodeIDRgnID(pa.pkaf_id, pa.pkaf_region_id)) as basis_cnt
    from uszn.all_po_amounts_ex pa
    where
      -- ������ �� ������
      pa.region_id=59 and
      -- ���� ������, �������� � ���������� ��������� ���������
      (pa.pka_kind_region_id, pa.pka_kind_id) in ((104,29),(104,29)) and
      -- �������� �������������� - ����������� ������
      pa.finsrc_region_id=0 and pa.finsrc_id=1 and
      -- ��������
      pa.st_kind_id=2 and
      -- �� ������ �������
      pa.poi_payout_date between TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q') and ADD_MONTHS(TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q'), 3)-1 and
      ( -- ������ �� ��������� �����
        ( -- ������� ����� ������������ � ���������� ������������� ��������� ����� ��� ��������� � ���������� ��������� ��������� ���� ������������
          (pa.pkaf_region_id, pa.pkaf_id) in
            (select pkaf_region_id, pkaf_id
              from uszn.dic_exp_pkaf_params
              where (exp_kind_region_id, exp_kind_id) in ((104,1)))
        ) or
        ( -- ������� ����� "������� ��������� ��������� � ��������� ����� �� ��� �� ������� 2008 ����"
          (pa.pkaf_region_id, pa.pkaf_id) in ((104, 339)) and
          -- ������� ������������ � ����������� ������������ ������ ��� ������
          -- ��� ��������� ���������, ����������  � ��������� � ��������� �����
          Exists(
            select 1
              from uszn.r_personal_doc_instances d, mapped_pkafs m
              where
                d.region_id=pa.region_id and d.people_coll_id=pa.pka_people_coll_id and
                -- �������� "�������� ���������"
                d.class_id=7116 and
                -- slurp-���� �������� ����� ���� � ������������ ��������� "�������� � ��������� �����..."
                m.pkaf_region_id*1000000+m.pkaf_id=uszn.ToIntDef(d.value)
          )
        ) or
        -- ��������� �������� �����, ��� ������� ������������ � �����������
        (pa.pkaf_region_id, pa.pkaf_id) in (select pkaf_region_id, pkaf_id from mapped_pkafs)
      ) /* ������ �� ��������� ����� */
    group by pa.region_id, pa.pka_people_coll_id
) r
