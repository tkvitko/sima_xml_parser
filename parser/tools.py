import os
import urllib.request

from parser.constants import *
from parser.exceptions import NotFoundUrlInFile
from parser.logs import logger


def read_url_from_file(filename):
    try:
        with open(filename, encoding='utf-8') as f:
            url = f.readline().strip()
            if 'http' not in url:
                raise NotFoundUrlInFile
            logger.info(f'Got url {url} from {filename}')
            return url
    except Exception as e:
        logger.error(f'Cant get url from {filename}: {e} - {e.__class__.__name__}')


def download_xml(url, dir):
    try:
        filename = url.split('/')[-1]
        file_path = os.path.join(dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        logger.info(f'Start downloading {url} to {file_path}')
        urllib.request.urlretrieve(url, file_path)
        logger.info(f'End downloading {url} to {file_path}')

    except Exception as e:
        logger.error(f'Cant download {url}: {e} - {e.__class__.__name__}')


def convert_xml(dir):
    try:
        logger.info(f'Start filtering data to {FILTERED_FILENAME}')
        # os.system(f"egrep '(<url>|<price>|<categoryId>)' {dir}/full_no_rs.xml > {dir}/{FILTERED_FILENAME}")
        os.system(f"egrep '(<url>|<price>)' {dir}/full_no_rs.xml > {dir}/{FILTERED_FILENAME}")
        logger.info(f'End filtering data to {FILTERED_FILENAME}')

        # logger.info(f'Start filtering data to {CATEGORIES_FILENAME}')
        # os.system(f"grep 'category id=' {dir}/full_no_rs.xml > {dir}/{CATEGORIES_FILENAME}")
        # logger.info(f'End filtering data to {CATEGORIES_FILENAME}')

    except Exception as e:
        logger.error(f'Cant filter: {e} - {e.__class__.__name__}')


def create_cats_dict():
    try:
        res = dict()
        with open(os.path.join(WORK_DIR, CATEGORIES_FILENAME)) as f:
            for line in f.readlines():
                cat_id = line.split('"')[1]
                cat_name = line.split('>')[1].split('<')[0]
                res[cat_id] = cat_name
        return res
    except Exception as e:
        logger.error(f'Cant create categories map: {e} - {e.__class__.__name__}')
