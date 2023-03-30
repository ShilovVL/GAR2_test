import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions


@pytest.mark.parametrize("objectguid, objectaoid, parentaoid, OKATO, OKTMO, name",
                         get_data_for_test_regions(sql_strings["test_find_addrobj_row"]["sql_request"],
                                                   count_regions,
                                                   sql_strings["test_find_addrobj_row"]["limit"]))
def test_find_addrobject_row_aoid(objectguid, objectaoid, parentaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/addrobject/row?aoid={objectaoid}"
    print(f"\n objectaoid - [{objectaoid}]")
    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    if len(response_body) > 1:
        for i in range(len(response_body)):
            if response_body[i]['AOID'] == parentaoid:
                found_parent = True
                print(" Parent found in response -", response_body[i]['AOID'], end="")
                break

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert found_parent
    assert str(type(response_body[0])) == "<class 'dict'>"

    assert response_body[-1]["AOID"] == objectaoid
    assert response_body[-1]["OKTMO"] == OKTMO
    assert response_body[-1]["OKATO"] == OKATO
    assert response_body[-1]["FORMALNAME"] == name

