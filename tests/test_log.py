"""
ContextLog tests
"""


import logging
import json
from io import StringIO
from time import sleep
import pytest
from pythonjsonlogger import jsonlogger

from context_log import ContextLog

from sub_module import sub_module_function

# Set-up logger with JSON formatting and a String IO buffer
# that can be used to compare with expected output
LOG_STREAM = StringIO()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOG_HANDLER = logging.StreamHandler(stream=LOG_STREAM)
LOG_FORMATTER = jsonlogger.JsonFormatter()
LOG_HANDLER.setFormatter(LOG_FORMATTER)
LOGGER.addHandler(LOG_HANDLER)


def test_premature_put():
    LOG_STREAM.truncate(0)
    LOG_STREAM.seek(0)
    ContextLog.clear()
    with pytest.raises(RuntimeError) as excinfo:
        ContextLog.put_request_id('xyz')
    assert "Don't call put before get_logger!" in str(excinfo.value)


def test_premature_get():
    LOG_STREAM.truncate(0)
    LOG_STREAM.seek(0)
    ContextLog.clear()
    with pytest.raises(RuntimeError) as excinfo:
        ContextLog.get('xyz')
    assert "Don't call get before get_logger!" in str(excinfo.value)


def test_premature_get_map():
    LOG_STREAM.truncate(0)
    LOG_STREAM.seek(0)
    ContextLog.clear()
    with pytest.raises(RuntimeError) as ex:
        ContextLog.get_map()
    assert "Don't call get_map before get_logger!" in str(ex.value)


def test_thread_context():
    LOG_STREAM.truncate(0)
    LOG_STREAM.seek(0)
    log = ContextLog.get_logger('test_thread_context', True)

    ContextLog.put_start_time()
    sleep(0.1)  # Short delay to test for sane duration range
    ContextLog.put('arbitrary', 'value')
    ContextLog.put_request_id('xyz')
    ContextLog.put_request_method('POST')
    ContextLog.put_request_path('/arbitrary')
    ContextLog.put_response_status('200')
    ContextLog.put_end_time()
    ContextLog.put_request_user_id('myuser')
    ContextLog.put_request_client_id('clientid')
    ContextLog.put_request_primary_ip('5.3.2.1')
    ContextLog.put_request_client_ip('1.2.3.5')
    ContextLog.put_request_viewer_country('dk')
    ContextLog.put_trigger_source('Event')

    log.debug('thread_context')
    entry = json.loads(LOG_STREAM.getvalue())
    assert entry['message'] == 'thread_context'
    assert 'contextMap' in entry
    assert entry['contextMap']['arbitrary'] == 'value'
    assert entry['contextMap']['request-id'] == 'xyz'
    assert entry['contextMap']['request-method'] == 'POST'
    assert entry['contextMap']['request-path'] == '/arbitrary'
    assert entry['contextMap']['response-status'] == '200'
    assert entry['contextMap']['start-time']
    assert entry['contextMap']['epoch-start-time']
    assert entry['contextMap']['end-time']
    assert entry['contextMap']['epoch-end-time']
    assert 100 <= entry['contextMap']['duration'] <= 500
    assert entry['contextMap']['user-id'] == 'myuser'
    assert entry['contextMap']['client-id'] == 'clientid'
    assert entry['contextMap']['primary-ip'] == '5.3.2.1'
    assert entry['contextMap']['client-ip'] == '1.2.3.5'
    assert entry['contextMap']['viewer-country'] == 'dk'
    assert entry['contextMap']['trigger-source'] == 'Event'

    assert ContextLog.get('trigger-source') == 'Event'

    assert ContextLog.get_map()


def sub_function():
    ContextLog.put_request_id('xyz123')


def test_sub_function():
    LOG_STREAM.truncate(0)
    LOG_STREAM.seek(0)
    log = ContextLog.get_logger('test_sub_function', True)
    sub_function()
    log.info('sub_function')
    entry = json.loads(LOG_STREAM.getvalue())
    assert entry['message'] == 'sub_function'
    assert 'contextMap' in entry
    assert entry['contextMap']['request-id'] == 'xyz123'


def test_sub_module():
    LOG_STREAM.truncate(0)
    LOG_STREAM.seek(0)
    log = ContextLog.get_logger('test_sub_module', True)
    sub_module_function()
    log.info('sub_module_function')
    entry = json.loads(LOG_STREAM.getvalue())
    assert entry['message'] == 'sub_module_function'
    assert 'contextMap' in entry
    assert entry['contextMap']['request-id'] == 'modulexyz'
