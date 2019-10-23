# Python context-log library

## About

context-log is a simple library to emit contextual information in structured logs (JSON).

It works particularly well in a Docker or Serverless (e.g. AWS Lambda) environment where a single thread executes a request and produces a response.

The library uses python threading to store contextual information that is automatically added to all subsequent logs in a `contextMap` field.

Because the library uses the Python thread local context it works across packages and modules in a given project.

The approach is loosely based on the [Log4j 2 API Thread Context](https://logging.apache.org/log4j/2.x/manual/thread-context.html).

## Usage

Structured logging can be achieved with the [python-json-logger library](https://pypi.org/project/python-json-logger/).

Simply add project dependencies to requirements.txt:

```python
python_json_logger
PyYAML
context-log
```

Add the code below to the main code module.

Add the following YAML configuration in the `resources/logging.yaml` file, which outputs JSON structured logs to `stdout`.

```yaml
version: 1
formatters:
  json:
    class:  .jsonlogger.JsonFormatter
    format: '%(asctime)s %(name)s %(levelname)s %(message)s %(filename)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: json
root:
  level: DEBUG
  handlers:
    - console
```

Use the context_log library to emit logs. Example below.

```python
import logging.config
import yaml

with open('resources/logging.yaml', 'r') as log_config_file:
  logging.config.dictConfig(yaml.safe_load(log_config_file))

from context_log import ContextLog

def handler(event, context):
    # Clear context (e.g. re-use) and get logger
    log = ContextLog.get_logger('handler', True)
    log.info('start')

    ContextLog.put('ip', '1.2.3.4')

    # Helper to add start time in ISO and epoch time
    ContextLog.put_request_start_time()

    # Process request
    sleep(0.1)

    # Helper to add end time in ISO and epoch time
    # as well as duration in milliseconds
    ContextLog.put_request_end_time()

    log.info('end')
```

First log info event:

```json
{
    "asctime": "2019-09-19 11:53:20,479",
    "name": "handler",
    "levelname": "INFO",
    "message": "start",
    "filename": "test_example.py",
    "contextMap": {}
}
```

Second log info event:

```json
{
  "asctime": "2019-09-19 11:53:20,580",
  "name": "handler",
  "levelname": "INFO",
  "message": "end",
  "filename": "test_example.py",
  "contextMap": {
      "ip": "1.2.3.4",
      "start-time": "2019-09-19T11:53:20.480085",
      "epoch-start-time": 1568890400.480085,
      "end-time": "2019-09-19T11:53:20.580513",
      "epoch-end-time": 1568890400.580513,
      "duration": 100.428}
}
```

## The Detail

The standard logger is wrapped by a `LoggerAdapter`. It is therefore imperative that the `ContextLog.get_logger(name='<name>', clear=True|False)` call is made to get the logger to emit contextual logs.

Use `clear=True` when starting a new request in order to clear the previous context if the thread is re-used. This is typically the case in thread pools and in AWS Lambda's.

To manipulate or retrieve the `contextMap` use the following methods:

* `clear()`
* `put(key, value)`
* `get(key)`
* `get_map()`

There are also a number of helpers in an attempt to standardise log output `contextMap` fields:

* `put_request_id(request_id)`
* `put_request_method(request_method)`
* `put_request_path(request_path)`
* `put_response_status(response_status)`
* `put_start_time()`
* `put_end_time()`
* `put_request_user_id(request_user_id)`
* `put_request_client_id(request_client_id)`
* `put_request_primary_ip(primary_ip)`
* `put_request_client_ip(client_ip)`
* `put_request_viewer_country(viewer_country)`
* `put_trigger_source(trigger_source)`

## Contributing

Pull requests are more than welcome.

## Running pytest

Create virtualenv, download dependencies and run tests:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r tests/requirements.txt
pip3 install -e .
pytest

# Clean up local development installation
rm -rf context_log.egg-info
```

## Running tox

```bash
pip3 install --user --upgrade tox
tox
```

## Releasing library to PyPI

Short version from the [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/) site.

Install the release tools:

```bash
python3 -m pip install --user --upgrade setuptools wheel twine
```

Remove old distribution(s):

```bash
rm -rf dist/
```

Build the context-log package:

```bash
python3 setup.py sdist bdist_wheel
```

Upload context-log first to Test PyPI:

```bash
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Test that uploaded package is functional:

```bash
python3 -m venv .vdist
source .vdist/bin/activate
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps context-log

# Do test
python3
from context_log import ContextLog
exit()
```

Upload context-log to Live PyPI:

```bash
python3 -m twine upload dist/*
```
