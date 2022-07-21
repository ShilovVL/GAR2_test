import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions


@pytest.mark.parametrize("parentaoid, parentguid, housecount",
                         get_data_for_test_regions_big(sql_strings["test_find_addrobject_housecount"]["sql_request_1"],
                                                       sql_strings["test_find_addrobject_housecount"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_find_addrobject_housecount"][
                                                           "limit"]))
def test_find_housecount_parentaoid_parenatguid(parentaoid, parentguid, housecount):
    # 1. Тест по parent  aoid
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

