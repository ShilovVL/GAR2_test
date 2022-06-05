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
    # Часть 1. Тест по parenaoid
    url = f"{domen}/api/addrobject/childCount?aoid={parentaoid}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'int'>"
    assert str(childcount) == str(response_body)

    # Часть 2. Тест по parentguid
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
    # Часть 1. Тест по parenaoid
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
    # Часть 2. Тест по parentguid
    url2 = f"{domen}/api/addrobject/houseCount?aoguid={parentguid}"

    response = requests.get(url2)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'int'>"
    assert str(housecount) == str(response_body)
