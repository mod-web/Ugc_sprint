import time
import uuid
from faker import Faker
from clickhouse_driver import Client


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
    client = Client(host="localhost")
    client.execute("CREATE DATABASE IF NOT EXISTS views")

    create_sql = """
    CREATE TABLE IF NOT EXISTS views.frame (
          id UUID,
          user_id UUID,
          movie_id UUID,
          viewed_frame Int32,
          event_time DateTime('Europe/Moscow'))
          Engine=MergeTree() PARTITION BY toYYYYMMDD(event_time) ORDER BY user_id;
    """
    client.execute(create_sql)

    # Check insert time for 10 000 000
    print('start insert')
    start = time.time()

    for i in gen_data(1000, 10000):
        client.execute(
            "INSERT INTO views.frame (id, user_id, movie_id, viewed_frame, event_time) VALUES",
            i,
        )

    result_insert = time.time() - start
    print(f'Total time INSERT: {result_insert}')   # Total time: 375.81954884529114

    # Check select time for 100
    limit = 100
    selected = [str(i[0]) for i in client.execute(f"SELECT user_id FROM views.frame LIMIT {limit}")]

    print('start select')
    start = time.time()
    for i in selected:
        client.execute(f"SELECT * FROM views.frame WHERE user_id='{i}'")

    result_select = time.time() - start
    print(f'Total time SELECT: {result_select}')    # Total time SELECT(100): 45.223976373672485
