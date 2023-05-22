import vertica_python
import time
import uuid
from faker import Faker


connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}


def gen_data(row: int, iterate: int):
    block = []
    fake = Faker()
    event_time = fake.date_time()

    for i in range(row * iterate):
        viewed_frame = fake.random_int(min=10, max=10)

        block.append((str(uuid.uuid4()),
                      str(uuid.uuid4()),
                      str(uuid.uuid4()),
                      viewed_frame,
                      event_time))

        if len(block) == row:
            yield block
            block = []
            event_time = fake.date_time()


if __name__ == "__main__":
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE views (
            id UUID,
            user_id UUID,
            movie_id UUID,
            viewed_frame INTEGER NOT NULL,
            event_time TIMESTAMP NOT NULL
        );
        """)

        # Check insert time for 10 000 000
        print('start insert')
        start = time.time()

        for i in gen_data(1000, 10000):
            cursor.executemany(
                """INSERT INTO views """
                """(id, user_id, movie_id, viewed_frame, event_time) """
                """VALUES(%s, %s, %s, %s, %s)""",
                i)

        result_insert = time.time() - start
        print(f'Total time INSERT: {result_insert}')

        # Check select time for 100
        limit = 100
        selected = [str(i[0]) for i in cursor.execute(f"SELECT user_id FROM views LIMIT {limit}").iterate()]

        print('start select')
        start = time.time()
        for i in selected:
            cursor.execute(f"SELECT * FROM views WHERE user_id='{i}'")

        result_select = time.time() - start
        print(f'Total time SELECT: {result_select}')
