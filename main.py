import configparser

from parser.constants import WORK_DIR
from parser.excel import create_xlsx
from parser.mongo_cache import all_products_from_cache, add_products_to_cache
from parser.parser import parse_filtered
from parser.sima_api import get_sima_bearer, get_product_by_article, get_sima_object_name_by_id
from parser.tools import *


def get_product_data_from_sima(product_id, bearer):
    product_data = get_product_by_article(product_id, bearer)
    product_data['country_id'] = get_sima_object_name_by_id(product_data['country_id'], 'country',
                                                            bearer)
    product_data['trademark_id'] = get_sima_object_name_by_id(product_data['trademark_id'], 'trademark',
                                                              bearer)
    return product_data


def check_if_price_changed_enough(product):
    config = configparser.ConfigParser()
    config.read("config.ini")
    percent = int(config['sima']['percent_price_changed'])

    new_price = product['price']
    try:
        old_price = old_products[product['_id']]
        if ((new_price / old_price) <= 1 * percent / 100) or ((new_price / old_price) >= 1 / (percent / 100)):
            return True
        return False
    except KeyError:
        # haven't find product by id in cache
        return False


if __name__ == '__main__':
    url = read_url_from_file(os.path.join(WORK_DIR, SOURCE_FILENAME))

    if url:
        # download_xml(url=url, dir=WORK_DIR)
        convert_xml(dir=WORK_DIR)
        new_products = parse_filtered(os.path.join(WORK_DIR, FILTERED_FILENAME))  # новые продукты

        if new_products:

            old_products = all_products_from_cache()  # продукты в кеше
            changed_products = list()

            for product in new_products:
                if check_if_price_changed_enough(product):  # если цена изменилась достаточно
                    changed_products.append(product['_id'])  # добавляем в список id на уведомление
                    logger.info(f'Product {product["_id"]} has been added to renew from sima')

            bearer = get_sima_bearer()
            data = list()
            for product_id in changed_products:
                product_data = get_product_data_from_sima(product_id, bearer)  # получаем данные из sima по sid
                data.append(product_data)  # добавляем в данные для уведомления
                logger.info(f'Product {product_id} has been added to excel')

            add_products_to_cache(new_products)  # записываем в кеш новые данные по полученным продуктам
            logger.info(f'{len(new_products)} has been added/updated in cache')
            if data:
                create_xlsx(data)  # создаем excel с достаточно изменившимися ценами
