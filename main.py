import configparser

from parser.constants import WORK_DIR
from parser.excel import create_xlsx
from parser.mongo_cache import all_products_from_cache, add_products_to_cache, add_product_to_cache
from parser.parser import parse_filtered
from parser.sima_api import get_sima_bearer, get_product_by_article, get_sima_object_name_by_id
from parser.tools import *


def get_product_data_from_sima(product_id, bearer):
    product_data = get_product_by_article(product_id, bearer)
    product_data['country_id'] = get_sima_object_name_by_id(product_data['country_id'],
                                                            'country', bearer)
    product_data['trademark_id'] = get_sima_object_name_by_id(product_data['trademark_id'],
                                                              'trademark', bearer)
    return product_data


def check_if_price_changed_enough(product):
    config = configparser.ConfigParser()
    config.read("config.ini")
    percent = int(config['sima']['percent_price_changed'])

    new_price = product['price']
    try:
        old_price = old_products[product['_id']]

        # если нашли продукт в кеше
        if new_price != old_price:
            # если цена отличается, обновляем
            add_product_to_cache(product)

        if ((new_price / old_price) <= 1 * percent / 100) or ((new_price / old_price) >= 1 / (percent / 100)):
            # если цена отличается достаточно сильно, добавляем на нотификацию
            logger.info(
                f'Product {product["_id"]} (new price {new_price}, old price {old_price}) has been added to notification')
            return old_price

        # если не достаточно сильно, не добавляем на нотификацию
        return None
    except KeyError:
        # если продукт новый, добавляем в кеш, не добавляем на нотификацию
        add_product_to_cache(product)
        return None


if __name__ == '__main__':
    url = read_url_from_file(os.path.join(WORK_DIR, SOURCE_FILENAME))

    if url:
        download_xml(url=url, dir=WORK_DIR)
        convert_xml(dir=WORK_DIR)
        new_products = parse_filtered(os.path.join(WORK_DIR, FILTERED_FILENAME))  # новые продукты

        if new_products:

            old_products = all_products_from_cache()  # продукты в кеше
            logger.info(f'Got {len(old_products)} from cache')
            changed_products = list()

            for product in new_products:
                old_price = check_if_price_changed_enough(product)
                if old_price:  # если цена изменилась достаточно
                    changed_products.append(
                        {'id': product['_id'], 'old_price': old_price})  # добавляем в список id на уведомление

            bearer = get_sima_bearer()
            data = list()
            for changed_product in changed_products:
                product_data = get_product_data_from_sima(changed_product['id'], bearer)  # получаем данные из sima по sid
                product_data['old_price'] = changed_product['old_price']
                data.append(product_data)  # добавляем в данные для уведомления
                logger.info(f'Product {changed_product["id"]} has been added to excel')

            logger.info(f'{len(new_products)} has been added/updated in cache')
            if data:
                create_xlsx(data)  # создаем excel с достаточно изменившимися ценами
