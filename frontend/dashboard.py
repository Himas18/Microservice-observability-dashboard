import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_BASE = "http://backend:8059"

st.set_page_config(page_title="Service Dashboard", layout="wide")
st.title("Microservice Status Tracker")

# Refresh button
if st.button(" Refresh Service Snapshot"):
    response = requests.post(f"{API_BASE}/refresh")
    if response.status_code == 200:
        st.success("Snapshot refreshed!")
    else:
        st.error("Failed to refresh services.")

# Optional filter
name_filter = st.text_input("🔍Filter by Service Name")

# Fetch service status 
try:
    params = {"exclude_common": True}
    if name_filter:
        params["name_filter"] = name_filter
    r = requests.get(f"{API_BASE}/status", params=params)
    data = r.json()

    if data:
        st.subheader("📊 Active Services")
        df = pd.DataFrame(data)
        df["last_updated"] = pd.to_datetime(df["last_updated"]).dt.strftime("%Y-%m-%d %H:%M:%S")

        # Color-coded status
        def color_status(val):
            return "background-color: #90ee90" if val == "up" else "background-color: #f08080"

        styled_df = df.style.applymap(color_status, subset=["status"])

        st.dataframe(styled_df, use_container_width=True)

        # Download CSV
        with st.spinner("Preparing CSV..."):
            csv_response = requests.get(f"{API_BASE}/report_csv")
            if csv_response.status_code == 200:
                st.download_button(
                    label="📥 Download CSV Report",
                    data=csv_response.content,
                    file_name="services_report.csv",
                    mime="text/csv"
                )
    else:
        st.warning("No service data found.")
except Exception as e:
    st.error(f"Couldn't fetch service data: {e}")

# Health check
try:
    r = requests.get(f"{API_BASE}/health")
    uptime = r.json().get("uptime_seconds", 0)
    st.caption(f"🩺 Uptime: {int(uptime)} seconds")
except:
    st.caption("❌ Health check failed.")