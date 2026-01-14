import MetaTrader5 as mt5
import time
import json
import os

# --- HARDCODED CREDENTIALS FOR FIRST TEST ---
LOGIN = 4000082688
PASSWORD = "@JILLson9"
SERVER = "Darwinex-Live"
PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

print("========================================")
print("   MT5 CONNECTION DIAGNOSTIC TOOL       ")
print("========================================")
print(f"Target: {LOGIN} on {SERVER}")
print(f"Path: {PATH}")

print("\n[STEP 1] Initialization...")
# Attempt 1: Just Initialize (attach if running, launch if not)
if not mt5.initialize(path=PATH):
    print(f"[FAIL] initialize() failed: {mt5.last_error()}")
    if mt5.last_error() == (-10005, 'IPC timeout'):
        print("\n!!! IPC TIMEOUT DETECTED !!!")
        print("Causes:")
        print("1. 'Algo Trading' button is OFF (Red/Play icon).")
        print("2. MT5 is running as Admin (script is User).")
        print("3. MT5 is stuck on a Login/Update dialog.")
    quit()

print("[PASS] MT5 Initialized (IPC communication established).")

print("\n[STEP 2] Login...")
if not mt5.login(login=LOGIN, password=PASSWORD, server=SERVER):
    print(f"[FAIL] login() failed: {mt5.last_error()}")
    quit()

print(f"[PASS] Logged in successfully!")

print("\n[STEP 3] Account Info...")
info = mt5.account_info()
if info:
    print(f"  - Balance: {info.balance} {info.currency}")
    print(f"  - Leverage: 1:{info.leverage}")
    print(f"  - Company: {info.company}")
    print(f"  - Trade Allowed: {info.trade_allowed}")
    print(f"  - Trade Expert: {info.trade_expert} (This is 'Algo Trading' status!)")
    
    if not info.trade_expert:
        print("\n[WARNING] 'Algo Trading' is DISABLED on the account level!")
        print("Please click the 'Algo Trading' button in MT5 toolbar.")
else:
    print("[FAIL] Could not get account info.")

print("\n[SUCCESS] DIAGNOSTIC COMPLETE. You are ready to run the bridge.")
input("\nPress Enter to exit...")
mt5.shutdown()
