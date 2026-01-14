import MetaTrader5 as mt5

if not mt5.initialize(path="C:\\Program Files\\MetaTrader 5\\terminal64.exe"):
    quit()

def print_info(symbol_name):
    print(f"\n--- {symbol_name} ---")
    info = mt5.symbol_info(symbol_name)
    if not info:
        print("Not Found")
        return
        
    # Safer print
    data = info._asdict()
    print(f"Contract Size: {data.get('trade_contract_size', data.get('contract_size'))}")
    print(f"Tick Value: {data.get('trade_tick_value')}")
    print(f"Min Volume: {data.get('volume_min')}")
    print(f"Trade Mode: {data.get('trade_mode')}")

# 1. Inspect NQ_H
print_info("NQ_H")

# 2. Try to add ND100m
if mt5.symbol_select("ND100m", True):
    print("\nSuccessfully selected ND100m!")
    print_info("ND100m")
else:
    print("\nCould not select ND100m")

mt5.shutdown()
