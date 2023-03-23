import logging.config
from os import environ
from typing import Tuple
from argparse import ArgumentParser, FileType
from configparser import ConfigParser

from dotenv import load_dotenv


def _load_config() -> Tuple[ConfigParser, str]:
    parser = ArgumentParser()
    parser.add_argument('--nauron-config', type=FileType('r'), default='config/config.ini',
                        help="Path to config file.")
    parser.add_argument('--log-config', type=FileType('r'), default='config/logging.ini',
                        help="Path to log config file.")
    args = parser.parse_known_args()[0]

    config = ConfigParser()
    config.read(args.nauron_config.name)
    return config, args.log_config.name


_config, _log_config = _load_config()
logging.config.fileConfig(_log_config)

load_dotenv('config/.env')
load_dotenv('config/sample.env')

DISTRIBUTED = environ.get('NAURON_MODE') in ['GATEWAY', 'WORKER']

MQ_PARAMS = None
if DISTRIBUTED:
    import pika

    MQ_PARAMS = pika.ConnectionParameters(
        host=environ.get('MQ_HOST'),
        port=environ.get('MQ_PORT'),
        credentials=pika.credentials.PlainCredentials(username=environ.get('MQ_USERNAME'),
                                                      password=environ.get('MQ_PASSWORD')))

MESSAGE_TIMEOUT = int(environ.get('GUNICORN_TIMEOUT', '30')) * 1000
MAX_CONTENT_LENGTH = eval(_config['general']['max_request_size'])

SERVICE_NAME = _config['nauron']['service']
ROUTING_KEY = _config['nauron']['routing_key']

MODEL_PATH = _config['general']['model_path']
