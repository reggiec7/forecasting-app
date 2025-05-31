# -----------------------------------------------
# README content (as string, optional for documentation)
# -----------------------------------------------
README = """
# 📦 Demand Forecasting App

This is a Streamlit web app that forecasts daily product demand using Facebook Prophet. Users can upload a sales CSV, run time series forecasting, and download projected results — all powered by a backend connection to Azure Blob Storage.

## 🚀 Features

- Upload historical sales data in `.csv` format
- Automatically forecast future demand for the next 7–90 days
- View interactive charts and confidence intervals
- Download forecasted results as a `.csv`
- Saves uploaded data to Azure Blob Storage

## 📂 Sample CSV Format

| Date       | Demand |
|------------|--------|
| 2022-01-01 | 150    |
| 2022-01-02 | 175    |

📝 Additional metadata like `Product ID` or `Store ID` can be included, but only `Date` and `Demand` are required for forecasting.

## 🛠 How to Run Locally

1. **Clone the repository**:
   ```bash
   git clone git@github.com:your-username/forecasting-app.git
   cd forecasting-app
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Azure secrets**:

   Create a file called `.streamlit/secrets.toml` and add your Azure storage credentials:

   ```toml
   AZURE_STORAGE_CONNECTION_STRING = "your_connection_string_here"
   ```

5. **Run the app**:

   ```bash
   streamlit run forecasting_app.py
   ```

   The app will open in your default browser at [http://localhost:8501](http://localhost:8501)

## ☁️ Optional: Deployment Options

- [Streamlit Community Cloud](https://streamlit.io/cloud)
- Azure App Service
- Docker + GitHub Actions (optional)

## 📄 License

MIT — free for personal and commercial use.
"""
