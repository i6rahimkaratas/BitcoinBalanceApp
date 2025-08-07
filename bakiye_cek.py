import requests


def get_crypto_prices():
  
    ids = [
        "bitcoin", "ethereum", "litecoin", "solana", "tether", "binancecoin",
        "usd-coin", "dogecoin", "cardano", "tron", "the-open-network", "ripple"
    ]
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&vs_currencies=usd"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None




def get_balance_blockcypher(address, coin_symbol):
    """BTC, ETH, LTC, DOGE gibi coinler için bakiye çeker."""
    units = {
        'btc': 100_000_000,
        'eth': 1_000_000_000_000_000_000,
        'ltc': 100_000_000,
        'doge': 100_000_000
    }
    try:
        url = f"https://api.blockcypher.com/v1/{coin_symbol}/main/addrs/{address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance = data.get('balance', 0) / units[coin_symbol]
        return balance
    except Exception:
        return None


def get_balance_bnb(address):
    """BNB ana coininin bakiyesini çeker."""
    try:
        url = f"https://api.bscscan.com/api?module=account&action=balance&address={address}&tag=latest"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == '1':
            return int(data['result']) / 1_000_000_000_000_000_000
        return 0
    except Exception:
        return None

def get_balance_bep20_token(wallet_address, token_contract_address):
    
    try:
        url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={token_contract_address}&address={wallet_address}&tag=latest"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == '1':
            
            return int(data['result']) / 1_000_000_000_000_000_000 
        return 0
    except Exception:
        return None


def get_balance_sol(address):
    """SOL bakiyesini çeker (Public RPC kullanarak)."""
    try:
        url = "https://api.mainnet-beta.solana.com"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [address]
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        balance_lamports = data['result']['value']
        return balance_lamports / 1_000_000_000 
    except Exception:
        return None

def get_balance_ada(address):
    
    try:
        url = f"https://api.blockchair.com/cardano/dashboards/address/{address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance_lovelace = data['data'][address]['address']['balance']
        return balance_lovelace / 1_000_000 
    except Exception:
        return None

def get_balance_trx(address):
    """TRX (Tron) bakiyesini TronGrid API'si ile çeker."""
    try:
        url = f"https://api.trongrid.io/v1/accounts/{address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['data']:
            return data['data'][0].get('balance', 0) / 1_000_000 
        return 0
    except Exception:
        return None

def get_balance_ton(address):
    """TON (Toncoin) bakiyesini Toncenter API'si ile çeker."""
    try:
        url = f"https://toncenter.com/api/v2/getAddressBalance?address={address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return int(data['result']) / 1_000_000_000 
    except Exception:
        return None

def get_balance_xrp(address):
    
    try:
        url = f"https://api.xrpscan.com/api/v1/account/{address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data.get('xrpBalance', 0))
    except Exception:
        return None


# Kripto para adresleri
addresses = {
    'btc': "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo",
    'eth': "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    'ltc': "ltc1qg0gxwpladdaaa3j5sv36ldc83pch2pyz4j4esm",
    'sol': "2Z2P82u3aY4YdCwg2RVd2uA32K22p2G4bYAaCey21j2a",
    'usdt_bep20': "0x4764e1E2133435565543545a25b39B3b9981883e",
    'bnb': "0x4764e1E2133435565543545a25b39B3b9981883e",
    'usdc_bep20': "0x4764e1E2133435565543545a25b39B3b9981883e",
    'doge': "D8L2hS34nURa1Tvr2sBLh3a1F6PabZq4rB",
    'ada': "addr1qx2szrqmyz2jwz2m5g2a5cc4y2a2g73d2gdgqct2k42vza2addaa3j5sv36ldc83pch2pyz4j4esu2l2f0xrha4q2z2sg5d2n9",
    'trx': "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
    'ton': "EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N",
    'xrp': "rPdvC6ccq8hCdPKSPJkPmyZ4Mi1oG2FFkT"
}


bep20_contracts = {
    'usdt': '0x55d398326f99059fF775485246999027B3197955',
    'usdc': '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d'
}


coins_to_check = [
    {'logo': '₿ ', 'name': 'BTC', 'func': lambda: get_balance_blockcypher(addresses['btc'], 'btc'), 'price_id': 'bitcoin'},
    {'logo': '⧫ ', 'name': 'ETH', 'func': lambda: get_balance_blockcypher(addresses['eth'], 'eth'), 'price_id': 'ethereum'},
    {'logo': 'Ł ', 'name': 'LTC', 'func': lambda: get_balance_blockcypher(addresses['ltc'], 'ltc'), 'price_id': 'litecoin'},
    {'logo': '♦ ', 'name': 'BNB', 'func': lambda: get_balance_bnb(addresses['bnb']), 'price_id': 'binancecoin'},
    {'logo': '✕ ', 'name': 'XRP', 'func': lambda: get_balance_xrp(addresses['xrp']), 'price_id': 'ripple'},
    {'logo': '◎ ', 'name': 'SOL', 'func': lambda: get_balance_sol(addresses['sol']), 'price_id': 'solana'},
    {'logo': '₮ ', 'name': 'USDT', 'func': lambda: get_balance_bep20_token(addresses['usdt_bep20'], bep20_contracts['usdt']), 'price_id': 'tether'},
    {'logo': 'C ', 'name': 'ADA', 'func': lambda: get_balance_ada(addresses['ada']), 'price_id': 'cardano'},
    {'logo': 'Ð ', 'name': 'DOGE', 'func': lambda: get_balance_blockcypher(addresses['doge'], 'doge'), 'price_id': 'dogecoin'},
    {'logo': 'T ', 'name': 'TRX', 'func': lambda: get_balance_trx(addresses['trx']), 'price_id': 'tron'},
    {'logo': 'O ', 'name': 'TON', 'func': lambda: get_balance_ton(addresses['ton']), 'price_id': 'the-open-network'},
    {'logo': 'U ', 'name': 'USDC', 'func': lambda: get_balance_bep20_token(addresses['usdc_bep20'], bep20_contracts['usdc']), 'price_id': 'usd-coin'},
]



print("Cüzdan bakiyeleri alınıyor, lütfen bekleyin...")
print("-" * 60)

prices = get_crypto_prices()

if not prices:
    print("Hata: Kripto para fiyatları alınamadı. Lütfen internet bağlantınızı kontrol edin.")
else:
    for coin in coins_to_check:
        balance = coin['func']()
        price_info = prices.get(coin['price_id'], {})
        price = price_info.get('usd')

        if balance is not None and price is not None:
            usd_value = balance * price
            print(f"{coin['logo']} {coin['name']:<5} Bakiye:")
            print(f"   {balance:.8f} {coin['name']} (${usd_value:,.2f} USD)")
            print() 
        else:
            print(f"{coin['logo']} {coin['name']:<5} Bakiye: Bilgiler alınamadı.")
            print()


print("-" * 60)
