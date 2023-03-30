import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions


@pytest.mark.parametrize("region_code, prefix, AOGUID,     AOID,       OKATO, OKTMO, FORMALNAME",
                         get_data_for_test_regions_big(sql_strings["test_place"]["sql_request_1"],
                                                       sql_strings["test_place"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_place"]["limit"]))
def test_place(region_code, prefix, AOGUID, AOID, OKATO, OKTMO, FORMALNAME):
    url = f"{domen}/api/place?region_code={region_code}&prefix={prefix}&all=true"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'

    response_body = response.json()
    testindex = 0
    # print(len(response_body), response_body)

    if len(response_body) > 1:
        limit = len(response_body)

        for i in range(limit):
            if response_body[i]['AOID'] == AOID:
                testindex = i

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[testindex]["AOID"] == AOID
    assert response_body[testindex]["OKTMO"] == OKTMO
    assert response_body[testindex]["OKATO"] == OKATO
    if response_body[testindex]["AOLEVEL"] not in [2, 6, "2", "6"]:
        assert response_body[testindex]["FORMALNAME"] == FORMALNAME


    print(f"region_code={region_code}&prefix={prefix}",           end="")
