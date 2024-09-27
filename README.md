# Flintor
An Ultra Lightweight Python Web Development Framework
=========================

Flintor is an ultra-lightweight, dependency-free web framework in Python. It provides core functionalities similar to Flask and Django but remains minimal and efficient. This documentation will guide you through installation, usage, and the various features offered by Flintor.

* * * * *

Table of Contents
-----------------

-   [Features](#features)
-   [Installation](#installation)
-   [Getting Started](#getting-started)
    -   [Hello World Example](#hello-world-example)
-   [Routing](#routing)
    -   [Defining Routes](#defining-routes)
    -   [Dynamic URL Parameters](#dynamic-url-parameters)
    -   [HTTP Methods](#http-methods)
-   [Request and Response Objects](#request-and-response-objects)
    -   [Request Object](#request-object)
    -   [Response Object](#response-object)
-   [Template Rendering](#template-rendering)
-   [Middleware](#middleware)
-   [Static Files](#static-files)
-   [Sessions](#sessions)
-   [Database ORM](#database-orm)
-   [Full Example Application](#full-example-application)
-   [Advanced Topics](#advanced-topics)
    -   [Error Handling](#error-handling)
    -   [Extending the Framework](#extending-the-framework)
-   [FAQ](#faq)
-   [Contributing](#contributing)
-   [License](#license)

* * * * *

Features
--------

-   **Routing with Decorators**: Define routes using Python decorators.
-   **Template Rendering**: Use the built-in `string.Template` for simple templating.
-   **Request and Response Objects**: Encapsulate HTTP request and response data.
-   **Middleware Support**: Add middleware functions for request processing.
-   **Static File Serving**: Serve static files like CSS, JS, and images.
-   **Simple ORM-like Functionality**: Interact with a SQLite database.
-   **Session Management**: Manage user sessions with cookies.

* * * * *

Installation
------------

**Note**: Flintor is designed to be installed via `pip` once it's uploaded to PyPI. For now, you can install it locally.

### Installing from PyPI

bash



`pip install flintor`

*(Assuming the package is uploaded to PyPI under the name `flintor`.)*

### Installing Locally

1.  Clone the repository or download the source code.

2.  Navigate to the root directory of the project (where `setup.py` is located).

3.  Install the package using:

    bash

    

    `pip install .`

* * * * *

Getting Started
---------------

### Hello World Example

Create a file named `app.py` and add the following code:

python



`from flintor import Framework

app = Framework()

@app.route('/')
def index(request):
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()`

Run the application:

bash



`python app.py`

Visit `http://127.0.0.1:8000/` in your browser to see "Hello, World!".

* * * * *

Routing
-------

### Defining Routes

Use the `@app.route()` decorator to define routes.

python



`@app.route('/path')
def handler(request):
    return 'Response'`

### Dynamic URL Parameters

Include dynamic parameters in the URL using angle brackets.

python



`@app.route('/user/<username>')
def show_user_profile(request, username):
    return f"User: {username}"`

### HTTP Methods

Specify allowed HTTP methods using the `methods` parameter.

python



`@app.route('/submit', methods=['GET', 'POST'])
def submit(request):
    if request.method == 'POST':
        # Handle POST request
        pass
    else:
        # Handle GET request
        pass`

* * * * *

Request and Response Objects
----------------------------

### Request Object

The `Request` object provides access to request data.

#### Attributes

-   `request.method`: HTTP method (e.g., 'GET', 'POST').
-   `request.path`: The path of the request URL.
-   `request.query`: Dictionary of query parameters.
-   `request.headers`: HTTP headers.
-   `request.cookies`: Cookies sent by the client.
-   `request.form`: Dictionary of form data (for POST requests).
-   `request.body`: Raw request body.

#### Accessing Query Parameters

python



`value = request.query.get('key', ['default'])[0]`

### Response Object

Use the `Response` object to customize the response.

python



`from  flintor import Response

@app.route('/custom')
def custom_response(request):
    response = Response(
        body='Custom Response',
        status=200,
        headers={'Content-Type': 'text/plain'}
    )
    response.set_cookie('sessionid', 'abc123')
    return response`

* * * * *

Template Rendering
------------------

Render templates using the `render_template` method.

### Template Files

Create templates in the `templates/` directory.

**templates/hello.html**

html



`<html>
<head>
    <title>$title</title>
</head>
<body>
    <h1>Hello, $name!</h1>
</body>
</html>`

### Rendering Templates

python



`@app.route('/hello/<name>')
def hello(request, name):
    return app.render_template('hello.html', title='Greeting', name=name)`

* * * * *

Middleware
----------

Middleware functions process requests before they reach route handlers.

python



`def simple_middleware(request, response):
    print(f"{request.method} request for {request.path}")
    # Return None to continue processing
    return None

app.add_middleware(simple_middleware)`

* * * * *

Static Files
------------

Serve static files from the `static/` directory.

### Accessing Static Files

In your templates:

html



`<link rel="stylesheet" type="text/css" href="/static/style.css">`

### Serving Static Files

Static files are automatically served when requested with the `/static/` path.

* * * * *

Sessions
--------

Manage user sessions using cookies.

### Storing Session Data

python



`@app.route('/login', methods=['POST'])
def login(request):
    username = request.form.get('username', [''])[0]
    request.session['user'] = username
    return 'Logged in'`

### Accessing Session Data

python



`@app.route('/dashboard')
def dashboard(request):
    user = request.session.get('user', 'Guest')
    return f'Welcome, {user}'`

* * * * *

Database ORM
------------

Interact with a SQLite database using the `ORM` class.

### Connecting to the Database

python



`db = ORM('mydatabase.db')`

### Executing Queries

python



`# Create a table
db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)', commit=True)

# Insert a user
db.execute('INSERT INTO users (username) VALUES (?)', (username,), commit=True)

# Fetch users
users = db.fetchall('SELECT * FROM users')`

### Closing the Connection

python



`db.close()`

* * * * *

Full Example Application
------------------------

**Project Structure**

arduino



`your_app/
├── app.py
├── templates/
│   ├── index.html
│   ├── hello.html
├── static/
│   └── style.css`

**app.py**

python



`from flintor import Framework, Response

app = Framework()

@app.route('/')
def index(request):
    return app.render_template('index.html', title='Home', message='Welcome!')

@app.route('/hello/<name>')
def hello(request, name):
    return app.render_template('hello.html', title='Greeting', name=name)

def logger_middleware(request, response):
    print(f"{request.method} {request.path}")
    return None

app.add_middleware(logger_middleware)

if __name__ == '__main__':
    app.run()`

**templates/index.html**

html



`<html>
<head>
    <title>$title</title>
    <link rel="stylesheet" type="text/css" href="/static/style.css">
</head>
<body>
    <h1>$message</h1>
    <p><a href="/hello/World">Say Hello</a></p>
</body>
</html>`

**templates/hello.html**

html



`<html>
<head>
    <title>$title</title>
</head>
<body>
    <h1>Hello, $name!</h1>
</body>
</html>`

* * * * *

Advanced Topics
---------------

### Error Handling

Customize error responses by overriding the `send_error` method in the `RequestHandler` class.

python



`def custom_send_error(self, code, message=None):
    self.send_response(code)
    self.end_headers()
    self.wfile.write(f"<h1>Error {code}</h1><p>{message}</p>".encode())

# In the Framework class, modify the _make_handler method:
def _make_handler(self):
    # Existing code...
    class RequestHandler(http.server.BaseHTTPRequestHandler):
        # Existing methods...

        def send_error(self, code, message=None):
            custom_send_error(self, code, message)`

### Extending the Framework

-   **Template Engine**: Integrate a more powerful template engine like Jinja2.
-   **Database Models**: Build an ORM layer for model representations.
-   **Security**: Implement authentication and authorization mechanisms.

* * * * *

FAQ
---


### Can I use a different database?

The included ORM uses SQLite for simplicity. You can extend the `ORM` class to support other databases or integrate a full-featured ORM like SQLAlchemy.

### How do I serve files other than CSS or images?

Any files placed in the `static/` directory can be served. Just ensure they're accessible via the correct URL path.

* * * * *

Contributing
------------

Contributions are welcome! To contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bugfix.
3.  Make your changes.
4.  Submit a pull request.

Remember, I am not God. I have not thought of everything, if you have an idea on what to do, please do it. I would love to incorportate it.

Please ensure your code follows good coding practices and includes documentation/comments where necessary.

Side note: If someone would be willing to clean up this readme with proper markdown format, it would be awesome. I will be getting to that later.
