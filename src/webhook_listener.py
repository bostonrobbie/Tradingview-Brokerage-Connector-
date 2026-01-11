from flask import Flask, request, jsonify
import ib_executor
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Webhook")

app = Flask(__name__)
SETTINGS = ib_executor.SETTINGS
SECURITY_CONFIG = SETTINGS.get('security', {})
SERVER_CONFIG = SETTINGS.get('server', {})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data"}), 400

    # Security Check
    incoming_secret = data.get('secret')
    configured_secret = SECURITY_CONFIG.get('webhook_secret')
    if configured_secret and incoming_secret != configured_secret:
         return jsonify({"status": "error", "message": "Unauthorized"}), 401

    logger.info(f"Received IBKR Webhook: {data}")

    try:
        # Check payload for IBKR specific fields or map them
        # IBKR uses 'volume' (quantity) differently than MT5 (lots). 
        # Ideally user sends 'volume': 20000 for 20k units.
        
        result = ib_executor.execute_trade_sync_wrapper(data)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Advanced Health Check endpoint."""
    is_connected = ib_executor.check_health_sync()
    status = "connected" if is_connected else "disconnected"
    return jsonify({
        "status": status, 
        "service": "IBKR Bridge", 
        "advanced_mode": True
    }), 200 if is_connected else 503

def start_server():
    host = SERVER_CONFIG.get('host', '0.0.0.0')
    # Use different port 5001 to avoid conflict if running both bridges
    port = SERVER_CONFIG.get('port', 5001) 
    debug = SERVER_CONFIG.get('debug', False)
    
    logger.info(f"Starting IBKR Webhook Server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
