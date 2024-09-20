import http.server
import socketserver
import urllib.parse
import re
import os
import threading
from http import cookies
import time
import random
import string
from string import Template

class Request:
    def __init__(self, handler):
        self.handler = handler
        self.method = handler.command
        self.path = urllib.parse.urlparse(handler.path).path
        self.query = urllib.parse.parse_qs(urllib.parse.urlparse(handler.path).query)
        self.headers = handler.headers
        self.cookies = cookies.SimpleCookie(handler.headers.get('Cookie'))
        self.session = {}
        self.body = None
        self.form = {}
        if self.method == 'POST':
            length = int(handler.headers.get('Content-Length', 0))
            self.body = handler.rfile.read(length).decode()
            self.form = urllib.parse.parse_qs(self.body)

    def get_cookie(self, key):
        return self.cookies.get(key).value if key in self.cookies else None

class Response:
    def __init__(self, body='', status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}
        self.cookies = cookies.SimpleCookie()

    def set_cookie(self, key, value, **kwargs):
        self.cookies[key] = value
        for k, v in kwargs.items():
            self.cookies[key][k.replace('_', '-')] = v

class Framework:
    def __init__(self):
        self.routes = []
        self.middlewares = []
        self.static_dir = 'static'
        self.template_dir = 'templates'
        self.sessions = {}
        self.session_lock = threading.Lock()

    def route(self, path, methods=['GET']):
        pattern = '^' + re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path) + '$'
        route_re = re.compile(pattern)

        def decorator(func):
            self.routes.append((methods, route_re, func))
            return func
        return decorator

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

    def render_template(self, template_name, **context):
        template_path = os.path.join(self.template_dir, template_name)
        with open(template_path, 'r') as f:
            tmpl = Template(f.read())
        return tmpl.substitute(**context)

    def generate_session_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=24))

    def get_session(self, request, response):
        session_id = request.get_cookie('SESSION_ID')
        if not session_id or session_id not in self.sessions:
            session_id = self.generate_session_id()
            response.set_cookie('SESSION_ID', session_id, path='/')
            with self.session_lock:
                self.sessions[session_id] = {}
        request.session = self.sessions[session_id]

    def run(self, host='127.0.0.1', port=8000):
        handler_class = self._make_handler()
        with socketserver.ThreadingTCPServer((host, port), handler_class) as httpd:
            print(f"Serving on http://{host}:{port}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nShutting down server...")

    def _make_handler(self):
        app = self

        class RequestHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.handle_request()

            def do_POST(self):
                self.handle_request()

            def handle_request(self):
                request = Request(self)
                response = Response()

                app.get_session(request, response)

                # Middleware processing (before)
                for middleware in app.middlewares:
                    result = middleware(request, response)
                    if isinstance(result, Response):
                        self._send_response(result)
                        return

                for methods, route_re, func in app.routes:
                    match = route_re.match(request.path)
                    if match and request.method in methods:
                        kwargs = match.groupdict()
                        result = func(request, **kwargs)
                        if isinstance(result, Response):
                            self._send_response(result)
                        else:
                            response.body = str(result)
                            self._send_response(response)
                        return

                # Serve static files
                if self.serve_static(request, response):
                    return

                self.send_error(404, "Not Found")

            def serve_static(self, request, response):
                if request.path.startswith('/static/'):
                    file_path = os.path.join(app.static_dir, request.path[len('/static/'):])
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as f:
                            content = f.read()
                        response.body = content
                        self._send_response(response, binary=True)
                        return True
                return False

            def _send_response(self, response, binary=False):
                self.send_response(response.status)
                for key, value in response.headers.items():
                    self.send_header(key, value)
                for morsel in response.cookies.values():
                    self.send_header('Set-Cookie', morsel.OutputString())
                self.end_headers()
                if binary:
                    self.wfile.write(response.body)
                else:
                    self.wfile.write(response.body.encode())

            def log_message(self, format, *args):
                pass

        return RequestHandler
