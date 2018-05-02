# -*-coding:utf-8 -*-

import json

import redis
from flask import Flask, render_template, jsonify, request, current_app

from nec_manage.monitor.monitor_settings import *
from nec_manage.monitor import dat_service
from nec_manage.monitor import url_extract_tools


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", timeinterval=TIMEINTERVAL, stats_keys=STATS_KEYS)


@app.route('/ajax')
def ajax():
    key = request.args.get('key')
    result = current_app.r.lrange(key, -POINTLENGTH, -1)[::POINTINTERVAL]
    if not current_app.spider_is_run:
        # spider is closed
        return json.dumps(result).replace('"', ''), 404
    return json.dumps(result).replace('"', '')


@app.route('/signal')
def signal():
    signal = request.args.get('sign')
    if signal == 'closed':
        current_app.spider_is_run = False
    elif signal == 'running':
        current_app.spider_is_run = True
    return jsonify('')


@app.route('/gen_spider', methods=['GET', 'POST'])
def gen_spider():
    jsonstr = request.form.get('json_result', '')
    js = dict(json.loads(jsonstr))
    start_urls = list(js['start_urls'])
    spider_name = url_extract_tools.extract_main_url(start_urls)
    dat_service.save_data(spider_name, jsonstr)
    return jsonify('ok')


@app.route('/add_ips', methods=['GET', 'POST'])
def add_ips():
    jsonstr = request.form.get('ips', '')
    ips_array = json.loads(jsonstr)['ips']
    print(ips_array)
    with open('static/valid_proxy.txt', 'a') as f:
        for i in ips_array:
            f.write(i + '\n')
    return jsonify('ok')


# @app.before_first_request
# def init():
#     current_app.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
#     current_app.spider_is_run = True if current_app.r.get('spider_is_run') == '1' else False


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT, debug=True)
