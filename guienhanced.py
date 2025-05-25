import tkinter as tk
from tkinter import messagebox
from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging


logging.basicConfig(filename='trading_bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class BasicBot:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret, testnet=True)
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com'

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='MARKET',
                quantity=quantity
            )
            logging.info(f"Market order placed: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"Market order error: {e}")
            raise

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            logging.info(f"Limit order placed: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"Limit order error: {e}")
            raise

    def place_stop_limit_order(self, symbol, side, quantity, stop_price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='STOP_MARKET',
                stopPrice=stop_price,
                closePosition=False,
                quantity=quantity,
                timeInForce='GTC'
            )
            logging.info(f"Stop-limit order placed: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"Stop-limit order error: {e}")
            raise

    def cancel_order(self, symbol, order_id):
        try:
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=int(order_id)
            )
            logging.info(f"Order canceled: {result}")
            return result
        except BinanceAPIException as e:
            logging.error(f"Cancel order error: {e}")
            raise

    def get_position(self, symbol):
        try:
            return self.client.futures_position_information(symbol=symbol)
        except BinanceAPIException as e:
            raise

    def get_balance(self):
        try:
            return self.client.futures_account_balance()
        except BinanceAPIException as e:
            raise



def launch_gui(bot):
    win = tk.Tk()
    win.title("Binance Futures Bot")
    win.geometry("400x600")
    win.configure(bg="#f5f5f5")

    def get(e): return e.get().strip()

    
    tk.Label(win, text="Symbol (e.g., BTCUSDT)").pack()
    sym = tk.Entry(win); sym.pack()

    tk.Label(win, text="Side (BUY/SELL)").pack()
    side = tk.Entry(win); side.pack()

    tk.Label(win, text="Quantity").pack()
    qty = tk.Entry(win); qty.pack()

    tk.Label(win, text="Limit Price").pack()
    price = tk.Entry(win); price.pack()

    tk.Label(win, text="Stop Price").pack()
    stop = tk.Entry(win); stop.pack()

    tk.Label(win, text="Order ID (to Cancel)").pack()
    oid = tk.Entry(win); oid.pack()

    def msg(title, text): messagebox.showinfo(title, text)

    # Button actions
    def market():
        try:
            o = bot.place_market_order(get(sym), get(side), get(qty))
            msg("Market Order", f"Order ID: {o['orderId']}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def limit():
        try:
            o = bot.place_limit_order(get(sym), get(side), get(qty), get(price))
            msg("Limit Order", f"Order ID: {o['orderId']}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def stop_limit():
        try:
            o = bot.place_stop_limit_order(get(sym), get(side), get(qty), get(stop))
            msg("Stop Order", f"Order ID: {o['orderId']}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def cancel():
        try:
            o = bot.cancel_order(get(sym), get(oid))
            msg("Cancelled", f"Order ID: {o['orderId']}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def balance():
        try:
            b = bot.get_balance()
            msg("Balance", str(b))
        except Exception as e: messagebox.showerror("Error", str(e))

    def position():
        try:
            p = bot.get_position(get(sym))
            msg("Position", str(p))
        except Exception as e: messagebox.showerror("Error", str(e))

    
    for (text, cmd) in [
        ("Market Order", market),
        ("Limit Order", limit),
        ("Stop-Limit Order", stop_limit),
        ("Cancel Order", cancel),
        ("View Balance", balance),
        ("View Position", position)
    ]:
        tk.Button(win, text=text, command=cmd).pack(pady=5)

    win.mainloop()



api_key = 'MYAPIKEY'
api_secret = 'MYAPISECRETKEY'
bot = BasicBot(api_key, api_secret)
launch_gui(bot)
