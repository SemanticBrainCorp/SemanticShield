import logging
import time

from argparse import ArgumentParser

from flask import Flask, request, session, jsonify
from flask_cors import CORS, cross_origin
from waitress import serve

from SemanticShield.yaml_parser import yaml_role_to_df
from SemanticShield.rb_generator import generate_for_role
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

@app.route(PREFIX + '/generate', methods=['POST'])
@cross_origin()
def generate():
    logging.info('entry')

    req = request.json
    role = req['role']
    text = req['text']

    result = generate_for_role(role_config_df, role, text)
    
    jsdata = {}
    jsdata['status'] = {
        "statusCode": 0,
        "statusDescription": "OK",
        "timestamp": int(time.time())
    }
    jsdata['data'] = result

    return jsonify(jsdata), 200

if __name__ == '__main__':
    parser = ArgumentParser(
        prog='SemanticShield',
        description='Semantic Shield helps manage AI security, safety and alignment',
        epilog='Use above options to overide default values for port, URL prefix and config file.')
    parser.add_argument("-p", "--port", nargs='?', type=int, default=8061, const=8061,
                    help="Specify alternate to the default port 8061")
    parser.add_argument("-u", "--url", nargs='?', type=str, default='/shield/v1', const='/shield/v1',
                    help="Specify alternate to the default URL prefix /shield/v1")
    parser.add_argument("-c", "--config", nargs='?', type=str, default='config_defaults.yml', const='config.yml',
                    help="Specify alternate to the default config file config.yml")

    port = parser.parse_args().port
    PREFIX = parser.parse_args().url
    config_file = parser.parse_args().config

    global role_config_df
    role_config_df = yaml_role_to_df(config_file)
    
    serve(app, host='0.0.0.0', port=port)
