import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s')

file_handler = logging.FileHandler('logging.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
