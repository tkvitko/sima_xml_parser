from parser.logs import logger
from parser.tools import create_cats_dict


def parse_filtered(filename):
    # cats_dict = create_cats_dict()
    res = list()

    logger.info(f'Start parsing data from {filename}')
    try:
        with open(filename, encoding='utf-8') as f:
            for line in f.readlines()[1:]:
                line = line.strip()
                if '<url>' in line:
                    id = line.split('/')[-3]
                    item = {'_id': id}
                elif '<price>' in line:
                    price = line.split('>')[1].split('<')[0]
                    item['price'] = float(price)
                # elif '<categoryId>' in line:
                #     cat_id = line.split('>')[1].split('<')[0]
                #     item['cat'] = cats_dict[cat_id]

                if 'price' in item.keys():
                    res.append(item)
        logger.info(f'End parsing data from {filename}')
        return res

    except Exception as e:
        logger.error(f'Cant parse data from {filename} in {line}: {e} - {e.__class__.__name__}')
