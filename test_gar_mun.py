# -*- coding: utf-8 -*-
"""
Command 4 start: pytest -v --alluredir allure-results test_gartest.py
Command 4 view result: allure serve allure-results


"""

import requests
import json
import pytest
from sql_strings import sql_strings_mun
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time

mun = "&munHierarchy=true"
count_regions = 10

@pytest.mark.parametrize("regioncode, objectguid, objectaoid, OKATO, OKTMO, name",
                         get_data_for_test_regions(sql_strings_mun["test_find_addrobject_aguid_aoid"]["sql_request"],
                                                   count_regions,
                                                   sql_strings_mun["test_find_addrobject_aguid_aoid"]["limit"]))
def test_find_addrobject_aguid_mun(regioncode, objectguid, objectaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/addrobject/aoguid?aoguid={objectguid}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0
    if len(response_body) > 1:
        for i in range(len(response_body)):
            if response_body[i]['AOID'] == objectaoid:
                testindex = i
    print(response_body[testindex]["FORMALNAME"], " aoguid -", response_body[testindex]["AOGUID"], end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[testindex]["AOID"] == objectaoid
    assert response_body[testindex]["OKTMO"] == OKTMO
    assert response_body[testindex]["OKATO"] == OKATO
    assert response_body[testindex]["FORMALNAME"] == name


@pytest.mark.parametrize("regioncode, objectguid, objectaoid, OKATO, OKTMO, name",
                         get_data_for_test_regions(sql_strings_mun["test_find_addrobject_aguid_aoid"]["sql_request"],
                                                   count_regions,
                                                   sql_strings_mun["test_find_addrobject_aguid_aoid"]["limit"]))
def test_find_addrobject_aoid_mun(regioncode, objectguid, objectaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/addrobject/aoid?aoid={objectaoid}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print("\n", response_body["FORMALNAME"], response_body["AOGUID"], end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'dict'>"
    assert response_body["AOGUID"] == objectguid
    assert response_body["OKTMO"] == OKTMO
    assert response_body["OKATO"] == OKATO
    assert response_body["FORMALNAME"] == name


@pytest.mark.parametrize("parentaoid, parentguid, childcount",
                         get_data_for_test_regions_big(sql_strings_mun["test_find_childcount"]["sql_request_1"],
                                                       sql_strings_mun["test_find_childcount"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings_mun["test_find_childcount"]["limit"]))
def test_find_chilcount_parentaoid_parenatguid_mun(parentaoid, parentguid, childcount):
    # 1. Тест по parenaoid
    url = f"{domen}/api/addrobject/childCount?aoid={parentaoid}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'int'>"
    assert str(childcount) == str(response_body)

    # 2. Тест по parentguid
    url2 = f"{domen}/api/addrobject/childCount?aoguid={parentguid}{mun}"

    response = requests.get(url2)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print(f" Parentguid - [{parentguid}], Parentaoid - [{parentaoid}], Childcount -", response_body, end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'int'>"
    assert str(childcount) in [str(int(response_body)-1), str(response_body), str(int(response_body)+1)]


@pytest.mark.parametrize("objectguid, objectaoid, name",
                         get_data_for_test_regions(sql_strings_mun["test_find_addrobject_full"]["sql_request"],
                                                   count_regions,
                                                   sql_strings_mun["test_find_addrobject_full"]["limit"]))
def test_find_addrobject_full_guid_mun(objectguid, objectaoid, name):
    url = f"{domen}/api/addrobject/full?aoguid={objectguid}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.text
    if response_body.find(name) >= 0:
        print(f" [{name}] есть в ответе ", f"[{response_body}]", " | ", objectguid, end="")
    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'str'>"
    assert response_body.find(name) >= 0  # Есть ли название места в ответе (0 - слово на первом месте в ответе)


@pytest.mark.parametrize("objectguid, objectaoid, name",
                         get_data_for_test_regions(sql_strings_mun["test_find_addrobject_full"]["sql_request"],
                                                   count_regions,
                                                   sql_strings_mun["test_find_addrobject_full"]["limit"]))
def test_find_addrobject_full_aoid_mun(objectguid, objectaoid, name):
    url = f"{domen}/api/addrobject/full?aoid={objectaoid}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.text
    if response_body.find(name) >= 0:
        print(f" [{name}] есть в ответе ", f"[{response_body}]", end="")
    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'str'>"
    assert response_body.find(name) >= 0  # Есть ли название места в ответе (0 - слово на первом месте в ответе)


@pytest.mark.parametrize("parentaoid, parentguid, housecount",
                         get_data_for_test_regions_big(sql_strings_mun["test_find_addrobject_housecount"]["sql_request_1"],
                                                       sql_strings_mun["test_find_addrobject_housecount"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings_mun["test_find_addrobject_housecount"][
                                                           "limit"]))
def test_find_housecount_parentaoid_parenatguid_mun(parentaoid, parentguid, housecount):
    # 1. Тест по parent  aoid
    url = f"{domen}/api/addrobject/houseCount?aoid={parentaoid}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'int'>"
    assert str(housecount) == str(response_body)
    print(parentaoid, " HouseCount -", response_body, end="")
    # 2. Тест по parentguid
    url2 = f"{domen}/api/addrobject/houseCount?aoguid={parentguid}{mun}"

    response = requests.get(url2)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'int'>"
    assert str(housecount) == str(response_body)


@pytest.mark.parametrize("objectguid, objectaoid, parentaoid, OKATO, OKTMO, name",
                         get_data_for_test_regions(sql_strings_mun["test_find_addrobj_row"]["sql_request"],
                                                   count_regions,
                                                   sql_strings_mun["test_find_addrobj_row"]["limit"]))
def test_find_addrobject_row_aoid_mun(objectguid, objectaoid, parentaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/addrobject/row?aoid={objectaoid}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    if len(response_body) > 1:
        for i in range(len(response_body)):
            if response_body[i]['AOID'] == parentaoid:
                found_parent = True
                print(f" Parentaoid [{parentaoid}] for [{objectaoid}]found in response -", response_body[i]['AOID'], end="")
                break

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert found_parent
    assert str(type(response_body[0])) == "<class 'dict'>"

    assert response_body[-1]["AOID"] == objectaoid
    assert response_body[-1]["OKTMO"] == OKTMO
    assert response_body[-1]["OKATO"] == OKATO
    assert response_body[-1]["FORMALNAME"] == name


@pytest.mark.parametrize("objectguid, objectaoid, parentaoid, OKATO, OKTMO, name",
                         get_data_for_test_regions(sql_strings_mun["test_find_addrobj_row"]["sql_request"],
                                                   count_regions,
                                                   sql_strings_mun["test_find_addrobj_row"]["limit"]))
def test_find_addrobject_row_guid_mun(objectguid, objectaoid, parentaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/addrobject/row?aoguid={objectguid}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    found_parent = False
    if len(response_body) > 1:
        for i in range(len(response_body)):
            if response_body[i]['AOID'] == parentaoid:
                found_parent = True
                print(f" Parentaoid [{parentaoid}] for [{objectaoid}] found in response -", response_body[i]['AOID'], end="")
                break

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert found_parent
    assert str(type(response_body[0])) == "<class 'dict'>"

    assert response_body[-1]["AOID"] == objectaoid
    assert response_body[-1]["OKTMO"] == OKTMO
    assert response_body[-1]["OKATO"] == OKATO
    assert response_body[-1]["FORMALNAME"] == name


@pytest.mark.parametrize("region_code, place_aoguid, prefix, AOGUID,     AOID,       OKATO, OKTMO, streetname",
                         get_data_for_test_regions_big(sql_strings_mun["test_street"]["sql_request_1"],
                                                       sql_strings_mun["test_street"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings_mun["test_street"]["limit"]))
def test_street_mun(region_code, place_aoguid, prefix, AOGUID, AOID, OKATO, OKTMO, streetname):
    url = f"{domen}/api/street?place_aoguid={place_aoguid}&prefix={prefix}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    # response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0  # номер правильной записи в ответе

    if len(response_body) > 1:

        for i in range(len(response_body)):
            if response_body[i]["RELNAME"].find(streetname) >= 0 and str(response_body[i]["OKATO"]) == str(OKATO) \
                    and str(response_body[i]["OKTMO"]) == str(OKTMO):
                testindex = i

    print("\n aoguid ", place_aoguid, " | prefix ", prefix, " |  RELNAME ", response_body[testindex]["RELNAME"],
          " |  номер/место в ответе JSON - ", testindex + 1, "/", len(response_body), sep="", end="")

    assert response.status_code == 200
    assert response_body[testindex]["RELNAME"].find(str(streetname)) >= 0  # streetname найден в RELNAME?

    if str(response_body[testindex]["RELNAME"]).find(str(streetname)) >= 0:
        print(f"\n Стритнейм [{streetname}] найден в RELNAME [{response_body[testindex]['RELNAME']}]", end="")

    errors = False
    if str(response_body[testindex]["RELNAME"]).find(str(response_body[testindex]["OFFNAME"])) >= 0:
        print(f"\n OFFNAME [{response_body[testindex]['OFFNAME']}] "
              f"найден в RELNAME [{response_body[testindex]['RELNAME']}]",
              end="")

    elif str(response_body[testindex]["RELNAME"]).find(str("Километр")) >= 0 \
            or str(response_body[testindex]["RELNAME"]).find(str("Линия")) >= 0 \
            or str(response_body[testindex]["RELNAME"]).find(str("Проспект")) >= 0 \
            or str(response_body[testindex]["RELNAME"]).find(str("Тракт")) >= 0 \
            or str(response_body[testindex]["RELNAME"]).find(str("Шоссе")) >= 0:
        pass  # "100-й Километр  = Километр 100-й"
    else:
        errors = True
        print(f"\n OFFNAME [{response_body[testindex]['OFFNAME']}]  "
              f"HE найден в RELNAME [{response_body[testindex]['RELNAME']}]",
              end="")

    assert str(response_body[testindex]["RELNAME"]).find(",") != 0
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert not errors


@pytest.mark.parametrize("regioncode, parentaoid, housenum, objectguid, postal_code, OKATO, OKTMO",
                         get_data_for_test_regions_big(sql_strings_mun["test_find_house_aoguid"]["sql_request_1"],
                                                       sql_strings_mun["test_find_house_aoguid"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings_mun["test_street"]["limit"]))
def test_find_house_aoguid_mun(regioncode, parentaoid, housenum, objectguid, postal_code, OKATO, OKTMO):
    url = f"{domen}/api/house/aoguid?aoguid={objectguid}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print("\t" * 2, response_body[0]['RELNAME'], f" objectguid - [{objectguid}]")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[0]["PARENTAOID"] == parentaoid
    assert response_body[0]["OKTMO"] == OKTMO
    assert response_body[0]["OKATO"] == OKATO
    assert response_body[0]["HOUSENUM"] == str.upper(housenum)
    assert response_body[0]["POSTALCODE"] == postal_code
    assert response_body[0]["REGIONCODE"] == regioncode
    assert response_body[0]["AOGUID"] != "null"


@pytest.mark.parametrize("regioncode, parentaoid, housenum, objectaoid, postal_code, OKATO, OKTMO",
                         get_data_for_test_regions_big(sql_strings_mun["test_find_house_aoid"]["sql_request_1"],
                                                       sql_strings_mun["test_find_house_aoid"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings_mun["test_find_house_aoid"]["limit"]))
def test_find_house_aoid_mun(regioncode, parentaoid, housenum, objectaoid, postal_code, OKATO, OKTMO):
    url = f"{domen}/api/house/aoid?aoid={objectaoid}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print("\t", response_body['RELNAME'])
    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'dict'>"
    assert response_body["PARENTAOID"] == parentaoid
    assert response_body["OKTMO"] == OKTMO
    assert response_body["OKATO"] == OKATO
    assert response_body["HOUSENUM"] == str.upper(housenum)
    assert response_body["POSTALCODE"] == postal_code
    assert response_body["REGIONCODE"] == regioncode


@pytest.mark.parametrize("parentaoid, housenum, objectaoid,       postal_code,      OKATO,    OKTMO,parentguid",
                         get_data_for_test(
                             sql_strings_mun["test_house_search"]["sql_request"] + sql_strings_mun["test_house_search"][
                                 "limit"]))
def test_house_search_parentaoid_parenatguid_mun(parentaoid, housenum, objectaoid, postal_code, OKATO, OKTMO, parentguid):
    url = f"{domen}/api/house/search?aoid={parentaoid}&housenum={str.upper(housenum)}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0

    if len(response_body) > 1:

        for i in range(len(response_body)):
            if response_body[i]['PARENTAOID'] == parentaoid and response_body[i]["HOUSENUM"] == housenum:
                testindex = i

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[testindex]["PARENTAOID"] == parentaoid
    assert response_body[testindex]["OKTMO"] == OKTMO
    assert response_body[testindex]["OKATO"] == OKATO
    assert str.upper(response_body[testindex]["HOUSENUM"]).find(str.upper(housenum)) >= 0
    assert response_body[testindex]["STRUCNUM"] or response_body[testindex]["BUILDNUM"] or response_body[testindex][
        "HOUSENUM"]
    # assert len(response_body[testindex]["STRUCNUM"]) > 0 or len(response_body[testindex]["BUILDNUM"]) > 0

    # test with parentguid
    url2 = f"{domen}/api/house/search?aoguid={parentguid}&housenum={str.upper(housenum)}{mun}"

    response = requests.get(url2)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0  # номер правильной записи в ответе

    if len(response_body) > 1:

        for i in range(len(response_body)):
            if response_body[i]['PARENTAOID'] == parentaoid and response_body[i]["HOUSENUM"] == housenum:
                testindex = i

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[testindex]['PARENTAOID'] == parentaoid
    assert response_body[testindex]["OKTMO"] == OKTMO
    assert response_body[testindex]["OKATO"] == OKATO

    assert str.upper(response_body[testindex]["HOUSENUM"]).find(str.upper(housenum)) >= 0

    assert response_body[testindex]["STRUCNUM"] or response_body[testindex]["BUILDNUM"] or response_body[testindex][
        "HOUSENUM"]

    print(
        f"\n parentaoid - [{response_body[testindex]['PARENTAOID']}], housenum - [{response_body[testindex]['HOUSENUM']}]")


@pytest.mark.parametrize("region_code, prefix, AOGUID,     AOID,       OKATO, OKTMO, FORMALNAME",
                         get_data_for_test_regions_big(sql_strings_mun["test_place"]["sql_request_1"],
                                                       sql_strings_mun["test_place"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings_mun["test_place"]["limit"]))
def test_place_mun(region_code, prefix, AOGUID, AOID, OKATO, OKTMO, FORMALNAME):
    url = f"{domen}/api/place?region_code={region_code}&prefix={prefix}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'

    response_body = response.json()
    testindex = 0
    # print(len(response_body), response_body)

    if len(response_body) > 1:
        limit = len(response_body)

        for i in range(limit):
            if response_body[i]['AOID'] == AOID:
                testindex = i

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[testindex]["AOID"] == AOID
    assert response_body[testindex]["OKTMO"] == OKTMO
    assert response_body[testindex]["OKATO"] == OKATO
    if response_body[testindex]["AOLEVEL"] not in [2, 6, "2", "6"]:
        assert response_body[testindex]["FORMALNAME"] == FORMALNAME
    print(f"region_code={region_code}&prefix={prefix}", end="")


@pytest.mark.parametrize("regioncode, name, level, isactual, parentid, parent_name", get_data_for_test_search(
    sql_strings_mun["test_search"]["sql_request_1"],
    sql_strings_mun["test_search"]["sql_request_2"],
    number_regions=count_regions,
    limit_for_region=sql_strings_mun["test_search"]["limit"]))
def test_search_mun(regioncode, name, level, isactual, parentid, parent_name):
    global i
    str_query = str(parent_name + " " + name)
    url = f"{domen}/api/addrobject/search?query={str_query}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    assert response.status_code == 200
    # response.encoding = 'utf-8'
    response = response.text

    response_body = json.loads(response)
    # response_body = response.json()
    # response_body.content.decode('unicode-escape', 'ignore')
    error_text = True
    error_act = True

    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    find_index = 0
    name_cute = name
    if len(name) >= 5:
        name_cute = name[:len(name) - 3]

    for i in range(len(response_body)):
        if str(response_body[i]["fullAddress"]).find(str(name)) >= 0 or str(response_body[i]["fullAddress"]).find(
                    str(name_cute)) >= 0:
            error_text = False
            find_index = i
            if response_body[i]["actStatus"] > 0:  # Запись актуальна
                error_act = False

                print(" Запрос - ", str_query, "   |  fullAddress", str(response_body[i]["fullAddress"]),
                      " | Позиция в отв. JSON ",
                      i + 1, "/", len(response_body), end="")
                break

    assert not error_text, f"Строка '{name}' не найдена в {response_body[find_index]['fullAddress']}"
    assert not error_act


@pytest.mark.parametrize("regioncode, parentaoid, housenum, objectguid, postal_code, OKATO, OKTMO",
                         get_data_for_test_regions_big(sql_strings_mun["test_house_aoguid_not_null"]["sql_request_1"],
                                                       sql_strings_mun["test_house_aoguid_not_null"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings_mun["test_house_aoguid_not_null"][
                                                           "limit"]))
def test_find_house_aoguid_notnull_mun(regioncode, parentaoid, housenum, objectguid, postal_code, OKATO, OKTMO):
    url = f"{domen}/api/house/aoguid?aoguid={objectguid}{mun}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print("\t" * 2, response_body[0]['RELNAME'], " AOGUID -", response_body[0]["AOGUID"], objectguid, end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[0]["PARENTAOID"] == parentaoid
    assert response_body[0]["OKTMO"] == OKTMO
    assert response_body[0]["OKATO"] == OKATO
    assert response_body[0]["HOUSENUM"] == str.upper(housenum)
    assert response_body[0]["POSTALCODE"] == postal_code
    assert response_body[0]["REGIONCODE"] == regioncode
    assert response_body[0]["AOGUID"] is not None

