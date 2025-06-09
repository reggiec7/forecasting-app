# 📦 BizForecast – Demand Forecasting App

![Version](https://img.shields.io/badge/version-v1.2-blue)

This is a Streamlit-based web app that uses **Facebook Prophet** to forecast product demand using uploaded sales data. It integrates with **Azure Blob Storage** for cloud-based file management.

---

## 🚀 Features

- Upload CSV sales data
- Forecast demand for specific `Product ID`s
- View interactive forecast plots and metrics (MAPE, RMSE)
- Download forecast results as CSV
- Automatically stores uploaded files to Azure Blob Storage
- Collects optional user contact info for lead capture

---

## 📂 Sample CSV Format

| Date       | Product ID | Demand |
|------------|------------|--------|
| 2022-01-01 | P0001      | 150    |
| 2022-01-01 | P0002      | 120    |
| ...        | ...        | ...    |


---

## 🛠 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/reggiec7/forecasting-app.git
cd forecasting-app

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your Azure storage secret in .streamlit/secrets.toml
AZURE_STORAGE_CONNECTION_STRING = "your_connection_string_here"

# Run the app
streamlit run forecasting_app.py
```

---

## 📈 Forecast Accuracy Metrics
- **MAPE**: Percent error in predictions — lower is better.
- **RMSE**: Absolute error in units of demand (e.g., units/day).

Displayed after training on historical data. Future forecast accuracy is not evaluated.

---

## 🔗 Useful Links

- [Live App on Streamlit Cloud](https://biz-forecast.streamlit.app/)
- [CHANGELOG.md](./CHANGELOG.md)

---

## 📋 License
MIT License