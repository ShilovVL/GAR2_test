import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions


@pytest.mark.parametrize("regioncode, parentaoid, housenum, objectguid, postal_code, OKATO, OKTMO",
                         get_data_for_test_regions_big(sql_strings["test_house_aoguid_not_null"]["sql_request_1"],
                                                       sql_strings["test_house_aoguid_not_null"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_house_aoguid_not_null"][
                                                           "limit"]))
def test_find_house_aoguid_notnull(regioncode, parentaoid, housenum, objectguid, postal_code, OKATO, OKTMO):
    url = f"{domen}/api/house/aoguid?aoguid={objectguid}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print("\t" * 2, response_body[0]['RELNAME'], " AOGUID -", response_body[0]["AOGUID"], objectguid, end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[0]["PARENTAOID"] == parentaoid
    assert response_body[0]["OKTMO"] == OKTMO
    assert response_body[0]["OKATO"] == OKATO
    assert response_body[0]["HOUSENUM"] == str.upper(housenum)
    assert response_body[0]["POSTALCODE"] == postal_code
    assert response_body[0]["REGIONCODE"] == regioncode
    assert response_body[0]["AOGUID"] != "None"
    assert response_body[0]["AOGUID"] is not None
    assert len(response_body[0]["AOGUID"]) != 0