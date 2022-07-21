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
def test_find_addrobject_row_guid(objectguid, objectaoid, parentaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/addrobject/row?aoguid={objectguid}"

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

    if response_body[-1]["AOLEVEL"] not in [2, 6, "2", "6"]:
        assert len(response_body[-1]['MUNFULLNAME']) > 0

        if str(response_body[-1]["OFFNAME"]).find("Линия") >= 0 \
                or str(response_body[-1]["OFFNAME"]).find("Шоссе") >= 0 \
                or str(response_body[-1]["OFFNAME"]).find("Километр") >= 0 \
                or str(response_body[-1]["OFFNAME"]).find("Проспект") >= 0:
            pass
        else:
            assert str(response_body[-1]["MUNFULLNAME"]).find(response_body[-1]["OFFNAME"]) >= 0

    assert response_body[-1]["AOID"] == objectaoid
    assert response_body[-1]["OKTMO"] == OKTMO
    assert response_body[-1]["OKATO"] == OKATO
    assert response_body[-1]["FORMALNAME"] == name

