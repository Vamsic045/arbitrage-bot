from exchanges import get_price_binance, get_price_coindcx, get_price_bitget

ask_b, bid_b = get_price_binance()
ask_c, bid_c = get_price_coindcx()
ask_g, bid_g = get_price_bitget()

print(f"Binance: Ask - {ask_b}, Bid - {bid_b}")
print(f"CoinDCX: Ask - {ask_c}, Bid - {bid_c}")
print(f"Bitget: Ask - {ask_g}, Bid - {bid_g}")
