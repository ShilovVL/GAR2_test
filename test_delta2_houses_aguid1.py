import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions



@pytest.mark.parametrize("objectguid, housenum, isactive, addnum1, addnum2, housetype",
                         get_data_for_test(sql_strings["test_delta2_houses_aoguid"]["sql_request"] +
                                           str(sql_strings["test_delta2_houses_aoguid"]["limit"])))
def test_delta2_houses_aguid1(objectguid, housenum, isactive, addnum1, addnum2, housetype):
    url = f"{domen}/api/house/aoguid?aoguid={objectguid}&all=true"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0
    if len(response_body) > 1:
        for i in range(len(response_body)):
            if response_body[i]['HOUSEGUID'] == objectguid:
                testindex = i
    elif len(response_body) == 0:
        assert False, f"Получен пустой ответ, guid - {objectguid}"
    print("HouseNum -", response_body[testindex]["HOUSENUM"], " aoguid - \t", objectguid, "  |  \t",
          response_body[testindex]["HOUSEGUID"], end="")
    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert str.upper(response_body[testindex]["HOUSENUM"]) == str.upper(housenum)
    # проверяем strucnum == addnum2
    if response_body[testindex]['STRUCNUM'] is not None or addnum2 is not None:
        assert str.upper(response_body[testindex]["STRUCNUM"]) in [str.upper("СТРОЕНИЕ " + str(addnum2)),
                                                                   str.upper("Корпус " + str(addnum2)),
                                                                   str.upper("Сооружение " + str(addnum2)),
                                                                   str.upper("Литера " + str(addnum2))]
        print(f"STRUCNUM={response_body[testindex]['STRUCNUM']}, addnum2={addnum2}")

    # проверяем buildnum == addnum1
    if response_body[testindex]['BUILDNUM'] is not None or addnum1 is not None:
        assert str.upper(response_body[testindex]["BUILDNUM"]) in [str.upper("СТРОЕНИЕ " + str(addnum1)),
                                                                   str.upper("Корпус " + str(addnum1)),
                                                                   str.upper("Сооружение " + str(addnum1)),
                                                                   str.upper("Литера " + str(addnum1))]
        print(f"BUILDNUM={response_body[testindex]['BUILDNUM']}, addnum1={addnum1}")

    assert housetype is not None
    assert response_body[testindex]["HOUSENUM"] is not None
