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
    **1. Upload a CSV file** with at least two columns:  
    - `Date`: format like `YYYY-MM-DD`  
    - `Demand`: daily or aggregated demand quantity

    **2. Choose how far ahead to forecast**

    **3. View the interactive chart and download forecast results**

    🔐 Your data is temporarily uploaded to secure Azure Blob Storage.
    """)

# -----------------------------------------------
# 2. Azure Blob Storage Setup
# -----------------------------------------------
AZURE_CONNECTION_STRING = st.secrets["AZURE_STORAGE_CONNECTION_STRING"]
CONTAINER_NAME = "forecast-input"

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

# -----------------------------------------------
# 3. Upload CSV File
# -----------------------------------------------
uploaded_file = st.file_uploader("Upload your sales_data.csv", type=["csv"])
forecast_days = st.slider("Forecast horizon (days)", min_value=7, max_value=90, value=30)

if uploaded_file:
    try:
        # Upload file to Azure Blob Storage
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=uploaded_file.name)
        blob_client.upload_blob(uploaded_file, overwrite=True)

        # Read file into DataFrame
        uploaded_file.seek(0)  # reset pointer
        df = pd.read_csv(uploaded_file)

        # Clean and prepare data
        df['Date'] = pd.to_datetime(df['Date'])
        df_daily = df.groupby("Date")["Demand"].sum().reset_index()
        df_daily.columns = ["ds", "y"]

        # Fit Prophet model
        model = Prophet()
        model.fit(df_daily)

        future = model.make_future_dataframe(periods=forecast_days)
        forecast = model.predict(future)

        # Calculate MAPE and RMSE over training period
        forecast_merged = forecast.set_index("ds")[["yhat"]].join(df_daily.set_index("ds")[["y"]]).dropna()
        forecast_merged["APE"] = abs((forecast_merged["y"] - forecast_merged["yhat"]) / forecast_merged["y"])
        mape = forecast_merged["APE"].mean() * 100
        rmse = np.sqrt(((forecast_merged["y"] - forecast_merged["yhat"]) ** 2).mean())

        # Show forecast accuracy
        st.subheader("📊 Forecast Accuracy (Training Period Only)")
        st.metric("Mean Absolute Percentage Error (MAPE)", f"{mape:.2f}%")
        st.metric("Root Mean Squared Error (RMSE)", f"{rmse:.2f}")

        st.caption("**MAPE** shows the average forecast error as a percentage of actual values — lower is better. **RMSE** tells how far off predictions are in the same units as demand (e.g. units/day). Both are based on historical training data.")

        # Rename forecast columns for user-friendly display
        forecast_display = forecast.rename(columns={
            "ds": "Date",
            "yhat": "Predicted Demand",
            "yhat_lower": "Lower Bound",
            "yhat_upper": "Upper Bound"
        })

        # Plot forecast
        st.subheader("📈 Forecast Plot")
        fig = plot_plotly(model, forecast)
        fig.update_layout(xaxis_title="Date", yaxis_title="Forecasted Demand")
        st.plotly_chart(fig)

        # Show forecast table
        st.subheader("🔢 Forecasted Values")
        st.dataframe(forecast_display[["Date", "Predicted Demand", "Lower Bound", "Upper Bound"]].tail(forecast_days))

        # Option to download results
        csv_output = forecast_display[["Date", "Predicted Demand", "Lower Bound", "Upper Bound"]].to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Forecast CSV", csv_output, file_name="demand_forecast.csv")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
