import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions



@pytest.mark.parametrize("regioncode, objectguid, objectaoid, OKATO, OKTMO, name",
                         get_data_for_test_regions(sql_strings["test_find_addrobject_aguid_aoid"]["sql_request"],
                                                   count_regions,
                                                   sql_strings["test_find_addrobject_aguid_aoid"]["limit"]))
def test_find_addrobject_aguid(regioncode, objectguid, objectaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/addrobject/aoguid?aoguid={objectguid}&all=true"

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
