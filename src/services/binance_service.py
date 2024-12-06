from binance.spot import Spot


client = Spot()


def crypto_search(pair, variable):
    try:
        search = client.ticker_price(pair)
        crypto_symbol = search.get("symbol")
        crypto_price = float(search.get("price"))

        variable.set(f"{crypto_symbol}: {crypto_price}$")

    except Exception as e:
        print(f"Error con api binance: {e}")
        variable.set("Par invalido o vacio")


def check_crypto_price(pair, variable):
    try:
        crypto = client.ticker_price(pair)
        crypto_price = float(crypto.get("price"))
        variable.set(f"{crypto_price:,}")

    except Exception as e:
        print(f"Error con {pair}: {e}")
