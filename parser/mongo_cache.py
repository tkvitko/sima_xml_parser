from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('mongodb://localhost:27017/')
db = client.sima


def add_product_to_cache(product: dict):
    db.products.update_one({'_id': product['_id']}, {"$set": product}, upsert=True)


def add_products_to_cache(products: list):
    for product in products:
        add_product_to_cache(product)


def find_product_in_cache(product_id):
    return db.products.find_one({'_id': product_id})


def all_products_from_cache():
    return {product['_id']: product['price'] for product in db.products.find()}


if __name__ == '__main__':
    test_product = {'_id': 4015142, 'price': 1.0}
    test_products = [{'_id': 4015145, 'price': 100.0}, {'_id': 4015142, 'price': 1.0}]
    add_products_to_cache(test_products)
    # print(find_product_in_cache(test_product['_id']))
    # print(all_products_from_cache())
