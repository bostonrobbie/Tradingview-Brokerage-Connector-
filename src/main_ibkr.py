import sys
import os
import signal
import asyncio

# Ensure src in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ib_executor
import webhook_listener

def main():
    print("=========================================")
    print("   TradingView to IBKR Bridge (Async)    ")
    print("=========================================")
    
    # Attempt initial connection in background loop usually, 
    # but here we rely on the webhook triggering it or pre-connect.
    # Since Flask is blocking, we need to run Flask. 
    # The 'ib_executor' handles the asyncio loop usage via ib.run() wrapper.
    
    # Note: ib_insync/async typically wants to run the loop. 
    # We will use the Webhook listener's Flask runner which is sync, 
    # and use ib.run() to invoke async commands.
    
    try:
        # Attempt initial connection
        print("[INFO] Attempting initial connection to IBKR (7497)...")
        try:
            ib_executor.ib.run(ib_executor.connect_ib())
        except Exception as e:
            print(f"[WARN] Initial connection failed: {e}")

        webhook_listener.start_server()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
    finally:
        ib_executor.disconnect()

if __name__ == "__main__":
    main()
