import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def buggy_function(x):
    logging.debug(f'Function called with x={x}')
    return 10 / x

try:
    result = buggy_function(0)
except Exception as e:
    logging.error(f'Error occurred: {e}')