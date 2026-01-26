# Interactive Brokers (IBKR) Bridge

This bridge connects TradingView to **Trader Workstation (TWS)** or **IB Gateway**.

## 1. Prerequisites
1.  **Install TWS**: Download "Trader Workstation" from Interactive Brokers.
2.  **Enable API in TWS**:
    *   Open TWS -> File -> Global Configuration.
    *   Go to **API** -> **Settings**.
    *   **Check**: "Enable ActiveX and Socket Clients".
    *   **Uncheck**: "Read-Only API".
    *   **Port**: 
        *   **7497** = Paper Trading (Demo)
        *   **7496** = Live Trading (Real Money)
    *   **NOTE**: You must update `src/config/settings.json` if you switch!

## 2. Installation
Run inside this folder:
```bash
pip install -r requirements.txt
```

## 3. Usage
Double-click **`launch_everything.bat`**.
(This starts TWS, the Bridge, and the Tunnel automatically).

## 4. Configuration
*   **Symbol format**: IBKR uses detailed contracts.
    *   Forex: `EURUSD` (Defaults to "CASH", "IDEALPRO").
    *   Stock: `AAPL` (Must set `sec_type` to "STK" in JSON payload).

## 5. Webhook Payload Examples
Set your TradingView Webhook to:
**`https://bostonrobbie-ibkr.loca.lt/webhook`**

### Forex Example
```json
{
    "secret": "fd70ac19-6154-4354-a8ba-b345b511ed93",
    "action": "BUY",
    "symbol": "EURUSD",
    "volume": 20000, 
    "secType": "CASH",
    "currency": "USD",
    "exchange": "IDEALPRO"
}
```

### Micro NQ (MNQ) Futures Example
Use `secType: "FUT"` and `symbol: "MNQ"`. The bridge automatically finds the "Front Month" contract.

```json
{
    "secret": "fd70ac19-6154-4354-a8ba-b345b511ed93",
    "action": "BUY",
    "symbol": "MNQ",
    "volume": 1, 
    "secType": "FUT",
    "currency": "USD",
    "exchange": "GLOBEX"
}
```

### Universal Strategy Payload (Entries & Exits)
If you use a **TradingView Strategy** (not simple alerts), use this **Single JSON** for everything. TradingView will automatically replace `{{...}}` with the correct Buy/Sell/Close action.

```json
{
    "secret": "fd70ac19-6154-4354-a8ba-b345b511ed93",
    "action": "{{strategy.order.action}}",
    "symbol": "MNQ",
    "volume": "{{strategy.order.contracts}}",
    "secType": "FUT",
    "exchange": "GLOBEX",
    "currency": "USD"
}
```
*Paste this into the **"Message"** field of your "Create Alert" -> "Strategy" window.*
