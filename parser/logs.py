import logging
import os
from logging import handlers


LOG_DIR = 'logs'
log_format = logging.Formatter('%(asctime)s %(module)s %(levelname)s %(message)s')
handler = handlers.TimedRotatingFileHandler(filename=os.path.join(LOG_DIR, 'xml.log'),
                                            when='D',
                                            interval=1,
                                            backupCount=6)
handler.setFormatter(log_format)
logger = logging.getLogger('xml')
logger.setLevel(logging.INFO)
logger.addHandler(handler)
