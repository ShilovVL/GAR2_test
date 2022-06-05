# -*- coding: utf-8 -*-
import requests
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test
from urls import domen

response_time = 20.00  # Максимальное время ответа, не считающееся ошибкой (сек)


@pytest.mark.parametrize("objectguid, typename, name",
                         get_data_for_test(sql_strings["test_find_not_active_aguid"]["sql_request"] +
                                           str(sql_strings["test_find_not_active_aguid"]["limit"])))
def test_find_not_active_addrobject_aoguid(objectguid, typename, name):
    url = f"{domen}/api/addrobject/aoguid?aoguid={objectguid}&all=true"
    # headers = {
    #     'accept': 'application/json; charset=UTF-8'
    # }

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


#                         objectguid, name
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


#                         objectguid, housenum, isactive
@pytest.mark.parametrize("objectguid, housenum, isactive", get_data_for_test(sql_strings["test_delta2_houses_aoguid"]["sql_request"] +
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
    print("HouseNum -", response_body[testindex]["HOUSENUM"], " aoguid - \t", objectguid, "  |  \t", response_body[testindex]["HOUSEGUID"], end="")
    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert str.upper(response_body[testindex]["HOUSENUM"]) == str.upper(housenum)