import streamlit as st
import pandas as pd
from prophet import Prophet
from azure.storage.blob import BlobServiceClient
import io
import plotly.graph_objs as go
from prophet.plot import plot_plotly

# -----------------------------------------------
# 1. Page Setup
# -----------------------------------------------
st.set_page_config(page_title="Demand Forecast App", layout="centered")
st.title("📦 Demand Forecasting Web App")
st.markdown("Upload your CSV file to forecast demand over time using Prophet.")

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

        # Plot forecast
        st.subheader("📈 Forecast Plot")
        fig = plot_plotly(model, forecast)
        fig.update_layout(xaxis_title="Date", yaxis_title="Forecasted Demand")
        st.plotly_chart(fig)

        # Show forecast table
        st.subheader("🔢 Forecasted Values")
        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(forecast_days))

        # Option to download results
        csv_output = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Forecast CSV", csv_output, file_name="demand_forecast.csv")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")


