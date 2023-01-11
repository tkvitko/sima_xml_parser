import os

import xlsxwriter

from parser.logs import logger


def create_xlsx(source, full_path):
    if os.path.exists(full_path):
        os.remove(full_path)

    logger.info(f'Start creating xlsx {full_path}')
    try:

        with xlsxwriter.Workbook(full_path) as workbook:
            num_fmt = workbook.add_format({'num_format': '#,###'})
            worksheet = workbook.add_worksheet()

            # Write headers
            i = 0
            for key in source[0]:
                worksheet.write(0, i, key)
                i += 1

            # Write dict data
            row = 1
            for item in source:
                column = 0
                for value in item.values():
                    if isinstance(value, float):
                        worksheet.write(row, column, value, num_fmt)
                    else:
                        worksheet.write(row, column, value)
                    column += 1
                row += 1

        logger.info(f'Start creating xlsx {full_path}')

    except Exception as e:
        logger.error(f'Cant create xlsx {full_path}: {e} - {e.__class__.__name__}')
