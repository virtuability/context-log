
import logging.config
import yaml

with open('tests/resources/logging.yaml', 'r') as log_config_file:
  logging.config.dictConfig(yaml.safe_load(log_config_file))

from context_log import ContextLog
from time import sleep

def test_handler():
    # Clear context (e.g. re-use) and get logger
    log = ContextLog.get_logger('handler', True)
    log.info('start')

    ContextLog.put('ip', '1.2.3.4')

    # Helper to add start time in ISO and epoch time
    ContextLog.put_start_time()

    # Process request
    sleep(0.1)

    # Helper to add end time in ISO and epoch time
    # as well as duration in milliseconds
    ContextLog.put_end_time()

    log.info('end')

