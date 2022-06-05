limit_no_region = "200"
limit_in_region = "10"

sql_strings = {"test_find_not_active_aguid":    {"name": "find_not_active_aquid", "sql_request": "select objectguid, typename, name from addrobj where isactual = '1'  and isactive = '0' ORDER BY random() LIMIT ", "limit": limit_no_region},
               "test_find_not_active_aoid":     {"name": "find_not_active_aoid", "sql_request": "select objectaoid, typename, name  from adm_objects_registry_historical where isactual = '1'  and isactive = '0' and objectaoid notnull ORDER BY random() LIMIT ", "limit": limit_no_region},
               "test_delta1_addr_object_aguid": {"name": "test_last_delta_update_aguid", "sql_request": "select objectguid, name from delta_addrobj a inner join delta_adm_hierarchy d on a.objectid =d.objectid  where a.isactive = 1  and d.isactive = 1"},
               "test_delta2_houses_aoguid":     {"name": "test_delta2_houses", "sql_request": "select objectguid, housenum, isactive from delta_houses a  where a.isactive = 1 LIMIT ", "limit": limit_no_region},
               "test_find_addrobject_aguid_aoid":   {"name": "test_addrobj_aguid_aoid", "sql_request": "select regioncode, objectguid, objectaoid, t6 OKATO, t7 OKTMO, name from adm_objects_registry where level in (1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15,16) and regioncode = ", "limit": limit_in_region},
               "test_find_childcount":          {"name": "test_childcount", "sql_request_1": "select parentaoid, parentguid, count(parentaoid) from adm_objects_registry where regioncode = ", "sql_request_2": " group by (parentaoid, parentguid ) having count(parentaoid) > '2' limit ", "limit": limit_in_region},
               "test_find_addrobject_full":     {"name": "test_addrobj_full", "sql_request": "select objectguid, objectaoid, name from adm_objects_registry where level in (1, 2, 3,4,5,6,7,8,14) and regioncode = ", "limit": limit_in_region},
               "test_find_addrobject_housecount":   {"name": "test_housecount", "sql_request_1": "select parentaoid, parentguid , count(parentaoid)  from adm_houses_registry ahr  where regioncode  = ", "sql_request_2": " group by (parentaoid, parentguid ) having count(parentaoid) > '1' limit ", "limit": limit_in_region},
               "test_find_addrobj_row":         {"name": "test_addrobj_row", "sql_request": "select objectguid, objectaoid, parentaoid, t6 OKATO, t7 OKTMO, name from adm_objects_registry where level in (2, 3,4,5,6,7,8,14) and regioncode = ", "limit": limit_in_region}
               }

"""


"""