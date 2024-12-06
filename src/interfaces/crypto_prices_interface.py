import threading
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from services.binance_service import (crypto_search,
                                      check_crypto_price)

from config import (LABEL_PAIRS, LABEL_TEXTS,
                    GUI_COLORS, PAIRS_AND_VARIABLES)

class CryptoPricesApp:
    def __init__(self):
        self.root = Tk()
        self.setup_window()
        self.setup_frame()
        self.setup_labels()
        self.start_price_updates()

    def setup_window(self):
        self.root.title("Crypto-Prices")
        self.root.resizable(0, 0)
        self.root.iconbitmap("media/btc.ico")
        self.root.config(bg=GUI_COLORS["root"])

    def setup_frame(self):
        self.frame = Frame(self.root, bg="#4D506B", padx=10, pady=10)
        self.frame.pack(padx=10, pady=10)

    def setup_labels(self):
        self.title_label = ttk.Label(
            self.frame, text=LABEL_TEXTS["TITLE"],
            font=("", 70), background=GUI_COLORS["frame"]
        )
        self.title_label.grid(row=1, columnspan=4)

        self.search_label = ttk.Label(
            self.frame, text=LABEL_TEXTS["SEARCH"],
            font=("", 25), background=GUI_COLORS["frame"]
        )
        self.search_label.grid(row=2, columnspan=4)

        self.search_entry = Entry(
            self.frame, width=20, font=("", 25), justify="center",
            background=GUI_COLORS["root"], fg=GUI_COLORS["fg"]
        )
        self.search_entry.grid(row=3, columnspan=4)

        self.search_image = Image.open(
            "media/boton_buscar.png"
        ).resize((40,40), Image.Resampling.LANCZOS)

        self.img = ImageTk.PhotoImage(self.search_image)

        self.search_button = Button(
            self.frame, image=self.img, border=0,
            bg=GUI_COLORS["frame"], activebackground=GUI_COLORS["frame"],
            cursor="hand2", command=self.set_searched_crypto,
        )
        self.search_button.grid(row=3, column=3)

        self.searched_crypto = StringVar()
        self.searched_crypto_label = ttk.Label(
            self.frame, textvariable=self.searched_crypto,
            background=GUI_COLORS["frame"], foreground=GUI_COLORS["fg"],
            font=("", 15)
        )
        self.searched_crypto_label.grid(row=5, columnspan=4)

        self.spot_label = ttk.Label(
            self.frame, font=("", 25),
            text=LABEL_TEXTS["SPOT"], background=GUI_COLORS["frame"]
        )
        self.spot_label.grid(row=6, columnspan=4)

        self.pair_label = ttk.Label(
            self.frame, font=("", 20),
            text=LABEL_TEXTS["PAIR"], background=GUI_COLORS["frame"]
        )
        self.pair_label.grid(row=7, column=0)

        self.price_label = ttk.Label(
            self.frame, font=("", 20),
            text=LABEL_TEXTS["PRICE"], background=GUI_COLORS["frame"]
        )
        self.price_label.grid(row=7, column=3)

        self.btc_label = ttk.Label(
            self.frame, font=("", 20),
            text=LABEL_PAIRS["BTC"], background=GUI_COLORS["frame"],
            foreground=GUI_COLORS["fg"]
        )
        self.btc_label.grid(row=8, column=0)

        self.btc_act = StringVar()
        self.btc_price_label = ttk.Label(
            self.frame, textvariable=self.btc_act, font=("", 20),
            background=GUI_COLORS["frame"], foreground=GUI_COLORS["fg"]
        )
        self.btc_price_label.grid(row=8, column=3)

        self.eth_label = ttk.Label(
            self.frame, font=("", 20),
            text=LABEL_PAIRS["ETH"], background=GUI_COLORS["frame"],
            foreground=GUI_COLORS["fg"]
        )
        self.eth_label.grid(row=9, column=0)

        self.eth_act = StringVar()
        self.eth_price_label = ttk.Label(
            self.frame, textvariable=self.eth_act, font=("", 20),
            background=GUI_COLORS["frame"], foreground=GUI_COLORS["fg"]
        )
        self.eth_price_label.grid(row=9, column=3)

        self.ada_label = ttk.Label(
            self.frame, font=("", 20),
            text=LABEL_PAIRS["ADA"], background=GUI_COLORS["frame"],
            foreground=GUI_COLORS["fg"]
        )
        self.ada_label.grid(row=10, column=0)

        self.ada_act = StringVar()
        self.ada_price_label = ttk.Label(
            self.frame, textvariable=self.ada_act, font=("", 20),
            background=GUI_COLORS["frame"], foreground=GUI_COLORS["fg"]
        )
        self.ada_price_label.grid(row=10, column=3)

        self.link_label = ttk.Label(
            self.frame, font=("", 20),
            text=LABEL_PAIRS["LINK"], background=GUI_COLORS["frame"],
            foreground=GUI_COLORS["fg"]
        )
        self.link_label.grid(row=11, column=0)

        self.link_act = StringVar()
        self.link_price_label = ttk.Label(
            self.frame, textvariable=self.link_act, font=("", 20),
            background=GUI_COLORS["frame"], foreground=GUI_COLORS["fg"]
        )
        self.link_price_label.grid(row=11, column=3)

        self.sol_label = ttk.Label(
            self.frame, font=("", 20),
            text=LABEL_PAIRS["SOL"], background=GUI_COLORS["frame"],
            foreground=GUI_COLORS["fg"]
        )
        self.sol_label.grid(row=12, column=0)

        self.sol_act = StringVar()
        self.sol_price_label = ttk.Label(
            self.frame, textvariable=self.sol_act, font=("", 20),
            background=GUI_COLORS["frame"], foreground=GUI_COLORS["fg"]
        )
        self.sol_price_label.grid(row=12, column=3)

        self.bnb_label = ttk.Label(
            self.frame, font=("", 20),
            text=LABEL_PAIRS["BNB"], background=GUI_COLORS["frame"],
            foreground=GUI_COLORS["fg"]
        )
        self.bnb_label.grid(row=13, column=0)

        self.bnb_act = StringVar()
        self.bnb_price_label = ttk.Label(
            self.frame, textvariable=self.bnb_act, font=("", 20),
            background=GUI_COLORS["frame"], foreground=GUI_COLORS["fg"]
        )
        self.bnb_price_label.grid(row=13, column=3)

    def set_searched_crypto(self):
        pair = self.search_entry.get().upper()
        try:
            thread = threading.Thread(target=crypto_search,
                                      args=(pair, self.searched_crypto),
                                      daemon=True)
            thread.start()

        except Exception as e:
            print(f"Error creando el hilo de {pair}: {e}")
            self.searched_crypto.set("Error en la busqueda")

    def start_price_updates(self):

        for pair, variable_name in PAIRS_AND_VARIABLES.items():
            try:
                variable = getattr(self, variable_name)
                thread = threading.Thread(target=check_crypto_price,
                                          args=(pair, variable),
                                          daemon=True)
                thread.start()

            except Exception as e:
                print(f"Error creando el hilo de {pair}: {e}")

        self.root.after(2000, self.start_price_updates)

    def run(self):
        self.root.mainloop()
