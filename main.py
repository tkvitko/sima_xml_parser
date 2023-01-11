from parser.constants import WORK_DIR
from parser.excel import create_xlsx
from parser.parser import parse_filtered
from parser.tools import *

if __name__ == '__main__':
    url = read_url_from_file(os.path.join(WORK_DIR, SOURCE_FILENAME))

    if url:
        # download_xml(url=url, dir=WORK_DIR)
        convert_xml(dir=WORK_DIR)
        res = parse_filtered(os.path.join(WORK_DIR, FILTERED_FILENAME))

        if res:
            create_xlsx(res, os.path.join(WORK_DIR, RESULT_FILENAME))
