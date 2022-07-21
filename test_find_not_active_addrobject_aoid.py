import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions



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
