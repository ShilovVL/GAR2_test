# -*- coding: utf-8 -*-
import requests
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from urls import domen

response_time = 20.00  # Максимальное время ответа, не считающееся ошибкой (сек)
count_regions = 5  # Сколько регионов тестим. "77", "78", "75", "99", "74" + рандомные


@pytest.mark.parametrize("objectguid, typename, name",
                         get_data_for_test(sql_strings["test_find_not_active_aguid"]["sql_request"] +
                                           str(sql_strings["test_find_not_active_aguid"]["limit"])))
def test_find_not_active_addrobject_aoguid(objectguid, typename, name):
    url = f"{domen}/api/addrobject/aoguid?aoguid={objectguid}&all=true"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print(response_body[0]["FORMALNAME"], response_body[0]["AOID"], " Livestatus = ", response_body[0]["LIVESTATUS"],
          end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'list'>"
    assert response_body[0]["LIVESTATUS"] == 0
    assert len(response_body) > 0


@pytest.mark.parametrize("objectaoid, typename, name", get_data_for_test(
    sql_strings["test_find_not_active_aoid"]["sql_request"] +
    str(sql_strings["test_find_not_active_aoid"]["limit"])))
def test_find_not_active_addrobject_aoid(objectaoid, typename, name):
    url = f"{domen}/api/addrobject/aoid?aoid={objectaoid}&all=true"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print(f"{typename} {name} в ответе -", response_body["FORMALNAME"], response_body["AOID"], end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'dict'>"
    assert response_body["LIVESTATUS"] == 0
    assert len(response_body) > 0


@pytest.mark.parametrize("objectguid, name",
                         get_data_for_test(sql_strings["test_delta1_addr_object_aguid"]["sql_request"]))
def test_delta_addrobject_aguid(objectguid, name):
    url = f"{domen}/api/addrobject/aoguid?aoguid={objectguid}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0
    if len(response_body) > 1:
        for i in range(len(response_body)):
            if response_body[i]['FORMALNAME'] == name:
                testindex = i
    print(response_body[testindex]["FORMALNAME"], " aoguid -", response_body[testindex]["AOGUID"], end="")
    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[testindex]["FORMALNAME"] == name


@pytest.mark.parametrize("objectguid, housenum, isactive",
                         get_data_for_test(sql_strings["test_delta2_houses_aoguid"]["sql_request"] +
                                           str(sql_strings["test_delta2_houses_aoguid"]["limit"])))
def test_delta2_houses_aguid1(objectguid, housenum, isactive):
    url = f"{domen}/api/house/aoguid?aoguid={objectguid}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0
    if len(response_body) > 1:
        for i in range(len(response_body)):
            if response_body[i]['HOUSEGUID'] == objectguid:
                testindex = i
    elif len(response_body) == 0:
        assert False, f"Получен пустой ответ, guid - {objectguid}"
    print("HouseNum -", response_body[testindex]["HOUSENUM"], " aoguid - \t", objectguid, "  |  \t",
          response_body[testindex]["HOUSEGUID"], end="")
    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert str.upper(response_body[testindex]["HOUSENUM"]) == str.upper(housenum)


@pytest.mark.parametrize("regioncode, objectguid, objectaoid, OKATO, OKTMO, name",
                         get_data_for_test_regions(sql_strings["test_find_addrobject_aguid_aoid"]["sql_request"],
                                                   count_regions,
                                                   sql_strings["test_find_addrobject_aguid_aoid"]["limit"]))
def test_find_addrobject_aguid(regioncode, objectguid, objectaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/addrobject/aoguid?aoguid={objectguid}"

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
                         get_data_for_test_regions(sql_strings["test_find_addrobject_aguid_aoid"]["sql_request"],
                                                   count_regions,
                                                   sql_strings["test_find_addrobject_aguid_aoid"]["limit"]))
def test_find_addrobject_aoid(regioncode, objectguid, objectaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/addrobject/aoid?aoid={objectaoid}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print(response_body["FORMALNAME"], response_body["AOGUID"], end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'dict'>"
    assert response_body["AOGUID"] == objectguid
    assert response_body["OKTMO"] == OKTMO
    assert response_body["OKATO"] == OKATO
    assert response_body["FORMALNAME"] == name


@pytest.mark.parametrize("parentaoid, parentguid, childcount",
                         get_data_for_test_regions_big(sql_strings["test_find_childcount"]["sql_request_1"],
                                                       sql_strings["test_find_childcount"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_find_addrobject_aguid_aoid"][
                                                           "limit"]))
def test_find_chilcount_parentaoid_parenatguid(parentaoid, parentguid, childcount):
    # 1. Тест по parenaoid
    url = f"{domen}/api/addrobject/childCount?aoid={parentaoid}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'int'>"
    assert str(childcount) == str(response_body)

    # 2. Тест по parentguid
    url2 = f"{domen}/api/addrobject/childCount?aoguid={parentguid}"

    response = requests.get(url2)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print(" Childcount -", response_body, end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'int'>"
    assert str(childcount) == str(response_body)


@pytest.mark.parametrize("objectguid, objectaoid, name",
                         get_data_for_test_regions(sql_strings["test_find_addrobject_full"]["sql_request"],
                                                   count_regions,
                                                   sql_strings["test_find_addrobject_full"]["limit"]))
def test_find_addrobject_full_guid(objectguid, objectaoid, name):
    url = f"{domen}/api/addrobject/full?aoguid={objectguid}"

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
                         get_data_for_test_regions(sql_strings["test_find_addrobject_full"]["sql_request"],
                                                   count_regions,
                                                   sql_strings["test_find_addrobject_full"]["limit"]))
def test_find_addrobject_full_aoid(objectguid, objectaoid, name):
    url = f"{domen}/api/addrobject/full?aoid={objectaoid}"

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
                         get_data_for_test_regions_big(sql_strings["test_find_addrobject_housecount"]["sql_request_1"],
                                                       sql_strings["test_find_addrobject_housecount"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_find_addrobject_housecount"][
                                                           "limit"]))
def test_find_housecount_parentaoid_parenatguid(parentaoid, parentguid, housecount):
    # 1. Тест по parenaoid
    url = f"{domen}/api/addrobject/houseCount?aoid={parentaoid}"

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
    url2 = f"{domen}/api/addrobject/houseCount?aoguid={parentguid}"

    response = requests.get(url2)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'int'>"
    assert str(housecount) == str(response_body)


@pytest.mark.parametrize("objectguid, objectaoid, parentaoid, OKATO, OKTMO, name",
                         get_data_for_test_regions(sql_strings["test_find_addrobj_row"]["sql_request"],
                                                   count_regions,
                                                   sql_strings["test_find_addrobj_row"]["limit"]))
def test_find_addrobject_row_aoid(objectguid, objectaoid, parentaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/addrobject/row?aoid={objectaoid}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    if len(response_body) > 1:
        for i in range(len(response_body)):
            if response_body[i]['AOID'] == parentaoid:
                found_parent = True
                print(" Parent found in response -", response_body[i]['AOID'], end="")
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
                         get_data_for_test_regions(sql_strings["test_find_addrobj_row"]["sql_request"],
                                                   count_regions,
                                                   sql_strings["test_find_addrobj_row"]["limit"]))
def test_find_addrobject_row_guid(objectguid, objectaoid, parentaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/addrobject/row?aoguid={objectguid}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    if len(response_body) > 1:
        for i in range(len(response_body)):
            if response_body[i]['AOID'] == parentaoid:
                found_parent = True
                print(" Parent found in response -", response_body[i]['AOID'], end="")
                break

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert found_parent
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[-1]["AOID"] == objectaoid
    assert response_body[-1]["OKTMO"] == OKTMO
    assert response_body[-1]["OKATO"] == OKATO
    assert response_body[-1]["FORMALNAME"] == name


@pytest.mark.parametrize("region_code, place_aoguid, prefix, AOGUID,     AOID,       OKATO, OKTMO, FORMALNAME",
                         get_data_for_test_regions_big(sql_strings["test_street"]["sql_request_1"],
                                                       sql_strings["test_street"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_street"]["limit"]))
def test_street_pg(region_code, place_aoguid, prefix, AOGUID, AOID, OKATO, OKTMO, FORMALNAME):
    url = f"{domen}/api/street?place_aoguid={place_aoguid}&prefix={prefix}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    # response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0  # номер правильной записи в ответе

    if len(response_body) > 1:

        for i in range(len(response_body)):
            if response_body[i]['AOID'] == AOID:
                testindex = i
    print("place_aoguid ", place_aoguid, " | prefix ", prefix, " |  RELNAME ", response_body[testindex]["RELNAME"],
          " |  номер/место в ответе JSON - ", testindex + 1, "/", len(response_body), sep="", end="")
    assert response.status_code == 200
    # assert response_body[testindex]["RELNAME"] == response_body[testindex]["OFFNAME"]
    assert str(response_body[testindex]["RELNAME"]).find(str(prefix)) >= 0  # prefix найден в RELNAME?

    if str(response_body[testindex]["RELNAME"]).find(str(prefix)) >= 0:
        print(f"\n Префикс [{prefix}] найден в строке [{response_body[testindex]['RELNAME']}]", end="")
    if str(response_body[testindex]["RELNAME"]).find(str(response_body[testindex]["OFFNAME"])) >= 0:
        print(
            f"\n OFFNAME [{response_body[testindex]['OFFNAME']}] найден в строке [{response_body[testindex]['RELNAME']}]",
            end="")
    else:
        print(
            f"\n OFFNAME [{response_body[testindex]['OFFNAME']}]  HE найден в строке [{response_body[testindex]['RELNAME']}]",
            end="")
    assert str(response_body[testindex]["RELNAME"]).find(",") != 0
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[testindex]["AOID"] == AOID
    assert response_body[testindex]["OKTMO"] == OKTMO
    assert response_body[testindex]["OKATO"] == OKATO
    assert response_body[testindex]["FORMALNAME"] == FORMALNAME


@pytest.mark.parametrize("regioncode, parentaoid, housenum, objectguid, postal_code, OKATO, OKTMO",
                         get_data_for_test_regions_big(sql_strings["test_find_house_aoguid"]["sql_request_1"],
                                                       sql_strings["test_find_house_aoguid"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_street"]["limit"]))
def test_find_house_aoguid(regioncode, parentaoid, housenum, objectguid, postal_code, OKATO, OKTMO):
    url = f"{domen}/api/house/aoguid?aoguid={objectguid}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print("\t" * 2, response_body[0]['RELNAME'], end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[0]["PARENTAOID"] == parentaoid
    assert response_body[0]["OKTMO"] == OKTMO
    assert response_body[0]["OKATO"] == OKATO
    assert response_body[0]["HOUSENUM"] == str.upper(housenum)
    assert response_body[0]["POSTALCODE"] == postal_code
    assert response_body[0]["REGIONCODE"] == regioncode


@pytest.mark.parametrize("regioncode, parentaoid, housenum, objectaoid, postal_code, OKATO, OKTMO",
                         get_data_for_test_regions_big(sql_strings["test_find_house_aoguid"]["sql_request_1"],
                                                       sql_strings["test_find_house_aoguid"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_street"]["limit"]))
def test_find_house_aoid(regioncode, parentaoid, housenum, objectaoid, postal_code, OKATO, OKTMO):
    url = f"{domen}/api/house/aoid?aoid={objectaoid}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print("\t", response_body['RELNAME'], end="")

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
                         get_data_for_test(sql_strings["test_house_search"]["sql_request"] + sql_strings["test_house_search"]["limit"]))
def test_house_search_parentaoid_parenatguid(parentaoid, housenum, objectaoid, postal_code, OKATO, OKTMO, parentguid):
    url = f"{domen}/api/house/search?aoid={parentaoid}&housenum={str.upper(housenum)}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0

    if len(response_body) > 1:

        for i in range(len(response_body)):
            if response_body[i]['PARENTAOID'] == parentaoid:
                testindex = i

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[testindex]["PARENTAOID"] == parentaoid
    assert response_body[testindex]["OKTMO"] == OKTMO
    assert response_body[testindex]["OKATO"] == OKATO
    assert response_body[testindex]["HOUSENUM"] == str.upper(housenum)
    # test with parentguid
    url2 = f"{domen}/api/house/search?aoguid={parentguid}&housenum={str.upper(housenum)}"

    response = requests.get(url2)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0  # номер правильной записи в ответе

    if len(response_body) > 1:

        for i in range(len(response_body)):
            if response_body[i]['PARENTAOID'] == parentaoid:
                testindex = i

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[testindex]["PARENTAOID"] == parentaoid
    assert response_body[testindex]["OKTMO"] == OKTMO
    assert response_body[testindex]["OKATO"] == OKATO
    assert response_body[testindex]["HOUSENUM"] == str.upper(housenum)


@pytest.mark.parametrize("region_code, prefix, AOGUID,     AOID,       OKATO, OKTMO, FORMALNAME",
                         get_data_for_test_regions_big(sql_strings["test_place"]["sql_request_1"],
                                                       sql_strings["test_place"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_place"]["limit"]))
def test_place_pg(region_code, prefix, AOGUID, AOID, OKATO, OKTMO, FORMALNAME):
    url = f"{domen}/api/place?region_code={region_code}&prefix={prefix}"

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
    assert response_body[testindex]["FORMALNAME"] == FORMALNAME
