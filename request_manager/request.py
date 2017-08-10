import logging
import time

import requests

from .exceptions import (
    MaxRetriesExceeded,
    HTTPMethodNotFound
)

logger = logging.getLogger('requests')

MAX_RETRIES = 5
RETRY_INTERVAL = 1


def get_method_function(method):
    try:
        return getattr(requests, method.lower())
    except AttributeError:
        raise HTTPMethodNotFound()


def execute(
    method,
    max_retries,
    retry_interval,
    use_retry=True,
    *args,
    **kwargs
):
    """Execute HTTP request with retry support.

    Args:
        method (string): HTTP verb.
        use_retry (bool): If True, will use retry
            configuration (default: True).
        max_retries (int): Max of request re-execution
            if error occurred (default: 5).
        retry_interval (int): Interval to re-execute requests
            if error occurred (default: 0).
    Returns:
        int, string: Request response status code and content.
    Raises:
        Exception: If max retries exceeded.
    """
    method = get_method_function(method=method)

    _max_retries = max_retries if use_retry else 1

    while _max_retries:
        try:
            response = method(*args, **kwargs)

            if not str(response.status_code).startswith('50'):
                return response

        except Exception as e:
            logger.exception(e)

        if use_retry and retry_interval:
            time.sleep(float(retry_interval))

        _max_retries -= 1

    logger.error('Max request retries exceeded')

    raise MaxRetriesExceeded()


def get(
    max_retries=MAX_RETRIES,
    retry_interval=RETRY_INTERVAL,
    *args,
    **kwargs
):
    return execute(
        method='GET',
        max_retries=max_retries,
        retry_interval=retry_interval,
        *args,
        **kwargs
    )


def post(
    max_retries=MAX_RETRIES,
    retry_interval=RETRY_INTERVAL,
    *args,
    **kwargs
):
    return execute(
        method='POST',
        max_retries=max_retries,
        retry_interval=retry_interval,
        *args,
        **kwargs
    )


def put(
    max_retries=MAX_RETRIES,
    retry_interval=RETRY_INTERVAL,
    *args,
    **kwargs
):
    return execute(
        method='PUT',
        max_retries=max_retries,
        retry_interval=retry_interval,
        *args,
        **kwargs
    )


def patch(
    max_retries=MAX_RETRIES,
    retry_interval=RETRY_INTERVAL,
    *args,
    **kwargs
):
    return execute(
        method='PATCH',
        max_retries=max_retries,
        retry_interval=retry_interval,
        *args,
        **kwargs
    )


def delete(
    max_retries=MAX_RETRIES,
    retry_interval=RETRY_INTERVAL,
    *args,
    **kwargs
):
    return execute(
        method='DELETE',
        max_retries=max_retries,
        retry_interval=retry_interval,
        *args,
        **kwargs
    )
