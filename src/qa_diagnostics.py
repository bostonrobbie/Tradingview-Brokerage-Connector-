import os
import json
import requests
import sys

def check_file(path, name):
    if os.path.exists(path):
        print(f"[PASS] {name} found at {path}")
        return True
    else:
        print(f"[FAIL] {name} NOT found at {path}")
        return False

def check_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.json')
    if check_file(config_path, "Settings JSON"):
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
                print(f"[PASS] Config loaded. Port: {data.get('ibkr', {}).get('port')}")
        except Exception as e:
            print(f"[FAIL] Config invalid: {e}")

def check_server_health():
    url = "http://127.0.0.1:5001/status"
    try:
        print(f"[*] Pinging Bridge Server at {url}...")
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            state = data.get("state", {})
            print(f"[PASS] Server is UP.")
            print(f"       - IBKR Connected: {state.get('ibkr_connected')}")
            print(f"       - Last Trade: {state.get('last_trade')}")
            print(f"       - Uptime Start: {state.get('uptime_start')}")
        else:
            print(f"[FAIL] Server returned status code {resp.status_code}")
    except Exception as e:
        print(f"[WARN] Server not reachable (Is it running?): {e}")

import socket

def check_tws_ports():
    print("\n[*] Checking TWS API Ports (Direct Socket Check)...")
    ports = [7496, 7497]
    found = False
    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            result = s.connect_ex(('127.0.0.1', p))
            if result == 0:
                print(f"[PASS] Port {p} is OPEN. TWS is listening.")
                found = True
            else:
                print(f"[FAIL] Port {p} is CLOSED.")
            s.close()
        except Exception as e:
            print(f"[ERR] Could not check port {p}: {e}")
    
    if not found:
        print("\n[!!!] CRITICAL FAILURE: TWS is NOT answering.")
        print("      The Bridge code is fine, but TWS has the door locked.")
        print("      FIX:")
        print("      1. TWS -> File -> Global Configuration -> API -> Settings.")
        print("      2. CHECK 'Enable ActiveX and Socket Clients'.")
        print("      3. UNCHECK 'Read-Only API'.")
        print("      4. Click 'Apply' and 'OK'.")
        print("      5. Restart TWS may be required.")
    else:
        print("\n[OK] TWS / Gateway is accessible.")

if __name__ == "__main__":
    print("=== IBKR BRIDGE QA DIAGNOSTICS ===")
    check_config()
    check_file("bridge.log", "Log File")
    check_server_health()
    check_tws_ports()
    print("==================================")
    print("Press Enter to close...")
    input()
