# 📌 Changelog

All notable changes to this project will be documented here.
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
