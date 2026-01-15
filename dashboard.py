import streamlit as st
import requests
import pandas as pd
import time
import json

st.set_page_config(page_title="IBKR Bridge Monitor", page_icon="📈", layout="wide")

st.title("🌉 IBKR Bridge Monitor")

# Auto-Refresh
count = st.empty()
if st.button("Refresh Now"):
    pass

STATUS_URL = "http://127.0.0.1:5001/status"

def get_status():
    try:
        r = requests.get(STATUS_URL, timeout=2)
        if r.status_code == 200:
            return r.json(), True
    except:
        pass
    return None, False

data, online = get_status()

# Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Bridge Server")
    if online:
        st.success("ONLINE")
    else:
        st.error("OFFLINE")

with col2:
    st.subheader("IBKR Connection")
    if online and data.get("state", {}).get("ibkr_connected"):
        st.success("CONNECTED")
    else:
        st.error("DISCONNECTED")

with col3:
    st.subheader("Last Trade")
    last_trade = data.get("state", {}).get("last_trade", "None") if online else "Unknown"
    st.info(last_trade)

st.divider()

if online:
    st.subheader("📜 Live Logs")
    logs = data.get("logs", [])
    if logs:
        # Clean logs
        log_data = []
        for line in logs:
            try:
                # Basic parsing if format is known, otherwise raw
                log_data.append({"Log Message": line.strip()})
            except:
                pass
        
        df = pd.DataFrame(log_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No logs found.")
        
    st.subheader("🔍 Bridge State")
    st.json(data.get("state", {}))

else:
    st.warning("Cannot reach Bridge Server. Ensure 'launch_everything.bat' is running.")

# Auto-rerun
time.sleep(3)
st.rerun()
