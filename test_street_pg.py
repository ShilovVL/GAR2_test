import requests
import json
import pytest
from sql_strings import sql_strings
from sql_connector import get_data_for_test, get_data_for_test_regions, get_data_for_test_regions_big
from sql_connector import get_data_for_test_search
from urls import domen
from params import response_time, count_regions


@pytest.mark.parametrize("region_code, place_aoguid, prefix, AOGUID,     AOID,       OKATO, OKTMO, streetname",
                         get_data_for_test_regions_big(sql_strings["test_street"]["sql_request_1"],
                                                       sql_strings["test_street"]["sql_request_2"],
                                                       number_regions=count_regions,
                                                       limit_for_region=sql_strings["test_street"]["limit"]))
def test_street_pg(region_code, place_aoguid, prefix, AOGUID, AOID, OKATO, OKTMO, streetname):
    url = f"{domen}/api/street?place_aoguid={place_aoguid}&prefix={prefix}&all=true"

    response = requests.get(url)
    elapsed_time = response.elapsed.total_seconds()
    # response.encoding = 'utf-8'
    response_body = response.json()
    testindex = 0  # номер правильной записи в ответе

    if len(response_body) > 1:

        for i in range(len(response_body)):
            if response_body[i]["RELNAME"].find(streetname) >= 0 and str(response_body[i]["OKATO"]) == str(OKATO) \
                    and str(response_body[i]["OKTMO"]) == str(OKTMO):
                testindex = i

    print("\n aoguid ", place_aoguid, " | prefix ", prefix, " |  RELNAME ", response_body[testindex]["RELNAME"],
          " |  номер/место в ответе JSON - ", testindex + 1, "/", len(response_body), sep="", end="")

    assert response.status_code == 200
    assert response_body[testindex]["RELNAME"].find(str(streetname)) >= 0  # streetname найден в RELNAME?

    if str(response_body[testindex]["RELNAME"]).find(str(streetname)) >= 0:
        print(f"\n Стритнейм [{streetname}] найден в RELNAME [{response_body[testindex]['RELNAME']}]", end="")

    errors = False
    if str(response_body[testindex]["RELNAME"]).find(str(response_body[testindex]["OFFNAME"])) >= 0:
        print(f"\n OFFNAME [{response_body[testindex]['OFFNAME']}] "
              f"найден в RELNAME [{response_body[testindex]['RELNAME']}]",
              end="")

    elif str(response_body[testindex]["RELNAME"]).find(str("Километр")) >= 0 \
            or str(response_body[testindex]["RELNAME"]).find(str("Линия")) >= 0 \
            or str(response_body[testindex]["RELNAME"]).find(str("Проспект")) >= 0 \
            or str(response_body[testindex]["RELNAME"]).find(str("Тракт")) >= 0 \
            or str(response_body[testindex]["RELNAME"]).find(str("Шоссе")) >= 0:
        pass  # "100-й Километр  = Километр 100-й"
    else:
        errors = True
        print(f"\n OFFNAME [{response_body[testindex]['OFFNAME']}]  "
              f"HE найден в RELNAME [{response_body[testindex]['RELNAME']}]",
              end="")

    assert str(response_body[testindex]["RELNAME"]).find(",") != 0
    assert elapsed_time <= response_time
    assert str(type(response_body[0])) == "<class 'dict'>"
    assert not errors

