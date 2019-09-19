"""
ContextLog implementation that retains context for a given
thread
"""

from datetime import datetime
from threading import local
import logging

LOCAL = local()


class ContextLog:
    """
    ContextLog class
    """

    @staticmethod
    def clear():
        """
        Fully clear the context map from local
        """
        if hasattr(LOCAL, 'context_map'):
            delattr(LOCAL, 'context_map')

    @staticmethod
    def put(key, value):
        """
        Put stuff on the local thread's context map

        Generic call to set any key or value pair.
        """

        if hasattr(LOCAL, 'context_map'):
            context_map = LOCAL.context_map
        else:
            raise RuntimeError("Don't call put before get_logger!")

        context_map[key] = value

    @staticmethod
    def get(key):
        """
        Get key value from the local thread's context map

        Generic call to get any key value.
        """

        if hasattr(LOCAL, 'context_map'):
            context_map = LOCAL.context_map
        else:
            raise RuntimeError("Don't call get before get_logger!")

        if key in context_map:
            return context_map[key]

        return None

    @staticmethod
    def get_map():
        """
        Get the full context map from the local thread

        Generic call to get any key value.
        """

        if hasattr(LOCAL, 'context_map'):
            context_map = LOCAL.context_map
        else:
            raise RuntimeError("Don't call get_map before get_logger!")

        return context_map

    @staticmethod
    def put_request_id(request_id):
        """
        Put request-id on the contextMap

        Typically this is a request id assigned by an upstream service
        like a load balancer or content delivery network.
        """
        ContextLog.put('request-id', request_id)

    @staticmethod
    def put_request_method(request_method):
        """
        Put request-method on the contextMap

        Typically this is the HTTP method, e.g. GET, POST, PUT, DELETE etc.
        """
        ContextLog.put('request-method', request_method)

    @staticmethod
    def put_request_path(request_path):
        """
        Put request-path on the contextMap

        Typically this is the HTTP request path, e.g. /my/webservice.
        """
        ContextLog.put('request-path', request_path)

    @staticmethod
    def put_response_status(response_status):
        """
        Put response-status on the contextMap

        Typically this is the HTTP response status code, e.g. 200, 4xx or 5xx.
        """
        ContextLog.put('response-status', response_status)

    @staticmethod
    def put_start_time():
        """
        Put start-time on the contextMap

        Adds the start-time in ISO and epoch-time formats.
        """
        now = datetime.now()
        isonow = now.isoformat()
        ContextLog.put('start-time', isonow)
        epochnow = now.timestamp()
        ContextLog.put('epoch-start-time', epochnow)

    @staticmethod
    def put_end_time():
        """
        Put end-time on the contextMap

        Adds the end-time in ISO and epoch-time formats. If start time
        is set then it also adds duration.
        """
        now = datetime.now()
        isonow = now.isoformat()
        ContextLog.put('end-time', isonow)
        epochnow = now.timestamp()
        ContextLog.put('epoch-end-time', epochnow)

        epoch_start_time = ContextLog.get('epoch-start-time')
        if epoch_start_time:
            duration = round((epochnow - epoch_start_time) * 1000, 3)
            ContextLog.put('duration', duration)

    @staticmethod
    def put_request_user_id(request_user_id):
        """
        Put user-id on the contextMap

        Typically this is the user id of the end-user.
        """
        ContextLog.put('user-id', request_user_id)

    @staticmethod
    def put_request_client_id(request_client_id):
        """
        Put client-id on the contextMap

        Typically this is the OAuth client id of the calling client
        """
        ContextLog.put('client-id', request_client_id)

    @staticmethod
    def put_request_primary_ip(primary_ip):
        """
        Put primary-ip on the contextMap

        Typically this is the ip address of the processing host, container
        or Lambda.
        """
        ContextLog.put('primary-ip', primary_ip)

    @staticmethod
    def put_request_client_ip(client_ip):
        """
        Put client-ip on the contextMap

        Typically this is the IP of the client, e.g. system that web browser
        runs on.
        """
        ContextLog.put('client-ip', client_ip)

    @staticmethod
    def put_request_viewer_country(viewer_country):
        """
        Put viewer-country on the contextMap

        Typically this is the
        [ISO 3166 alpha-2 2-letter code]
        (https://www.iso.org/iso-3166-country-codes.html)
        designating the client's (viewer) country.
        """
        ContextLog.put('viewer-country', viewer_country)

    @staticmethod
    def put_trigger_source(trigger_source):
        """
        Put trigger-source on the contextMap
        """
        ContextLog.put('trigger-source', trigger_source)

    @staticmethod
    def get_logger(name, clear=False):
        """
        Get the named logger with LoggerAdapter wrapped around, which adds
        extra info that points at the context_map dict.

        Irrespective of the number of created loggers the context_map dict
        remains the same in a given thread.

        If clear=True, clear context (map)
        """

        if clear:
            ContextLog.clear()

        if hasattr(LOCAL, 'context_map'):
            context_map = LOCAL.context_map
        else:
            context_map = dict()
            LOCAL.context_map = context_map

        logger = logging.LoggerAdapter(
            logging.getLogger(name),
            extra={'contextMap': context_map}
        )

        return logger
