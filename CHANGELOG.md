# 📌 Changelog

All notable changes to this project will be documented here.
## [v1.2] – 2024-06-02
### ✨ Enhancements
- Added multi-product forecasting: users can select a `Product ID` from uploaded CSVs to generate individual forecasts.
- Added a contact capture form (name, email, company) and securely store it in Azure Blob Storage.

### 📊 Benefits
- Enables business-specific forecasting at the product level.
- Begins user acquisition flow with basic lead capture for potential monetization.

## [v1.1] – 2024-06-02
### ✨ Enhancements
- Added **MAPE** (Mean Absolute Percentage Error) and **RMSE** (Root Mean Squared Error) to measure forecast accuracy.
- Displayed training error metrics using `st.metric` for clarity.
- Added user-friendly caption explaining both metrics in plain language.

### 📊 Benefits
- Improves user trust by showing how accurate the model was during training.
- Supports non-technical users with plain-English metric descriptions.

## [v1.0] – 2024-06-01
### 🎉 Initial Public Release

- Clean landing page UI with Streamlit
- Upload `.csv` to Azure Blob Storage
- Forecasts future demand using Facebook Prophet
- Interactive forecast chart (Plotly)
- Download forecasted results as `.csv`
- Auto-deployment via Streamlit Cloud
