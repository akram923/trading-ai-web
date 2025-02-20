import tkinter as tk
from tkinter import messagebox
import MetaTrader5 as mt5

def connect_mt4():
    if not mt5.initialize():
        messagebox.showerror("Erreur", "Connexion à MT4 échouée")
        return False
    messagebox.showinfo("Succès", "Connexion réussie à MT4")
    return True

def execute_trade(action, lot_size):
    symbol = 'EURUSD'
    trade_type = mt5.ORDER_BUY if action == 'BUY' else mt5.ORDER_SELL
    price = mt5.symbol_info_tick(symbol).ask if action == 'BUY' else mt5.symbol_info_tick(symbol).bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": trade_type,
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": "Trade Automatique",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        messagebox.showerror("Erreur", f"Échec du trade: {result.retcode}")
    else:
        messagebox.showinfo("Succès", "Trade exécuté avec succès")

def launch_ui():
    root = tk.Tk()
    root.title("Trading AI")
    root.geometry("300x200")

    tk.Label(root, text="Assistant de Trading", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="Taille du lot :").pack()
    lot_entry = tk.Entry(root)
    lot_entry.insert(0, "0.1")
    lot_entry.pack()

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Button(frame, text="BUY", command=lambda: execute_trade("BUY", float(lot_entry.get())), bg="green", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(frame, text="SELL", command=lambda: execute_trade("SELL", float(lot_entry.get())), bg="red", fg="white").pack(side=tk.RIGHT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    if connect_mt4():
        launch_ui()

