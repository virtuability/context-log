from context_log import ContextLog


def sub_module_function():
    ContextLog.put_request_id('modulexyz')
