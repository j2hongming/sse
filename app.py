import json
import time
import redis

from flask import Flask, Response, render_template

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/stream')
def stream():
    def iter_data():
        while True:
            yield 'data:' + json.dumps({'time': time.strftime('%Y-%m-%d %H:%M:%S')}) + '\n\n'
            time.sleep(3)
    return iter_data(), {'Content-Type': 'text/event-stream'}

@app.route('/hit')
def hit():
    count = get_hit_count()
    return 'Hit count: {}\n'.format(count)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
