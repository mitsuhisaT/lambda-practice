import json
import logging
import subprocess
import sys


logger = logging.getLogger()
if (os.getenv('LOG_LEVEL') is not None):
    log_level = os.environ['LOG_LEVEL']
else:
    log_level = 'INFO'
level = logging.getLevelName(log_level)
if not isinstance(level, int):
    level = logging.INFO
logger.setLevel(level)
formatter = logging.Formatter(
    ('[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t)'
        '%(filename)s\t%(funcname)s\t%(lineno)s\t%(message)s\n'),
    '%y-%m-%dT%H:%M:%S'
    )
for handler in logger.handlers:
    handler.setFormatter(formatter)


logger.debug('Loading function.')


def lambda_handler(event, context):
    # TODO implement
    command = ['ffmpeg', '-version']
    # res = subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    res = subprocess.run(command, capture_output=True, text=True)
    logging.debug(f'res: {res}')

    return {
        'statusCode': 200,
        # 'body': res.decord()
    }
