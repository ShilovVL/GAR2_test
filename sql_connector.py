from secret import SECRET
from sshtunnel import SSHTunnelForwarder
import psycopg2
from random import randint
from sql_strings import sql_strings


def get_data_for_test(sql_string):
    try:
        with SSHTunnelForwarder(
                ('195.19.108.146', 22),
                ssh_username=SECRET.DATABASE_USER,
                ssh_password=SECRET.DATABASE_PASSWORD,
                remote_bind_address=('192.168.14.6', 5432)) as server:

            server.start()

            print("Use local port:", server.local_bind_port)  # show assigned local port
            # work with `SECRET SERVICE` through `server.local_bind_port`.
            params = {
                'database': "gar",
                'user': SECRET.DATABASE_USER,
                'password': SECRET.DATABASE_PASSWORD,
                'host': 'localhost',
                'port': server.local_bind_port
            }
            conn = psycopg2.connect(**params)
            curs = conn.cursor()

            data_for_test = []
            # print(sql_string)
            curs.execute(sql_string)
            rows = curs.fetchall()

            for y in rows:
                data_for_test.append(y)

            server.stop()
            return data_for_test

    except:
        print("Fail connection")


def get_data_for_test_regions(sql_string, number_regions=30, limit_for_region=20):
    try:
        with SSHTunnelForwarder(
                ('195.19.108.146', 22),
                ssh_username=SECRET.DATABASE_USER,
                ssh_password=SECRET.DATABASE_PASSWORD,
                remote_bind_address=('192.168.14.6', 5432)) as server:
            # '192.168.249.13'
            server.start()

            print("Use local port:", server.local_bind_port)  # show assigned local port
            # work with `SECRET SERVICE` through `server.local_bind_port`.
            params = {
                'database': "gar",
                'user': SECRET.DATABASE_USER,
                'password': SECRET.DATABASE_PASSWORD,
                'host': 'localhost',
                'port': server.local_bind_port
            }
            conn = psycopg2.connect(**params)
            curs = conn.cursor()

            sql_regions = "select regioncode from adm_objects_registry where level in (1)"  # get regions list
            curs.execute(sql_regions)
            all_regions_rf = curs.fetchall()

            allregions_normal = []
            for i in all_regions_rf:
                for y in i:
                    allregions_normal.append(y)
            regions_for_test = ["77", "78", "75", "99", "74"]  # Регионы, обязательные к проверке
            while len(regions_for_test) < number_regions:  # Дополнение списка проверяемых до 10 регионов случайными
                add_region = str(randint(1, len(allregions_normal)))
                regions_for_test.append(add_region)
                regions_for_test = list(set(regions_for_test))  # убрать повторы

            data_for_test = []
            for i in regions_for_test:
                test_sql_string = sql_string + f"'{i}' limit '{limit_for_region}'"
                # print(test_sql_string)
                curs.execute(test_sql_string)
                rows = curs.fetchall()
                for y in rows:
                    data_for_test.append(y)

            server.stop()
            return data_for_test

    except:
        print("Fail connection")


