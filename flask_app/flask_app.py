import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def base_route():
    return '<h1>Instance number {} is responding now!</h1>'.format(os.environ['instanceId'])

@app.route('/hello')
def hello():
    return '<h1>hello world</h1>'


@app.route('/cluster1')
@app.route('/cluster2')
def cluster_route():
    return '<h1>Instance number {} is responding now!</h1>'.format(os.environ['instanceId'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
