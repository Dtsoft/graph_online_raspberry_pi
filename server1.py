from flask import Flask

app = Flask(__name__)


@app.route('/')
def show_image():
    return '<img src="static/image.png">'


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')