def get_data_for_test_regions_big(sql_string1, sql_string2, number_regions=30, limit_for_region=20):
    try:
        with SSHTunnelForwarder(
                ('195.19.108.146', 22),
                ssh_username=SECRET.DATABASE_USER,
                ssh_password=SECRET.DATABASE_PASSWORD,
                remote_bind_address=('192.168.14.6', 5432)) as server:
            # '192.168.249.13'
            server.start()

            print("Use local port:", server.local_bind_port)  # show assigned local port
            # work with `SECRET SERVICE` through `server.local_bind_port`.
            params = {
                'database': "gar",
                'user': SECRET.DATABASE_USER,
                'password': SECRET.DATABASE_PASSWORD,
                'host': 'localhost',
                'port': server.local_bind_port
            }
            conn = psycopg2.connect(**params)
            curs = conn.cursor()

            sql_regions = "select regioncode from adm_objects_registry where level in (1)"  # get regions list
            curs.execute(sql_regions)
            all_regions_rf = curs.fetchall()

            allregions_normal = []
            for i in all_regions_rf:
                for y in i:
                    allregions_normal.append(y)
            regions_for_test = ["77", "78", "75", "99", "74"]  # Регионы, обязательные к проверке
            while len(regions_for_test) < number_regions:
                add_region = str(randint(1, len(allregions_normal)))
                regions_for_test.append(add_region)
                regions_for_test = list(set(regions_for_test))  # убрать повторы

            data_for_test = []
            for i in regions_for_test:

                test_sql_string = sql_string1 + "'" + str(i) + "'" + sql_string2 + str(limit_for_region)
                # print(test_sql_string)
                curs.execute(test_sql_string)
                rows = curs.fetchall()
                for y in rows:
                    data_for_test.append(y)

            server.stop()
            return data_for_test

    except:
        print("Fail connection")


def get_data_for_test_search(sql_string1, sql_string2, number_regions=30, limit_for_region=20):
    try:
        with SSHTunnelForwarder(
                ('195.19.108.146', 22),
                ssh_username=SECRET.DATABASE_USER,
                ssh_password=SECRET.DATABASE_PASSWORD,
                remote_bind_address=('192.168.14.6', 5432)) as server:
            # '192.168.249.13'
            server.start()

            print("Use local port:", server.local_bind_port)  # show assigned local port
            # work with `SECRET SERVICE` through `server.local_bind_port`.
            params = {
                'database': "gar",
                'user': SECRET.DATABASE_USER,
                'password': SECRET.DATABASE_PASSWORD,
                'host': 'localhost',
                'port': server.local_bind_port
            }
            conn = psycopg2.connect(**params)
            curs = conn.cursor()

            sql_regions = "select regioncode from adm_objects_registry where level in (1)"  # get regions list
            curs.execute(sql_regions)
            all_regions_rf = curs.fetchall()

            allregions_normal = []
            for ii in all_regions_rf:
                for y in ii:
                    allregions_normal.append(y)
            regions_for_test = ["77", "78", "75", "99", "74"]  # Регионы, обязательные к проверке
            while len(
                    regions_for_test) < number_regions:  # Дополнение списка проверяемых до numbers_regions регионов случайными
                add_region = str(randint(1, len(allregions_normal)))
                regions_for_test.append(add_region)
                regions_for_test = list(set(regions_for_test))  # убрать повторы

            data_for_test = []
            number_region = 0
            parents = []
            for ii in regions_for_test:

                # SQL request for /street method
                test_sql_string = sql_string1 + "'" + str(ii) + "' limit " + str(limit_for_region)
                curs.execute(test_sql_string)
                rows = curs.fetchall()

                for row in rows:
                    # отдельный запрос для получения имени родителя. Списком было бы быстрее, но Postgres удаляет
                    # повторы в ответе и теряется связь
                    sql_string_parent = sql_string2 + str(row[4])
                    curs.execute(sql_string_parent)
                    parent_name = curs.fetchall()
                    parents.append(parent_name[0][0])
                    row = list(row)
                    row.append(parent_name[0][0])
                    data_for_test.append(row)  # Основной список для тестирования

            server.stop()
            return data_for_test

    except:
        print("Fail connection")


# print(sql_strings["test_house_search"]["sql_request"])
# print(get_data_for_test(sql_string))

# print(len(get_data_for_test(sql_strings["test_house_search"]["sql_request"] + sql_strings["test_house_search"]["limit"])))
# print(len(get_data_for_test_regions(sql_strings["test_house_search"]["sql_request"], 50, 100)))
# print(get_data_for_test_regions_big(sql_strings["test_find_addrobject_housecount"]["sql_request_1"], sql_strings["test_find_addrobject_housecount"]["sql_request_2"]))
# print(get_data_for_test_search(sql_strings["test_search"]["sql_request_1"],sql_strings["test_search"]["sql_request_2"]))
