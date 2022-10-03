import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions


@pytest.mark.parametrize("regioncode, parentaoid, housenum, objectaoid, postal_code, OKATO, OKTMO",
                         get_data_for_test_regions_big(sql_strings["test_find_house_aoid"]["sql_request_1"],
                                                       sql_strings["test_find_house_aoid"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_find_house_aoid"]["limit"]))
def test_find_house_aoid(regioncode, parentaoid, housenum, objectaoid, postal_code, OKATO, OKTMO):
    url = f"{domen}/api/house/aoid?aoid={objectaoid}&all=true"

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

