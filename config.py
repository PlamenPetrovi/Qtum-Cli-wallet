import os

DEBUG = False
PORT = 3404
SECRET_KEY = os.urandom(24)
WALLET_DIR = os.path.expanduser('~/.qtum')
QTUM_PATH = 'qtum-cli'
DONATION_ADDR = 'qtum:QceE7a47byDhFs9wy2c2ZdXz4yfT4RZLJQ?amount=&label=Donation&message=PIUI-Donation'
UI_VERSION = 'v0.3.2-Beta'

try:
    from local_config import *
except ImportError:
    # no local config found
    pass
