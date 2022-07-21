# -*- coding: utf-8 -*-
import requests
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from urls import domen
from params import response_time, version_gar


def test_get_version_gar():
    url = f"{domen}/api/version"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.text

    assert response.status_code == 200
    assert elapsed_time <= response_time

    assert str(response_body) == str(version_gar)
    print(" Версия ГАР -", response_body, end="")


def test_get_all_versions_DB_gar():
    url = f"{domen}/gar/versions"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print(" Загруженные обновления - ", end="")
    for i in response_body:
        print(i['TEXTVERSION'], end=", ")
        pass

    assert response.status_code == 200
    assert elapsed_time <= response_time


def test_regions():
    url = f"{domen}/api/regions"  # Один запрос выводит список всех регионов РФ

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()

    assert response.status_code == 200
    assert elapsed_time <= response_time
    sql_data = get_data_for_test(sql_strings["test_find_regions"]["sql_request"])
    print("")
    response_lenght = len(response_body)

    for i in range(response_lenght):
        for y in range(response_lenght):
            if response_body[y]["AOID"] == sql_data[i][1]:
                assert response_body[y]["OKATO"] == sql_data[i][2]
                assert response_body[y]["OKTMO"] == sql_data[i][3]
                assert response_body[y]["FORMALNAME"] == sql_data[i][4]
                assert response_body[y]["REGIONCODE"] == sql_data[i][0]
                assert str(response_body[y]["MUNFULLNAME"]).find(response_body[y]["FORMALNAME"]) >= 0
                assert len(str(response_body[y]["MUNFULLNAME"])) > 0
                print("", response_body[y]['RELNAME'], " Ok")
                print(f" MUNFULLNAME - [{response_body[y]['MUNFULLNAME']}]", end="\n\n")
                break


@pytest.mark.parametrize("regioncode, objectaoid, OKATO, OKTMO, name",
                         get_data_for_test(sql_strings["test_find_regions"]["sql_request"]))
def test_region_code(regioncode, objectaoid, OKATO, OKTMO, name):
    url = f"{domen}/api/region/code?code={regioncode}"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    response.encoding = 'utf-8'
    response_body = response.json()
    print("\t" * 2, response_body[0]['RELNAME'])
    print(f"\t 'MUNFULLNAME' - [{response_body[0]['MUNFULLNAME']}]", end="")

    assert response.status_code == 200
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert response_body[0]["AOID"] == objectaoid
    assert response_body[0]["OKTMO"] == OKTMO
    assert response_body[0]["OKATO"] == OKATO
    assert response_body[0]["FORMALNAME"] == name
    assert response_body[0]["REGIONCODE"] == regioncode
    assert str(response_body[0]["MUNFULLNAME"]).find(response_body[0]["FORMALNAME"]) >= 0
    assert len(str(response_body[0]["MUNFULLNAME"])) > 0

