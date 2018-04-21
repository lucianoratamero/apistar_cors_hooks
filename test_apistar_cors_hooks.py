
from copy import deepcopy
from collections import namedtuple
from unittest.mock import patch

import wsgicors
import apistar_cors_hooks
from apistar.server import wsgi
from apistar.http import Response


FakePolicy = namedtuple('Policy', ['credentials', 'origin', 'expose_headers'])


@patch('apistar_cors_hooks.CORS')
def test_initializes_cors_with_default_options(mocked_cors):
    apistar_cors_hooks.CORSRequestHooks()
    assert mocked_cors.called_once_with(lambda x, y: None, {
        "headers": "*",
        "methods": "*",
        "maxage": "86400",
        "origin": "*",
    })


@patch('apistar_cors_hooks.CORS')
def test_initializes_cors_with_custom_options(mocked_cors):
    apistar_cors_hooks.CORSRequestHooks(options={'origin': 'lala.com', 'lala': 'lala'})
    assert mocked_cors.called_once_with(lambda x, y: None, {
        "headers": "*",
        "methods": "*",
        "maxage": "86400",
        "origin": "lala.com",
        "lala": "lala"
    })


def test_self_cors_is_wsgicors_CORS_instance():
    hooks = apistar_cors_hooks.CORSRequestHooks()
    assert isinstance(hooks.cors, wsgicors.CORS)


@patch('apistar_cors_hooks.CORS')
def test_calls_cors_when_calling_on_request(mocked_cors):
    hooks = apistar_cors_hooks.CORSRequestHooks()
    environ = wsgi.WSGIEnviron('lala')
    start_response = wsgi.WSGIStartResponse('lala')

    hooks.on_request(environ, start_response)

    assert mocked_cors().called_once_with(environ, start_response)


@patch('apistar_cors_hooks.CORS')
def test_calls_select_policy_when_calling_on_response(mocked_cors):
    mocked_cors().selectPolicy.return_value = 'lala', 'lulu'

    hooks = apistar_cors_hooks.CORSRequestHooks()
    environ = wsgi.WSGIEnviron({
        'HTTP_ORIGIN': 'orig',
        'REQUEST_METHOD': 'GET'
    })
    response = Response('lala')

    hooks.on_response(environ, response)

    assert mocked_cors.selectPolicy.called_once_with('orig', 'GET')


@patch('apistar_cors_hooks.CORS')
def test_does_not_modify_headers_if_not_ret_origin_on_response(mocked_cors):
    mocked_cors().selectPolicy.return_value = 'lala', None
    mocked_cors().policies = {'lala': FakePolicy('false', 'fake_origin', 'fake_expose_headers')}

    hooks = apistar_cors_hooks.CORSRequestHooks()
    environ = wsgi.WSGIEnviron({'REQUEST_METHOD': 'GET'})
    response = Response('lala')
    expected_headers = deepcopy(response.headers)

    hooks.on_response(environ, response)

    assert response.headers == expected_headers


@patch('apistar_cors_hooks.CORS')
def test_modified_headers_on_response(mocked_cors):
    mocked_cors().selectPolicy.return_value = 'policyname', 'orig'
    mocked_cors().policies = {'policyname': FakePolicy('true', '*', 'fake_expose_headers')}

    hooks = apistar_cors_hooks.CORSRequestHooks()
    environ = wsgi.WSGIEnviron({
        'HTTP_ORIGIN': 'orig',
        'REQUEST_METHOD': 'GET',
    })
    response = Response('lala')

    hooks.on_response(environ, response)

    assert 'orig' == response.headers['Access-Control-Allow-Origin']
    assert 'true' == response.headers['Access-Control-Allow-Credentials']
    assert 'fake_expose_headers' == response.headers['Access-Control-Expose-Headers']


@patch('apistar_cors_hooks.CORS')
def test_headers_vary_on_response(mocked_cors):
    mocked_cors().selectPolicy.return_value = 'policyname', 'orig'
    mocked_cors().policies = {'policyname': FakePolicy('true', 'orig', 'fake_expose_headers')}

    hooks = apistar_cors_hooks.CORSRequestHooks()
    environ = wsgi.WSGIEnviron({
        'HTTP_ORIGIN': 'orig',
        'REQUEST_METHOD': 'GET',
    })
    response = Response('lala')

    hooks.on_response(environ, response)

    assert 'orig' == response.headers['Access-Control-Allow-Origin']
    assert 'true' == response.headers['Access-Control-Allow-Credentials']
    assert 'fake_expose_headers' == response.headers['Access-Control-Expose-Headers']
    assert 'Origin' == response.headers['Vary']
