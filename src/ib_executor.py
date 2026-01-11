from ib_async import *
import json
import os
import asyncio
import logging

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IB_Executor")

ib = IB()

# Load settings
def load_settings():
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.json')
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"[ERROR] Failed to load settings: {e}")
        return {}

SETTINGS = load_settings()
IBKR_CONFIG = SETTINGS.get('ibkr', {})
TRADING_CONFIG = SETTINGS.get('trading', {})

async def connect_ib():
    """Connects to TWS or IB Gateway."""
    host = IBKR_CONFIG.get('host', '127.0.0.1')
    port = int(IBKR_CONFIG.get('port', 7497))
    client_id = int(IBKR_CONFIG.get('client_id', 1))

    if not ib.isConnected():
        logger.info(f"Connecting to IBKR {host}:{port} ClientID:{client_id}...")
        try:
            await ib.connectAsync(host, port, clientId=client_id)
            logger.info("Connected to Interactive Brokers!")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    return True

def get_contract(symbol, sec_type, currency, exchange):
    """Creates a contract object."""
    if sec_type == 'CASH':
        # Split EURUSD -> EUR, USD
        # Simple heuristic: First 3 chars base, next 3 quote
        if len(symbol) == 6:
            base = symbol[:3]
            quote = symbol[3:]
            return Forex(base, quote)
        return Forex(symbol) # Fallback
    elif sec_type == 'STK':
        return Stock(symbol, exchange, currency)
    elif sec_type == 'CRYPTO':
         return Crypto(symbol, exchange, currency)
    else:
        # Generic fallback
        return Contract(symbol=symbol, secType=sec_type, exchange=exchange, currency=currency)

async def execute_trade_async(data):
    """Executes a trade asynchronously."""
    if not ib.isConnected():
        logger.warning("IB Not connected, attempting to connect...")
        connected = await connect_ib()
        if not connected:
             return {"status": "error", "message": "Could not connect to IBKR"}

    action = data.get('action', TRADING_CONFIG.get('default_action', 'BUY')).upper()
    symbol = data.get('symbol', TRADING_CONFIG.get('default_symbol', 'EURUSD')).upper()
    quantity = float(data.get('volume', TRADING_CONFIG.get('default_quantity', 10000))) # IB uses 'quantity' (shares/contracts), TV sends 'volume' (lots usually) - User must configure logic
    
    # Contract Construction
    sec_type = data.get('secType', TRADING_CONFIG.get('default_sec_type', 'CASH'))
    exchange = data.get('exchange', TRADING_CONFIG.get('default_exchange', 'IDEALPRO'))
    currency = data.get('currency', TRADING_CONFIG.get('default_currency', 'USD'))

    contract = get_contract(symbol, sec_type, currency, exchange)
    
    # Order Construction
    # Using Market order for simplicity in this bridge V1
    order = MarketOrder(action, quantity)
    
    # Optional: Attach Stop Loss / Take Profit
    # IBKR "Bracket Orders" are complex, for V1 we just place the main order.
    # Future enhancement: Bracket orders.
    
    logger.info(f"Placing Order: {action} {quantity} {symbol}")
    
    try:
        trade = ib.placeOrder(contract, order)
        # We don't wait for fill in this webhook response to keep it fast, 
        # but we wait for it to be 'submitted' to TWS.
        await asyncio.sleep(0.5) 
        
        return {
            "status": "success",
            "message": "Order Submitted",
            "order_id": trade.order.orderId,
            "status_ib": trade.orderStatus.status
        }
    except Exception as e:
        logger.error(f"Order placement error: {e}")
        return {"status": "error", "message": str(e)}

def execute_trade_sync_wrapper(data):
    """Wrapper to call async function from sync Flask context."""
    return ib.run(execute_trade_async(data))

def check_health_sync():
    """Checks connection status."""
    return ib.isConnected()

def disconnect():
    ib.disconnect()
