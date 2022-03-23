import time
from datetime import datetime

import requests

import config


def check_token(token, tg_id):
    users = get_all_users()
    pairs = []

    for i in users:
        pair = {str(i['token']): str(i['tg_id'])}
        pairs.append(pair)

    if {token: tg_id} in pairs and token[:1] == 'A':
        return 'admin'
    elif {token: tg_id} in pairs and token[:6] == 'USRMCNT':
        return 'user'
    else:
        return False


def get_all_users():
    response = requests.get('http://127.0.0.1:8000/user/')
    return response.json()


def get_user_info(id_):
    response = requests.get('http://127.0.0.1:8000/user/' + str(id_))

    return response.json()


def get_admins():
    response = get_all_users()
    adm = []
    for r in response:
        if r['role'] == 'admin':
            adm.append(r['tg_id'])

    return adm


def add_user(username, token, tg_id, limit, current_limit, role, address_USDT):
    date = datetime.now().date()
    data = {"username": username,
            "token": token,
            "tg_id": tg_id,
            "limit": limit,
            "current_limit": current_limit,
            "role": role,
            "address_USDT": address_USDT,
            "state": 'no_deposit',
            "reg_date": date
            }
    requests.post('http://127.0.0.1:8000/user/', data=data)


def delete_user(token):
    requests.delete('http://127.0.0.1:8000/user/' + token + '/')


def change_limit(username, token, tg_id, limit, current_limit, role):
    data = {
            "username": username,
            "token": token,
            "tg_id": tg_id,
            "limit": limit,
            "current_limit": current_limit,
            "role": role
            }
    requests.put('http://127.0.0.1:8000/user/' + tg_id + '/', json=data)



def change_current_limit(tg_id, amount):
    info = get_user_info(tg_id)
    current_limit = info['current_limit']
    data = {
            "username": info['username'],
            "token": info['token'],
            "tg_id": tg_id,
            "limit": info['limit'],
            "current_limit": current_limit - amount,
            "role": info['role']
            }
    requests.put('http://127.0.0.1:8000/user/' + str(tg_id) + '/', json=data)


def change_user_state(tg_id, state):
    info = get_user_info(tg_id)
    data = {
        "username": info['username'],
        "token": info['token'],
        "tg_id": tg_id,
        "limit": info['limit'],
        "current_limit": info['current_limit'],
        "role": info['role'],
        "state": state
    }
    requests.put('http://127.0.0.1:8000/user/' + str(tg_id) + '/', json=data)


def change_trade_amount(tg_id, amount):
    info = get_user_info(tg_id)
    data = {
            "username": info['username'],
            "token": info['token'],
            "tg_id": tg_id,
            "limit": info['limit'],
            "current_limit": info['current_limit'],
            "role": info['role'],
            "trade_amount": info['trade_amount'] + amount,
            }
    requests.put('http://127.0.0.1:8000/user/' + str(tg_id) + '/', json=data)


def change_trade_count(tg_id):
    info = get_user_info(tg_id)
    data = {
            "username": info['username'],
            "token": info['token'],
            "tg_id": tg_id,
            "limit": info['limit'],
            "current_limit": info['current_limit'],
            "role": info['role'],
            "trade_count": info['trade_count'] + 1,
            }
    requests.put('http://127.0.0.1:8000/user/' + str(tg_id) + '/', json=data)


def change_USDT_balance(tg_id, amount, action):
    info = get_user_info(tg_id)
    if action == 'plus':
        data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "USDT_balance": info['USDT_balance'] + amount
                }
    elif action == 'minus':
        data = {
            "username": info['username'],
            "token": info['token'],
            "tg_id": tg_id,
            "limit": info['limit'],
            "current_limit": info['current_limit'],
            "role": info['role'],
            "USDT_balance": info['USDT_balance'] - amount
        }

    requests.put('http://127.0.0.1:8000/user/' + str(tg_id) + '/', json=data)


