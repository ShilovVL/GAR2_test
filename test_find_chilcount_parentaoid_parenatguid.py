import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions


@pytest.mark.parametrize("parentaoid, parentguid, childcount",
                         get_data_for_test_regions_big(sql_strings["test_find_childcount"]["sql_request_1"],
                                                       sql_strings["test_find_childcount"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_find_childcount"]["limit"]))
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
    print(f" Parentguid - [{parentguid}], Parentaoid - [{parentaoid}], Childcount -", response_body, end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body)) == "<class 'int'>"
    assert str(childcount) == str(response_body)

