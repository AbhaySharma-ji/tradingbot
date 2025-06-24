import tkinter as tk
from tkinter import messagebox
import time
import json
import logging
import os

# ----- Setup Logger -----
def setup_logger():
    logger = logging.getLogger("MockBinanceBot")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("mock_bot.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

logger = setup_logger()

# ----- Mock Bot Class -----
class MockBot:
    def __init__(self):
        self.orders = []
        # Load previous orders if any
        if os.path.exists("orders.json"):
            with open("orders.json", "r") as f:
                self.orders = json.load(f)

    def place_order(self, symbol, side, order_type, quantity, price=None):
        order = {
            "orderId": int(time.time()),
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
            "price": price if order_type.upper() == "LIMIT" else "market price",
            "status": "FILLED" if order_type.upper() == "MARKET" else "NEW",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        self.orders.append(order)
        logger.info(f"Order simulated: {order}")

        # Save to orders.json
        with open("orders.json", "w") as f:
            json.dump(self.orders, f, indent=2)

        return order

# ----- GUI Functionality -----
bot = MockBot()

def place_order():
    symbol = symbol_entry.get().upper()
    side = side_var.get().upper()
    order_type = type_var.get().upper()
    quantity = quantity_entry.get()
    price = price_entry.get()

    if not symbol or not quantity:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    try:
        quantity = float(quantity)
        if order_type == "LIMIT":
            if not price:
                messagebox.showerror("Error", "Please enter a price for LIMIT orders.")
                return
            price_val = float(price)
            order = bot.place_order(symbol, side, order_type, quantity, price_val)
        else:
            order = bot.place_order(symbol, side, order_type, quantity)

        messagebox.showinfo("Order Placed",
                            f"✅ Order saved successfully!\n\n"
                            f"Order ID: {order['orderId']}\n"
                            f"Symbol: {order['symbol']}\n"
                            f"Side: {order['side']}\n"
                            f"Type: {order['type']}\n"
                            f"Status: {order['status']}\n"
                            f"Price: {order['price']}\n"
                            f"Qty: {order['quantity']}")

        # Clear fields
        symbol_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        side_var.set("BUY")
        type_var.set("MARKET")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to place order.\n{e}")

# ----- Build GUI -----
root = tk.Tk()
root.title("🪙 Mock Binance Trading Bot")
root.geometry("360x300")
root.resizable(False, False)

tk.Label(root, text="Symbol (e.g. BTCUSDT):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
symbol_entry = tk.Entry(root)
symbol_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Side:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
side_var = tk.StringVar(value="BUY")
tk.OptionMenu(root, side_var, "BUY", "SELL").grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Order Type:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
type_var = tk.StringVar(value="MARKET")
tk.OptionMenu(root, type_var, "MARKET", "LIMIT").grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Quantity:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Price (for LIMIT):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
price_entry = tk.Entry(root)
price_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Button(root, text="Place Order", command=place_order, bg="green", fg="white").grid(row=5, column=0, columnspan=2, pady=20)

# Run the GUI
root.mainloop()
