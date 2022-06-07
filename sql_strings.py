from params import limit_in_region, limit_no_region

sql_strings = {"test_find_not_active_aguid":    {"name": "find_not_active_aquid", "sql_request": "select objectguid, typename, name from addrobj where isactual = '1'  and isactive = '0' ORDER BY random() LIMIT ", "limit": limit_no_region},
               "test_find_not_active_aoid":     {"name": "find_not_active_aoid", "sql_request": "select objectaoid, typename, name  from adm_objects_registry_historical where isactual = '1'  and isactive = '0' and objectaoid notnull ORDER BY random() LIMIT ", "limit": limit_no_region},
               "test_delta1_addr_object_aguid": {"name": "test_last_delta_update_aguid", "sql_request": "select objectguid, name from delta_addrobj a inner join delta_adm_hierarchy d on a.objectid =d.objectid  where a.isactive = 1  and d.isactive = 1"},
               "test_delta2_houses_aoguid":     {"name": "test_delta2_houses", "sql_request": "select objectguid, housenum, isactive from delta_houses a  where a.isactive = 1 LIMIT ", "limit": limit_no_region},
               "test_find_addrobject_aguid_aoid":   {"name": "test_addrobj_aguid_aoid", "sql_request": "select regioncode, objectguid, objectaoid, t6 OKATO, t7 OKTMO, name from adm_objects_registry where level in (1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15,16) and regioncode = ", "limit": limit_in_region},
               "test_find_childcount":          {"name": "test_childcount", "sql_request_1": "select parentaoid, parentguid, count(parentaoid) from adm_objects_registry where regioncode = ", "sql_request_2": " group by (parentaoid, parentguid ) having count(parentaoid) > '2' limit ", "limit": limit_in_region},
               "test_find_addrobject_full":     {"name": "test_addrobj_full", "sql_request": "select objectguid, objectaoid, name from adm_objects_registry where level in (1, 2, 3,4,5,6,7,8,14) and regioncode = ", "limit": limit_in_region},
               "test_find_addrobject_housecount":   {"name": "test_housecount", "sql_request_1": "select parentaoid, parentguid , count(parentaoid)  from adm_houses_registry ahr  where regioncode  = ", "sql_request_2": " group by (parentaoid, parentguid ) having count(parentaoid) > '1' limit ", "limit": limit_in_region},
               "test_find_addrobj_row":         {"name": "test_addrobj_row", "sql_request": "select objectguid, objectaoid, parentaoid, t6 OKATO, t7 OKTMO, name from adm_objects_registry where level in (2, 3,4,5,6,7,8,14) and regioncode = ", "limit": limit_in_region},
               "test_find_regions":             {"name": "test_regions", "sql_request": "select regioncode, objectaoid, t6 OKATO, t7 OKTMO, name from adm_objects_registry where level in (1) order by objectid "},
               "test_street":                   {"name": "test_street", "sql_request_1": "select regioncode, parentguid, name, objectguid, objectaoid, t6, t7, name  from adm_objects_registry where level in (7,8,9,10,11,12,13,14,15,16) and regioncode = ", "sql_request_2": " order by level limit ", "limit": limit_in_region},
               "test_find_house_aoguid":        {"name": "test_house_aoguid", "sql_request_1": "select regioncode, parentaoid, housenum, objectguid, t5 as postal_code, t6 as OKATO, t7 OKTMO from adm_houses_registry where isactual = '1' and regioncode = ", "sql_request_2": " and isactive = '1' and t5 notnull limit ", "limit": limit_in_region},
               "test_house_search":             {"name": "test_house_search", "sql_request": "select parentaoid, housenum, objectaoid, t5 as postal_code, t6 as OKATO, t7 OKTMO, parentguid from adm_houses_registry where isactual = '1' and isactive = '1' and t5 notnull limit ", "limit": limit_in_region},
               "test_place":                    {"name": "test_place", "sql_request_1": "select regioncode , name, objectguid, objectaoid, t6, t7, name  from adm_objects_registry where level in (2,3,4,5,6) and regioncode = ", "sql_request_2": " order by level limit ", "limit": limit_in_region},
               "test_search":                   {"name": "test_search", "sql_request_1": "select regioncode, name, level, isactual, parentid from adm_objects_registry where level in (floor(random()*(15-4+1))+4) and regioncode = ", "sql_request_2": "select name from  adm_objects_registry aor where objectid = ", "limit": limit_in_region}
               }

"""


"""