"""
https://www.sima-land.ru/api/v5/help/#operations-tag-item
"""

import configparser

import requests
from requests import ConnectTimeout, ReadTimeout

from parser.logs import logger

BASE_URL = 'https://www.sima-land.ru/api/v5/'
EKATERINBURG_ID = 27503892

config = configparser.ConfigParser()
config.read("config.ini")
email = config['sima']['email']
password = config['sima']['password']


def get_sima_bearer():
    request_url = 'https://www.sima-land.ru/api/v5/signin'
    request_body = {
        'email': email,
        'password': password,
        'regulation': True
    }
    request_params = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.goa.error'
    }

    answer = requests.post(url=request_url,
                           json=request_body,
                           params=request_params)

    bearer = answer.headers['authorization']

    return bearer.split(' ')[1]


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def get_product_by_article(sid, bearer):
    # getting product from sima by sid (=offer_id from ozon)

    request_url = f'{BASE_URL}item/{sid}?by_sid=true'

    count = 0
    max_count = 10
    answered = False

    while not answered and count < max_count:

        try:
            response = requests.get(request_url, auth=BearerAuth(bearer), timeout=30)
            answered = True

            if response.status_code == 200:
                response_obj = response.json()

                logger.info(f'Got sima product by sid {sid}')
                return response_obj

            else:
                logger.warning('Cant get product by sid {} from sima: {}'.format(sid, response.status_code))

        except (ConnectTimeout, ReadTimeout):
            logger.error(f'Timeout connecting to sima ({sid}), will try again ({count}/{max_count})')
            count += 1
        except Exception as e:
            logger.error(f'{e} connecting to sima ({sid}), will try again ({count}/{max_count})')
            count += 1


def get_sima_object_name_by_id(id, object_type: str, bearer):
    request_url = f'{BASE_URL}{object_type}/{id}'
    response = requests.get(request_url, auth=BearerAuth(bearer), timeout=30)
    if response.status_code == 200:
        response_obj = response.json()
        return response_obj['name']


if __name__ == '__main__':
    BEARER = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjY5NzAyMDMsImlhdCI6MTY2NjM2NTQwMywianRpIjo0MTExMTA4LCJuYmYiOjE2NjYzNjU0MDN9.Y8x6Ot0QnrbLTluszW7qAK9qdX-5NnL_JWzNyRoerEI'
    print(get_product_by_article(528, BEARER))
    # SIMA_EMAIL = 'prostoexport@gmail.com'
    # SIMA_PASSWORD = 'LG#V!hM3>h-bB274,%JLGH?2'
    # print(get_sima_bearer(SIMA_EMAIL, SIMA_PASSWORD))
