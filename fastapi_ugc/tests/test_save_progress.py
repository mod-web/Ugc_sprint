import requests
from datetime import datetime
from conftest import HOST, USER_ID, FILM_ID, VIEWED_FRAME


def test_save_movie_progress():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = f'{HOST}/api/v1/save'
    data = {
            'user_id': USER_ID,
            'film_id': FILM_ID,
            'viewed_frame': VIEWED_FRAME,
            'message_time': str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')),
        }
    response = requests.post(url=url,
                             json=data,
                             headers=headers
                             )
    assert response.status_code == 200
