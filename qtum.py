import subprocess
import time
import json
import config

DONATION_ADDR = config.DONATION_ADDR
UI_VERSION = config.UI_VERSION
QTUM_PATH = config.QTUM_PATH
WALLET_DIR = config.WALLET_DIR

def procedure_call(x='', y='', path=QTUM_PATH):
    process = subprocess.Popen("%s %s %s" % (path, x, y), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = process.communicate()
    if process.returncode != 0:
        return None
    return out

def qtum_info(x='getwalletinfo', y=''):
    call = procedure_call(x,y)
    if call == None:
        return None
    result = str(call,'utf-8')
    parsed_result = json.loads(result)
    return parsed_result

def qtum(x):
    call = procedure_call(x)
    if call == None:
        return None
    result = str(call,'utf-8')
    return result

def immature_coins():
    total_coins = 0
    unspent_coins = qtum_info('listunspent', 0)
    for unspent in unspent_coins:
        if unspent['confirmations'] < 500:
            total_coins += unspent['amount']
    return total_coins

def wallet_checks():
    check_wallet = qtum_info()
    if check_wallet == None:
        return 'Not_Running'
    result = list(check_wallet.keys())
    if 'unlocked_until' not in result:
        return 'Not_Encrypted'
    return 'OK'

def wallet_start_up():
    process = subprocess.Popen("~/qtum-wallet/bin/qtumd -daemon=1", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out,err) = process.communicate()
    if process.returncode != 0:
        return None
    return process

def qtum_unlock(passwd, duration, stake='false'):
    wallet_unlock = 'walletpassphrase "%s" %d %s' % (passwd, duration, stake)
    call = procedure_call(wallet_unlock)
    if call == None:
        return None
    return call

def get_time():
    time_to_stake = qtum("getstakinginfo | grep expectedtime | cut -d':' -f2")
    time = int(time_to_stake) / 60 / 60 / 24
    expected_stake = round(time)
    return expected_stake

def last_sent_tx():
    last_tx = qtum_info("listtransactions '*'", 100)
    all_sent = {}
    for send in last_tx:
        if send['category'] == "send" or  send['category'] == "move":
            all_sent.update(send)
    return all_sent

def get_address():
    response = qtum("getaccountaddress ''")
    return response

def get_account_addresses():
    list_accounts = qtum_info("listaccounts")
    all_addresses = {}
    for x in list_accounts:
        each_address = qtum("getaddressesbyaccount '%s'" % x)
        parsed_json = json.loads(each_address)
        all_addresses[x] = parsed_json
    return all_addresses

def donate_piui():
    donation_string = DONATION_ADDR
    return donation_string

def qrcode_format(address, amount, name, msg):
    response = 'qtum:%s?amount=%s&label=%s&message=%s' % (address, amount, name, msg)
    return response
