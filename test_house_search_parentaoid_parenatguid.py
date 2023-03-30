import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions


@pytest.mark.parametrize("parentaoid, housenum, objectaoid,       postal_code,      OKATO,    OKTMO,parentguid",
                         get_data_for_test(
                             sql_strings["test_house_search"]["sql_request"] + sql_strings["test_house_search"][
                                 "limit"]))
def test_house_search_parentaoid_parenatguid(parentaoid, housenum, objectaoid, postal_code, OKATO, OKTMO, parentguid):
    url = f"{domen}/api/house/search?aoid={parentaoid}&housenum={str.upper(housenum)}&all=true"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0

    if len(response_body) > 1:

        for i in range(len(response_body)):
            if response_body[i]['PARENTAOID'] == parentaoid and response_body[i]["OKTMO"] == OKTMO:
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
    url2 = f"{domen}/api/house/search?aoguid={parentguid}&housenum={str.upper(housenum)}"

    response = requests.get(url2)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0  # номер правильной записи в ответе

    if len(response_body) > 1:

        for i in range(len(response_body)):
            if response_body[i]['PARENTAOID'] == parentaoid and response_body[i]["OKTMO"] == OKTMO:
                testindex = i

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[testindex]['PARENTAOID'] == parentaoid
    assert response_body[testindex]["OKTMO"] == OKTMO
    assert response_body[testindex]["OKATO"] == OKATO
    assert str.upper(response_body[testindex]["HOUSENUM"]).find(str.upper(housenum)) >= 0
    assert response_body[testindex]["STRUCNUM"] != "null"
    assert response_body[testindex]["STRUCNUM"] or response_body[testindex]["BUILDNUM"] or response_body[testindex][
        "HOUSENUM"]
    # assert len(response_body[testindex]["STRUCNUM"]) > 0
