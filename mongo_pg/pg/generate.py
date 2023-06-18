import uuid
from datetime import datetime
from random import choice, randint
from psycopg2.extras import execute_batch
from tqdm import tqdm
import psycopg2
from psycopg2.extras import RealDictCursor

from config import configs


dsl = {'host': configs.db.host,
       'port': configs.db.port,
       'dbname': configs.db.db,
       'user': 'app',
       'password': configs.db.password}


class PgCollection:
    def __init__(self):
        self.dsl = dsl
        self.pg_conn = psycopg2.connect(**self.dsl)
        self.batch_size = configs.db.batch_size

    def get_cursor(self):
        return self.pg_conn.cursor()

    def select(self, table, limit):
        with self.get_cursor() as cur:
            cur.execute(f'SELECT * FROM {table}')
            return [i[0] for i in cur.fetchmany(limit)]

    def insert(self, table, count):
        with self.get_cursor() as cur:
            cmd = f'INSERT INTO {table} VALUES (%s)'
            imp = [(str(uuid.uuid4()), ) for _ in range(count)]
            execute_batch(cur, cmd, imp, page_size=self.batch_size)
            self.pg_conn.commit()

    def insert_like(self, count):
        idx = str(uuid.uuid4())
        user = self.select('users', 1)[0]
        movie = self.select('movies', 1)[0]
        with self.get_cursor() as cur:
            cmd = 'INSERT INTO likes VALUES (%s, %s, %s, %s, %s, %s)'
            imp = [(idx, user, movie, randint(1, 10), datetime.now(), datetime.now()) for _ in range(count)]
            execute_batch(cur, cmd, imp, page_size=self.batch_size)
            self.pg_conn.commit()
        return idx

    def insert_likes(self, count):
        users = self.select('users', 1000)
        movies = self.select('movies', 100000)
        with self.get_cursor() as cur:
            cmd = 'INSERT INTO likes VALUES (%s, %s, %s, %s, %s, %s)'
            imp = [(str(uuid.uuid4()), choice(users), choice(movies), randint(1, 10), datetime.now(), datetime.now()) for _ in range(count)]
            execute_batch(cur, cmd, imp, page_size=self.batch_size)
            self.pg_conn.commit()

    def insert_bookmarks(self, count):
        users = self.select('users', 1000)
        movies = self.select('movies', 100000)
        with self.get_cursor() as cur:
            cmd = 'INSERT INTO bookmarks VALUES (%s, %s, %s, %s)'
            imp = [(str(uuid.uuid4()), choice(users), choice(movies), datetime.now()) for _ in range(count)]
            execute_batch(cur, cmd, imp, page_size=self.batch_size)
            self.pg_conn.commit()

    def insert_reviews(self, count):
        users = self.select('users', 1000)
        movies = self.select('movies', 100000)
        with self.get_cursor() as cur:
            cmd = 'INSERT INTO reviews VALUES (%s, %s, %s, %s, %s, %s)'
            imp = [(str(uuid.uuid4()),
                    choice(users),
                    choice(movies),
                    'Test review for movie from user',
                    datetime.now(),
                    datetime.now()
                    ) for _ in range(count)]
            execute_batch(cur, cmd, imp, page_size=self.batch_size)
            self.pg_conn.commit()


if __name__ == '__main__':
    pg = PgCollection()
    pg.insert('users', configs.db.user_count)
    pg.insert('movies', configs.db.movie_count)
    pg.insert_likes(configs.db.doc_count)
    pg.insert_bookmarks(configs.db.doc_count)
    pg.insert_reviews(configs.db.doc_count)
    print('complete generate')



#
# class MngCollection:
#     """ Cls for operation with Mongo """
#
#     def __init__(self):
#         self.dsn = configs.db.dsn
#         self.db_name = configs.db.db_name
#         self.batch_size = configs.db.batch_size
#         self.user_count = configs.db.user_count
#         self.movie_count = configs.db.movie_count
#         self.docs_count = self.user_count * 100
#         self.db = self.conn_mongo()
#         self.user_ids = [uuid.uuid4() for _ in range(self.user_count)]
#         self.movie_ids = [uuid.uuid4() for _ in range(self.movie_count)]
#
#
#
#     def create_data(self, collection):
#         match collection:  # noqa: E999
#             case 'reviews':
#                 return self.create_review()
#             case 'likes':
#                 return self.create_like()
#             case 'bookmarks':
#                 return self.create_bookmark()
#
#     def create_like(self):
#         return {'user_id': choice(self.user_ids),
#                 'movie_id': choice(self.movie_ids),
#                 'like': randint(0, 10),
#                 'created': datetime.now(),
#                 'modified': datetime.now()}
#
#     def create_review(self):
#         user_id = choice(self.user_ids)
#         movie_id = choice(self.movie_ids)
#         return {'user_id': user_id,
#                 'movie_id': movie_id,
#                 'review': f'Test review for {movie_id} from {user_id}',
#                 'created': datetime.now(),
#                 'modified': datetime.now()}
#
#     def create_bookmark(self):
#         return {'user_id': choice(self.user_ids),
#                 'movie_id': choice(self.movie_ids),
#                 'created': datetime.now()}
#
#
# if __name__ == '__main__':
#     print('Loading ..')
#     db = MngCollection()
#     lst_collection = db.get_list_collection()
#     for c in tqdm(lst_collection, desc=str(lst_collection)):
#         batch = list()
#         counter = 0
#         for i in tqdm(range(0, db.docs_count), desc=c):
#             data = db.create_data(c)
#             batch.append(data)
#             if len(batch) >= db.batch_size:
#                 try:
#                     db.get_collection(c).insert_many(batch)
#                 except Exception as e:
#                     print(f'{e.code}: {e.message}')
#                 finally:
#                     counter += db.batch_size
#                     batch.clear()
#     print('Load Complete')
