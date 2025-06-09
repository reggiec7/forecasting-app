# forecasting_app.py

# Install required packages (use in setup or notebook environment)
# !pip install streamlit pandas prophet azure-storage-blob plotly

import streamlit as st
import pandas as pd
from prophet import Prophet
from azure.storage.blob import BlobServiceClient
import io
import plotly.graph_objs as go
from prophet.plot import plot_plotly
import numpy as np
from datetime import datetime

# -----------------------------------------------
# 1. Page Setup & Intro
# -----------------------------------------------
st.set_page_config(
    page_title="BizForecast – Demand Forecasting Tool",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("📦 BizForecast")
st.markdown("### AI-Powered Demand Forecasting Web App")
st.markdown(
    """
    Upload your sales data to generate a demand forecast using Facebook Prophet.
    This tool is ideal for business analysts, planners, and inventory managers.
    """
)

st.markdown("---")

# Optional: collapsible instructions
with st.expander("ℹ️ How to Use This App", expanded=False):
    st.markdown("""
    **1. Upload a CSV file** with at least three columns:  
    - `Date`: format like `YYYY-MM-DD`  
    - `Demand`: daily or aggregated demand quantity  
    - `Product ID`: for product-specific forecasts

    **2. Enter your contact info (optional but recommended)**

    **3. Choose how far ahead to forecast**

    **4. View the interactive chart and download forecast results**

    🔐 Your data is temporarily uploaded to secure Azure Blob Storage.
    """)

# -----------------------------------------------
# 2. Azure Blob Storage Setup
# -----------------------------------------------
AZURE_CONNECTION_STRING = st.secrets["AZURE_STORAGE_CONNECTION_STRING"]
CONTAINER_NAME = "forecast-input"
CONTACT_CONTAINER = "user-contact"
LOG_CONTAINER = "forecast-logs"

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

# Auto-create required containers if they don't exist
required_containers = [CONTAINER_NAME, CONTACT_CONTAINER, LOG_CONTAINER]
for cname in required_containers:
    try:
        blob_service_client.create_container(cname)
    except Exception as e:
        if "ContainerAlreadyExists" not in str(e):
            st.warning(f"⚠️ Failed to create container '{cname}': {e}")

# -----------------------------------------------
# 3. Contact Form
# -----------------------------------------------
st.markdown("### 🙋 Contact (Optional)")
with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Email Address")
    company = st.text_input("Company (optional)")
    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        contact_data = pd.DataFrame([{"name": name, "email": email, "company": company, "timestamp": datetime.now()}])
        csv_bytes = contact_data.to_csv(index=False).encode('utf-8')
        blob_name = f"contact_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        contact_blob = blob_service_client.get_blob_client(container=CONTACT_CONTAINER, blob=blob_name)
        contact_blob.upload_blob(csv_bytes, overwrite=True)
        st.session_state["user_email"] = email  # store email in session
        st.success("✅ Contact submitted successfully!")
    except Exception as e:
        st.error(f"❌ Failed to save contact info: {e}")

# -----------------------------------------------
# 4. Upload CSV File
# -----------------------------------------------
uploaded_file = st.file_uploader("Upload your sales_data.csv", type=["csv"])
forecast_days = st.slider("Forecast horizon (days)", min_value=7, max_value=90, value=30)

if uploaded_file:
    try:
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=uploaded_file.name)
        blob_client.upload_blob(uploaded_file, overwrite=True)

        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)

        if not {'Date', 'Demand', 'Product ID'}.issubset(df.columns):
            st.error("❌ CSV must include 'Date', 'Demand', and 'Product ID' columns.")
        else:
            df['Date'] = pd.to_datetime(df['Date'])
            product_ids = df['Product ID'].unique()
            selected_product = st.selectbox("Select a Product to Forecast", product_ids)
            df_filtered = df[df['Product ID'] == selected_product]

            df_daily = df_filtered.groupby("Date")["Demand"].sum().reset_index()
            df_daily.columns = ["ds", "y"]

            if len(df_daily) < 2:
                st.warning("⚠️ Not enough data to train the model for this product.")
                st.stop()

            model = Prophet()
            model.fit(df_daily)

            future = model.make_future_dataframe(periods=forecast_days)
            forecast = model.predict(future)

            forecast_merged = forecast.set_index("ds")[["yhat"]].join(df_daily.set_index("ds")[["y"]]).dropna()
            forecast_merged["APE"] = abs((forecast_merged["y"] - forecast_merged["yhat"]) / forecast_merged["y"])
            mape = forecast_merged["APE"].mean() * 100
            rmse = np.sqrt(((forecast_merged["y"] - forecast_merged["yhat"]) ** 2).mean())

            st.subheader("📊 Forecast Accuracy (Training Period Only)")
            st.metric("Mean Absolute Percentage Error (MAPE)", f"{mape:.2f}%")
            st.metric("Root Mean Squared Error (RMSE)", f"{rmse:.2f}")

            st.caption("**MAPE** shows the average forecast error as a percentage of actual values — lower is better. **RMSE** tells how far off predictions are in the same units as demand (e.g. units/day). Both are based on historical training data.")

            forecast_display = forecast.rename(columns={
                "ds": "Date",
                "yhat": "Predicted Demand",
                "yhat_lower": "Lower Bound",
                "yhat_upper": "Upper Bound"
            })

            st.subheader(f"📈 Forecast Plot for Product: {selected_product}")
            fig = plot_plotly(model, forecast)
            fig.update_layout(xaxis_title="Date", yaxis_title="Forecasted Demand")
            st.plotly_chart(fig)

            st.subheader("🔢 Forecasted Values")
            st.dataframe(forecast_display[["Date", "Predicted Demand", "Lower Bound", "Upper Bound"]].tail(forecast_days))

            csv_output = forecast_display[["Date", "Predicted Demand", "Lower Bound", "Upper Bound"]].to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Forecast CSV", csv_output, file_name=f"forecast_{selected_product}.csv")

            # Log forecast event
            try:
                user_email = st.session_state.get("user_email", "anonymous")
                log_entry = pd.DataFrame([{
                    "timestamp": datetime.now(),
                    "user_email": user_email,
                    "product_id": selected_product,
                    "forecast_days": forecast_days,
                    "mape": round(mape, 2),
                    "rmse": round(rmse, 2)
                }])
                log_bytes = log_entry.to_csv(index=False).encode("utf-8")
                log_name = f"forecast_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                log_blob = blob_service_client.get_blob_client(container=LOG_CONTAINER, blob=log_name)
                log_blob.upload_blob(log_bytes, overwrite=True)
                st.success("📄 Forecast event logged.")
            except Exception as e:
                st.warning(f"⚠️ Logging failed: {e}")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")