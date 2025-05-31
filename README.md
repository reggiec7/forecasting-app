# 📦 Demand Forecasting App

This is a Streamlit web app that forecasts daily product demand using Facebook Prophet. Users can upload a sales CSV, run time series forecasting, and download projected results — all powered by a backend connection to Azure Blob Storage.

---

## 🚀 Features

- Upload historical sales data in `.csv` format
- Automatically forecast future demand for the next 7–90 days
- View interactive charts and confidence intervals
- Download results as a `.csv`
- Saves your uploaded data to Azure Blob Storage

---

## 📂 Sample CSV Format

| Date       | Demand |
|------------|--------|
| 2022-01-01 | 150    |
| 2022-01-02 | 175    |
| ...        | ...    |

Or with additional metadata like `Product ID`, `Store ID`, etc. (only `Date` and `Demand` are required for forecasting).

---

## 🛠 How to Run Locally

1. Clone the repo:
   ```bash
   git clone git@github.com:your-username/forecasting-app.git
   cd forecasting-app
   
## Create a virtual environment and activate
python3 -m venv venv
source venv/bin/activate

## Install dependencies:
pip install -r requirements.txt

## Add your Azure storage connection string to .streamlit/secrets.toml:
AZURE_STORAGE_CONNECTION_STRING = "your_connection_string_here"

## Launch the app:
streamlit run forecasting_app.py