def change_coin_balance(tg_id, amount, action, coin):
    info = get_user_info(tg_id)
    if action == 'plus':
        if coin == 'SOL':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "SOL_balance": info['SOL_balance'] + amount
            }
        elif coin == 'TRX':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "TRX_balance": info['TRX_balance'] + amount
            }
        elif coin == 'USDT':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "USDT_balance": info['USDT_balance'] + amount
            }
        elif coin == 'ADA':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "ADA_balance": info['ADA_balance'] + amount
            }
        elif coin == 'DOGE':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "DOGE_balance": info['DOGE_balance'] + amount
            }
        elif coin == 'MATIC':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "MATIC_balance": info['MATIC_balance'] + amount
            }
        elif coin == 'LUNA':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "LUNA_balance": info['LUNA_balance'] + amount
            }
        elif coin == 'DOT':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "DOT_balance": info['DOT_balance'] + amount
            }
        elif coin == 'AVAX':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "AVAX_balance": info['AVAX_balance'] + amount
            }
    elif action == 'minus':
        if coin == 'SOL':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "SOL_balance": info['SOL_balance'] - amount
            }
        elif coin == 'TRX':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "TRX_balance": info['TRX_balance'] - amount
            }
        elif coin == 'USDT':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "USDT_balance": info['USDT_balance'] - amount
            }
        elif coin == 'ADA':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "ADA_balance": info['ADA_balance'] - amount
            }
        elif coin == 'DOGE':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "DOGE_balance": info['DOGE_balance'] - amount
            }
        elif coin == 'MATIC':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "MATIC_balance": info['MATIC_balance'] - amount
            }
        elif coin == 'LUNA':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "LUNA_balance": info['LUNA_balance'] - amount
            }
        elif coin == 'DOT':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "DOT_balance": info['DOT_balance'] - amount
            }
        elif coin == 'AVAX':
            data = {
                "username": info['username'],
                "token": info['token'],
                "tg_id": tg_id,
                "limit": info['limit'],
                "current_limit": info['current_limit'],
                "role": info['role'],
                "AVAX_balance": info['AVAX_balance'] - amount
            }
    requests.put('http://127.0.0.1:8000/user/' + str(tg_id) + '/', json=data)


def change_reg_date(uid, new_date):
    info = get_user_info(uid)
    date = datetime.strptime(new_date, '%Y-%m-%d').date()
    data = {
        "username": info['username'],
        "token": info['token'],
        "tg_id": info['tg_id'],
        "limit": info['limit'],
        "current_limit": info['current_limit'],
        "role": info['role'],
        "reg_date": new_date
    }
    requests.put('http://127.0.0.1:8000/user/' + str(uid) + '/', json=data)


def get_coins():
    response = requests.get('http://127.0.0.1:8000/coin/')
    return response.json()


def get_coin_info(tiker):
    response = requests.get('http://127.0.0.1:8000/coin/' + str(tiker))
    return response.json()


def add_coin(tiker, network, address):
    data = {"tiker": tiker,
            "network_type": network,
            "address": address
            }
    response = requests.post('http://127.0.0.1:8000/coin/', data=data)
    return response


def delete_coin(tiker):
    requests.delete('http://127.0.0.1:8000/coin/' + tiker + '/')


def change_coin_addr(tiker, addr):
    coin = get_coin_info(tiker)
    data = {"tiker": tiker,
            "network_type": coin['network_type'],
            "address": addr
            }
    response = requests.put('http://127.0.0.1:8000/coin/' + tiker + '/', data=data)

    return response


def get_orders():
    response = requests.get('http://127.0.0.1:8000/order/')
    return response.json()


def get_order_info(id):
    response = requests.get('http://127.0.0.1:8000/order/' + str(id))
    return response.json()


def add_order(id, status, owner_id, amount, cryptocurrency, from_, to_, type):
    data = {"id": id,
            "status": status,
            "owner_id": owner_id,
            "amount": amount,
            "cryptocurrency": cryptocurrency,
            "from_adr": from_,
            "to_adr": to_,
            "type": type
            }
    print(data)
    response = requests.post('http://127.0.0.1:8000/order/', data=data)
    return response


def delete_order(id):
    requests.delete('http://127.0.0.1:8000/order/' + str(id) + '/')


def get_user_orders(uid):
    orders = get_orders()
    u_orders = []
    for order in orders:
        if order['owner_id'] == uid:
            u_orders.append(order)

    return u_orders


def change_order_status(order_id, new_status):
    order_info = get_order_info(order_id)
    data = {"id": order_id,
            "status": new_status,
            "owner_id": order_info['owner_id'],
            "amount": order_info['amount'],
            "cryptocurrency": order_info['cryptocurrency'],
            "from_adr": order_info['from_adr'],
            "to_adr": order_info['to_adr'],
            "type": order_info['type']
            }
    requests.put('http://127.0.0.1:8000/order/' + str(order_id) + '/', json=data)


