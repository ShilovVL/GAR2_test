from secret import SECRET
from sshtunnel import SSHTunnelForwarder
import psycopg2

# response_time = 20.00  # Максимальное время ответа, не считающееся ошибкой (сек)
# limit_tests = 100
# sql_string = "select objectguid, typename, name from addrobj where isactual = '1'  and isactive = '0' ORDER BY random() LIMIT " + str(
#     limit_tests)


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
            # SQL request for /street method

            curs.execute(sql_string)
            rows = curs.fetchall()

            for y in rows:
                data_for_test.append(y)

            server.stop()
            return data_for_test

    except:
        print("Fail connection")


# print(get_data_for_test(sql_string))