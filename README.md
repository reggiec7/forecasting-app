# 📦 BizForecast

![Version](https://img.shields.io/badge/version-v1.3-blue)

A Streamlit web app that forecasts product demand using Facebook Prophet.  
It supports Azure Blob Storage for file handling and tracks usage events for lead capture and business analytics.

---

## 🚀 Features

- Upload a CSV with `Date`, `Demand`, and `Product ID`
- Forecast demand for a selected product over 7–90 days
- View forecast chart and accuracy metrics (MAPE, RMSE)
- Download forecasted results
- Contact form with name, email, company
- Forecast usage is logged to Azure Blob
- Auto-creates Blob containers as needed

---

## 🛠 How to Run Locally

```bash
git clone https://github.com/reggiec7/forecasting-app.git
cd forecasting-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run forecasting_app.py
