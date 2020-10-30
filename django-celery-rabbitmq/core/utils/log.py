import logging

test_logger = logging.getLogger('test')


def write_log(msg):
    test_logger.info(msg)
