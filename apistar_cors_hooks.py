
from apistar.http import Response
from apistar.server import wsgi
from wsgicors import CORS

__all__ = ["CORSRequestHooks"]
__version__ = "0.1.0"


class CORSRequestHooks:

    def __init__(self, options={}):
        options = {
            "headers": "*",
            "methods": "*",
            "maxage": "86400",
            "origin": "*",
            **options
        }
        self.cors = CORS(lambda x, y: None, **options)

    def on_request(self, environ: wsgi.WSGIEnviron, start_response: wsgi.WSGIStartResponse):
        self.cors(environ, start_response)

    def on_response(self, environ: wsgi.WSGIEnviron, response: Response):
        orig = environ.get("HTTP_ORIGIN", None)
        request_method = environ['REQUEST_METHOD']
        headers = response.headers

        policyname, ret_origin = self.cors.selectPolicy(orig, request_method)
        policy = self.cors.policies[policyname]

        if policy.credentials == 'true' and policy.origin == "*":
            # for credentialed access '*' are ignored in origin
            ret_origin = orig

        if ret_origin:
            headers['Access-Control-Allow-Origin'] = ret_origin

            if policy.credentials == 'true':
                headers['Access-Control-Allow-Credentials'] = 'true'

            if policy.expose_headers:
                headers['Access-Control-Expose-Headers'] = policy.expose_headers

            if policy.origin != "*":
                headers['Vary'] = 'Origin'
