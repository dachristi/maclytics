import re

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

from sql_queries import query_average_dwell
from sql_queries import query_unique_visitors
from sql_queries import query_mac_search
from sql_queries import query_current_devices
from sql_queries import query_repeat_devices


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dwell', methods=['POST'])
def dwell():
    dwell_time = query_average_dwell(1, 2)
    return jsonify(dwell_time=dwell_time)


@app.route('/unique_visitors', methods=['POST'])
def unique_visitors():
    unique_visitor_count = query_unique_visitors()
    return jsonify(unique_visitor_count=unique_visitor_count)


@app.route('/current_devices', methods=['POST'])
def current_devices():
    current_device_count = query_current_devices()
    return jsonify(current_device_count=current_device_count)


@app.route('/repeat_devices', methods=['POST'])
def repeat_devices():
    repeat_device_count = query_repeat_devices()
    return jsonify(repeat_device_count=repeat_device_count)


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        mac = str(request.form['data'])
        print(mac)
        mac = mac.lower()
        mac = re.sub(r'\:', '', mac)
    else:
        return jsonify(num_entries='Bad Entry')
    mac_count = query_mac_search(mac)
    print(mac)
    return jsonify(mac_count=mac_count)


if __name__ == '__main__':
    app.run(debug=True)
