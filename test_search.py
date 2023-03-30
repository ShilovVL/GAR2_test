import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions


@pytest.mark.parametrize("regioncode, name, level, isactual, parentid, parent_name", get_data_for_test_search(
    sql_strings["test_search"]["sql_request_1"],
    sql_strings["test_search"]["sql_request_2"],
    number_regions=count_regions,
    limit_for_region=sql_strings["test_search"]["limit"]))
def test_search(regioncode, name, level, isactual, parentid, parent_name):
    str_query = str(parent_name + " " + name)
    url = f"{domen}/api/addrobject/search?query={str_query}&all=true"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    assert response.status_code == 200
    # response.encoding = 'utf-8'
    response = response.text

    response_body = json.loads(response)
    # response_body = response.json()
    # response_body.content.decode('unicode-escape', 'ignore')
    error_text = True
    error_act = True

    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    find_index = 0
    name_cute = name
    if len(name) >= 5:
        name_cute = name[:len(name) - 3]

    for i in range(len(response_body)):
        if str(response_body[i]["fullAddress"]).find(str(name)) >= 0 or str(response_body[i]["fullAddress"]).find(
                    str(name_cute)) >= 0:
            error_text = False
            find_index = i
            if response_body[i]["actStatus"] > 0:  # Запись актуальна
                error_act = False

                print(" Запрос - ", str_query, "   |  fullAddress", str(response_body[i]["fullAddress"]),
                      " | Позиция в отв. JSON ",
                      i + 1, "/", len(response_body), end="")
                break

    assert not error_text, f"Строка '{name}' не найдена в {response_body[find_index]['fullAddress']}"
    assert not error_act


def test_search_one_const_obj1(name='Центральное', parent_name='Барнаул'):
    str_query = str(parent_name + " " + name)
    url = f"{domen}/api/addrobject/search?query={str_query}&all=true"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    assert response.status_code == 200
    # response.encoding = 'utf-8'
    response = response.text

    response_body = json.loads(response)
    # response_body = response.json()
    # response_body.content.decode('unicode-escape', 'ignore')
    error_text = True
    error_act = True

    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    find_index = 0
    name_cute = name
    if len(name) >= 5:
        name_cute = name[:len(name) - 3]

    for i in range(len(response_body)):
        if str(response_body[i]["fullAddress"]).find(str(name)) >= 0 or str(response_body[i]["fullAddress"]).find(
                    str(name_cute)) >= 0:
            error_text = False
            find_index = i
            if response_body[i]["actStatus"] > 0:  # Запись актуальна
                error_act = False

                print(" Запрос - ", str_query, "   |  fullAddress", str(response_body[i]["fullAddress"]),
                      " | Позиция в отв. JSON ",
                      i + 1, "/", len(response_body), end="")
                break

    assert not error_text, f"Строка '{name}' не найдена в {response_body[find_index]['fullAddress']}"
    assert not error_act
