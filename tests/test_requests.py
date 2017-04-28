import pytest
import sys

from request_manager import request
from request_manager.exceptions import (
    MaxRetriesExceeded,
    HTTPMethodNotFound
)

if sys.version_info.major == 2:
    from mock import patch, MagicMock, Mock
else:
    from unittest.mock import patch, MagicMock, Mock


@patch('requests.get')
def test_get(mocked_get):
    """Test GET request."""
    mocked_get.return_value = MagicMock(status_code=200, text='{}')
    request.get(url='blabla')
    assert mocked_get.called


@patch('requests.post')
def test_post(mocked_post):
    """Test POST request."""
    mocked_post.return_value = MagicMock(status_code=200, text='{}')
    request.post(url='blabla')
    assert mocked_post.called


@patch('requests.put')
def test_put(mocked_put):
    """Test PUT request."""
    mocked_put.return_value = MagicMock(status_code=200, text='{}')
    request.put(url='blabla')
    assert mocked_put.called


@patch('requests.patch')
def test_patch(mocked_patch):
    """Test PATCH request."""
    mocked_patch.return_value = MagicMock(status_code=200, text='{}')
    request.patch(url='blabla')
    assert mocked_patch.called


@patch('requests.get')
def test_execute_invalid_method(mocked_get):
    """Test invalid Method."""
    mocked_get.return_value = MagicMock(status_code=200, text='{}')

    with pytest.raises(HTTPMethodNotFound):
        request.execute(
            max_retries=4,
            retry_interval=0,
            url='blabla',
            method='BLA'
        )

    assert not mocked_get.called


@patch('requests.get')
def test_execute_retry(mocked_get):
    """Test request retry."""
    mocked_get.side_effect = Mock(side_effect=[
        MagicMock(status_code=500, text=''),
        MagicMock(status_code=200, text='{}')
    ])

    response = request.execute(
        max_retries=4,
        retry_interval=0,
        url='blabla',
        method='GET'
    )

    assert response.status_code == 200
    assert response.text == '{}'
    assert mocked_get.call_count == 2


@patch('requests.get')
def test_execute_retry_max_exceeded(mocked_get):
    """Test request max retry exceeded."""
    mocked_get.return_value = MagicMock(status_code=500, text='')

    with pytest.raises(MaxRetriesExceeded):
        request.execute(
            max_retries=4,
            retry_interval=0,
            url='blabla',
            method='GET'
        )

    assert mocked_get.call_count == 4


@patch('time.sleep')
@patch('requests.get')
def test_execute_retry_with_interval(mocked_get, mocked_sleep):
    """Test request retry with time sleep."""
    mocked_sleep.return_value = None
    mocked_get.return_value = MagicMock(status_code=500, text='')

    with pytest.raises(MaxRetriesExceeded):
        request.execute(
            max_retries=1,
            retry_interval=2,
            url='blabla',
            method='GET'
        )

    assert mocked_get.call_count == 1
    assert mocked_sleep.call_count == 1

    mocked_sleep.assert_called_with(2.0)


@patch('time.sleep')
@patch('requests.get')
def test_execute_retry_without_interval(mocked_get, mocked_sleep):
    """Test request retry without time sleep."""
    mocked_sleep.return_value = None
    mocked_get.return_value = MagicMock(status_code=500, text='')

    with pytest.raises(MaxRetriesExceeded):
        request.execute(
            max_retries=1,
            retry_interval=0,
            url='blabla',
            method='GET'
        )

    assert mocked_get.call_count == 1
    assert not mocked_sleep.called
