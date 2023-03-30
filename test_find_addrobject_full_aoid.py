import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions


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
