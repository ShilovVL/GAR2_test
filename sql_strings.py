limit_no_region = "200"
limit_in_region = "50"

sql_strings = {"test_find_not_active_aguid": {"name": "find_not_active_aquid", "sql_request": "select objectguid, typename, name from addrobj where isactual = '1'  and isactive = '0' ORDER BY random() LIMIT ", "limit": limit_no_region},
               "test_find_not_active_aoid": {"name": "find_not_active_aoid", "sql_request": "select objectaoid, typename, name  from adm_objects_registry_historical where isactual = '1'  and isactive = '0' and objectaoid notnull ORDER BY random() LIMIT ", "limit": limit_no_region},
               "test_delta1_addr_object_aguid": {"name": "test_last_delta_update_aguid", "sql_request": "select objectguid, name from delta_addrobj a inner join delta_adm_hierarchy d on a.objectid =d.objectid  where a.isactive = 1  and d.isactive = 1"},
               "test_delta2_houses_aoguid": {"name": "test_delta2_houses", "sql_request": "select objectguid, housenum, isactive from delta_houses a  where a.isactive = 1 LIMIT ", "limit": limit_no_region}
               }