def change_order_flag(order_id, flag):
    order_info = get_order_info(order_id)
    data = {"id": order_id,
            "status": order_info['status'],
            "owner_id": order_info['owner_id'],
            "amount": order_info['amount'],
            "cryptocurrency": order_info['cryptocurrency'],
            "from_adr": order_info['from_adr'],
            "to_adr": order_info['to_adr'],
            "type": order_info['type'],
            "flag": flag
            }
    requests.put('http://127.0.0.1:8000/order/' + str(order_id) + '/', json=data)


def set_order_link(order_id, link):
    order_info = get_order_info(order_id)
    data = {"id": order_id,
            "status": order_info['status'],
            "owner_id": order_info['owner_id'],
            "amount": order_info['amount'],
            "cryptocurrency": order_info['cryptocurrency'],
            "from_adr": order_info['from_adr'],
            "to_adr": order_info['to_adr'],
            "type": order_info['type'],
            "link": link
            }

    requests.put('http://127.0.0.1:8000/order/' + str(order_id) + '/', json=data)


def get_ads():
    response = requests.get('http://127.0.0.1:8000/ad/')
    return response.json()


def get_ad_info(id):
    response = requests.get('http://127.0.0.1:8000/ad/' + str(id))
    return response.json()


def add_ad(id, owner_id, min_amount, max_amount):
    data = {"id": id,
            "owner_id": owner_id,
            "min_amount": min_amount,
            "max_amount": max_amount,
            "state": True,
            }

    response = requests.post('http://127.0.0.1:8000/ad/', data=data)
    return response


def delete_ad(id):
    requests.delete('http://127.0.0.1:8000/ad/' + str(id) + '/')


def get_user_ads(uid):
    ads = get_ads()
    u_ads = []
    for ad in ads:
        if str(ad['owner_id']) == str(uid):
            u_ads.append(ad)

    return u_ads


def change_ad_state(aid, state):
    ad_info = get_ad_info(aid)
    data = {"id": ad_info['id'],
            "owner_id": ad_info['owner_id'],
            "min_amount": ad_info['min_amount'],
            "max_amount": ad_info['max_amount'],
            "state": state,
            "description": ad_info['description']
            }

    requests.put('http://127.0.0.1:8000/ad/' + str(aid) + '/', json=data)


def change_ad_amount(aid, max_amount):
    ad_info = get_ad_info(aid)
    data = {"id": ad_info['id'],
            "owner_id": ad_info['owner_id'],
            "min_amount": ad_info['min_amount'],
            "max_amount": max_amount,
            "state": ad_info['state'],
            "description": ad_info['description']
            }

    requests.put('http://127.0.0.1:8000/ad/' + str(aid) + '/', json=data)


def change_ad_min(aid, min_amount):
    ad_info = get_ad_info(aid)
    data = {"id": ad_info['id'],
            "owner_id": ad_info['owner_id'],
            "min_amount": min_amount,
            "max_amount": ad_info['max_amount'],
            "state": ad_info['state'],
            "description": ad_info['description']
            }

    requests.put('http://127.0.0.1:8000/ad/' + str(aid) + '/', json=data)


def get_trades():
    response = requests.get('http://127.0.0.1:8000/trade/')
    return response.json()


def get_trade_info(id_):
    response = requests.get('http://127.0.0.1:8000/trade/' + str(id_))
    return response.json()


def add_trade(id_, to_id, state, usdt_amount, coin_amount, coin):
    data = {"id": id_,
            "to_id": to_id,
            "state": state,
            "usdt_amount": usdt_amount,
            "coin_amount": coin_amount,
            "coin": coin
            }

    response = requests.post('http://127.0.0.1:8000/trade/', data=data)
    return response


def delete_trade(id):
    requests.delete('http://127.0.0.1:8000/trade/' + str(id) + '/')


def change_trade_state(tid, state):
    trade_info = get_trade_info(tid)
    data = {"id": trade_info['id'],
            "to_id": trade_info['to_id'],
            "state": state,
            "usdt_amount": trade_info['usdt_amount'],
            "coin_amount": trade_info['coin_amount'],
            "coin": trade_info['coin']
            }

    requests.put('http://127.0.0.1:8000/trade/' + str(tid) + '/', json=data)


def create_fake_ad(fid, owner_name, trade_number, trade_amount, reg_date, min_amount, max_amount, des):
    data = {"id": fid,
            "owner_name": owner_name,
            "trade_number": trade_number,
            "trade_amount": trade_amount,
            "reg_date": reg_date,
            "min_amount": min_amount,
            "max_amount": max_amount,
            "des": des
            }

    response = requests.post('http://127.0.0.1:8000/fake/', data=data)
    return response


