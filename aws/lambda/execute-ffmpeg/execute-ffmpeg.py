import json
import logging
import subprocess
import sys


logger = logging.getLogger()
for h in logger.handlers:
  logger.removeHandler(h)

h = logging.StreamHandler(sys.stdout)

FORMAT = '%(levelname)s %(asctime)s [%(funcName)s] %(message)s'
h.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(h)

logger.setLevel(logging.DEBUG)


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
