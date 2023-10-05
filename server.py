import logging
from pprint import pprint
import time

from flask import Flask, request, session, jsonify
from flask_cors import CORS, cross_origin
from waitress import serve

from SemanticShield import SemanticShield, ShieldConfig
from SemanticShield.errors import APIKEYException

PREFIX = '/shield/v1'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = '43o56(S&p?Ox'

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -15s %(filename) -15s %(funcName) '
              '-15s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("tldextract").setLevel(logging.WARNING)
logging.getLogger("filelock").setLevel(logging.WARNING)

def init_shield(config):
    if config is None:
        shield = SemanticShield()
    else:
        shield = SemanticShield(ShieldConfig.from_dict(config))
    return shield

@app.route(PREFIX + '/check', methods=['POST'])
@cross_origin()
def check():
    logging.info('entry')

    req = request.json
    text = req['text']
    config = req.get('config', None)
    shield = init_shield(config)
    try:
        result = shield(text)
    except APIKEYException:
        jsdata = {}
        jsdata['status'] = {
            "statusCode": 2,
            "statusDescription": "ERROR",
            "timestamp": int(time.time())
        }
        jsdata['data'] = "OPENAI key missing"

        return jsonify(jsdata), 500


    if result.fail:
        print(f'FAIL {result.message}')
    else:
        print('PASS')
    print(f'Token usage: {result.usage}')

    jsdata = {}
    jsdata['status'] = {
        "statusCode": 0,
        "statusDescription": "OK",
        "timestamp": int(time.time())
    }
    jsdata['data'] = result

    return jsonify(jsdata), 200

@app.route(PREFIX + '/sanitize', methods=['POST'])
@cross_origin()
def sanitize():
    logging.info('entry')

    req = request.json
    text = req['text']
    config = req.get('config', None)

    shield = init_shield(config)
    result = shield.sanitize(text)
    
    jsdata = {}
    jsdata['status'] = {
        "statusCode": 0,
        "statusDescription": "OK",
        "timestamp": int(time.time())
    }
    jsdata['data'] = result

    return jsonify(jsdata), 200

@app.route(PREFIX + '/revert', methods=['POST'])
@cross_origin()
def revert():
    logging.info('entry')

    req = request.json
    text = req['text']
    replacement_map = req['replacement_map']
    config = req.get('config', None)

    shield = init_shield(config)
    result = shield.revert(text, replacement_map=replacement_map)
        
    jsdata = {}
    jsdata['status'] = {
        "statusCode": 0,
        "statusDescription": "OK",
        "timestamp": int(time.time())
    }
    jsdata['data'] = result

    return jsonify(jsdata), 200


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8061)