def get_fake_ads():
    response = requests.get('http://127.0.0.1:8000/fake/')
    return response.json()


def get_fake_info(id_):
    response = requests.get('http://127.0.0.1:8000/fake/' + str(id_))
    return response.json()


def delete_fake(id_):
    requests.delete('http://127.0.0.1:8000/fake/' + str(id_) + '/')


def change_fake_min(id_, new_min):
    fake_info = get_fake_info(id_)
    data = {"id": fake_info['id'],
            "owner_name": fake_info['owner_name'],
            "trade_number": fake_info['trade_number'],
            "trade_amount": fake_info['trade_amount'],
            "reg_date": fake_info['reg_date'],
            "min_amount": float(new_min),
            "max_amount": fake_info['max_amount'],
            "des": fake_info['des']
            }

    requests.put('http://127.0.0.1:8000/fake/' + str(id_) + '/', json=data)


def change_fake_max(id_, new_max):
    fake_info = get_fake_info(id_)
    data = {"id": fake_info['id'],
            "owner_name": fake_info['owner_name'],
            "trade_number": fake_info['trade_number'],
            "trade_amount": fake_info['trade_amount'],
            "reg_date": fake_info['reg_date'],
            "min_amount": fake_info['min_amount'],
            "max_amount": float(new_max),
            "des": fake_info['des']
            }

    requests.put('http://127.0.0.1:8000/fake/' + str(id_) + '/', json=data)


def change_fake_count(id_, new_count):
    fake_info = get_fake_info(id_)
    data = {"id": fake_info['id'],
            "owner_name": fake_info['owner_name'],
            "trade_number": int(new_count),
            "trade_amount": fake_info['trade_amount'],
            "reg_date": fake_info['reg_date'],
            "min_amount": fake_info['min_amount'],
            "max_amount": fake_info['max_amount'],
            "des": fake_info['des']
            }

    requests.put('http://127.0.0.1:8000/fake/' + str(id_) + '/', json=data)


def change_fake_amount(id_, new_amount):
    fake_info = get_fake_info(id_)
    data = {"id": fake_info['id'],
            "owner_name": fake_info['owner_name'],
            "trade_number": fake_info['trade_number'],
            "trade_amount": float(new_amount),
            "reg_date": fake_info['reg_date'],
            "min_amount": fake_info['min_amount'],
            "max_amount": fake_info['max_amount'],
            "des": fake_info['des']
            }

    requests.put('http://127.0.0.1:8000/fake/' + str(id_) + '/', json=data)


def get_min_amount_for_out(tiker):
    if tiker == 'USDT':
        return config.MIN_AMOUNT
    elif tiker == 'TRX':
         return config.TRX_MIN_AMOUNT
    elif tiker == 'XLM':
         return config.XLM_MIN_AMOUNT
    elif tiker == 'ADA':
         return config.ADA_MIN_AMOUNT
    elif tiker == 'DOGE':
         return config.DOGE_MIN_AMOUNT
    elif tiker == 'MATIC':
         return config.MATIC_MIN_AMOUNT
    elif tiker == 'LUNA':
         return config.LUNA_MIN_AMOUNT
    elif tiker == 'DOT':
         return config.DOT_MIN_AMOUNT
    elif tiker == 'AVAX':
         return config.AVAX_MIN_AMOUNT


def get_comission(tiker):
    if tiker == 'USDT':
        return config.USDT_COMS
    elif tiker == 'TRX':
         return config.TRX_COMS
    elif tiker == 'XLM':
         return config.XLM_COMS
    elif tiker == 'ADA':
         return config.ADA_COMS
    elif tiker == 'DOGE':
         return config.DOGE_COMS
    elif tiker == 'MATIC':
         return config.MATIC_COMS
    elif tiker == 'LUNA':
         return config.LUNA_COMS
    elif tiker == 'DOT':
         return config.DOT_COMS
    elif tiker == 'AVAX':
         return config.AVAX_COMS


def update_limits():
    users = get_all_users()
    for u in users:
        limit = u['limit']
        data = {
            "username": u['username'],
            "token": u['token'],
            "tg_id": u['tg_id'],
            "limit": u['limit'],
            "current_limit": limit,
            "role": u['role']
        }
        requests.put('http://127.0.0.1:8000/user/' + str(u['tg_id']) + '/', json=data)
        time.sleep(1)

def get_user_trades(uid):
    trades = get_trades()
    u_trades = []
    for trade in trades:
        if trade['to_id'] == uid and trade['state'] == 'created':
            u_trades.append(trade)

    return u_trades