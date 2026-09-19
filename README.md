# California House Price Prediction

A machine learning project that predicts California housing prices using a
Random Forest Regressor, served through a FastAPI REST API and a Streamlit
web frontend. Supports both single-record predictions and bulk CSV
predictions.

## Overview

This project uses the **California Housing dataset** (20,640 records) to
train a regression model that estimates median house prices based on
neighborhood-level features like income, location, and occupancy.

- **Model:** Random Forest Regressor (scikit-learn)
- **Average error:** ~$39,000 (Mean Absolute Error)
- **Serving:** FastAPI, with model persisted via `joblib`
- **Frontend:** A Streamlit app for entering features and viewing predictions in the browser

## Project Structure

```
price_prediction/
├── explore.py              # Exploratory Data Analysis (EDA) on the dataset
├── train.py                 # Trains the model and saves it to disk
├── main.py                   # FastAPI app — serves predictions
├── app_frontend.py           # Streamlit frontend — calls the FastAPI /predict endpoint
├── house_model.joblib        # Trained Random Forest model (generated)
├── house_features.joblib     # List of feature names (generated)
├── requirements.txt          # Python dependencies
└── docs/
    ├── House_Price_Prediction.pptx   # Project presentation
    └── screenshots/                   # API/UI testing screenshots
```

## How It Works

1. **`explore.py`** — Loads the California Housing dataset and prints shape,
   head, and summary statistics to understand the data before modeling.
2. **`train.py`** — Loads the dataset, splits it into train/test sets (80/20),
   trains a `RandomForestRegressor` (100 trees), evaluates it (MAE, R²), and
   saves the trained model + feature list as `.joblib` files.
3. **`main.py`** — Loads the saved model at startup and exposes a FastAPI app
   with endpoints to get single or bulk predictions.
4. **`app_frontend.py`** — A Streamlit app that collects the 8 features
   through a form, calls the running FastAPI `/predict` endpoint, and
   displays the predicted price and confidence range.

## Features Used by the Model

| Feature | Description |
|---|---|
| `MedInc` | Median income in the neighborhood block |
| `HouseAge` | Average age of houses in the block |
| `AveRooms` | Average number of rooms per house |
| `AveBedrms` | Average number of bedrooms per house |
| `Population` | Total population of the block |
| `AveOccup` | Average number of occupants per house |
| `Latitude` | Block latitude (32–42) |
| `Longitude` | Block longitude (-125 to -114) |

## Setup & Installation

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Re)train the model
python train.py

# 4. Run the API server
uvicorn main:app --reload

# 5. In a separate terminal, run the frontend
streamlit run app_frontend.py
```

The API will be live at `http://127.0.0.1:8000`, with interactive docs at
`http://127.0.0.1:8000/docs`. The Streamlit frontend runs at
`http://localhost:8501` and requires the API server to be running.

## API Endpoints

### `GET /`
Health check with basic API info.

### `GET /health`
Returns model status, model type, feature list, and average error.

### `POST /predict`
Predicts price for a single house given its features (JSON body).

**Example request body:**
```json
{
  "MedInc": 8.3,
  "HouseAge": 25,
  "AveRooms": 6.1,
  "AveBedrms": 1.0,
  "Population": 1200,
  "AveOccup": 3.0,
  "Latitude": 34.05,
  "longitude": -118.25
}
```

**Example response:**
```json
{
  "predicted_price": "$452,300",
  "predicted_price_short": "$4.52 hundred thousands",
  "confidence_range": "$413,300 to $491,300"
}
```

### `POST /predict-file`
Upload a `.csv` file containing the required columns (`MedInc`, `HouseAge`,
`AveRooms`, `AveBedrms`, `Population`, `AveOccup`, `Latitude`, `Longitude`)
and get back a CSV with an added `predicted_price` column.

## Frontend

`app_frontend.py` is a Streamlit app that provides a simple UI on top of the
API:

- A form with number inputs for all 8 features (income, house age, rooms,
  bedrooms, population, occupancy, latitude, longitude)
- A "Predict price" button that sends the inputs to the FastAPI `/predict`
  endpoint
- Displays the predicted price and confidence range returned by the API

It requires the FastAPI server (`main.py`) to already be running, since it
calls `http://127.0.0.1:8000/predict` under the hood. Bulk CSV predictions
are only available via the API's `/predict-file` endpoint, not the frontend.

## Tech Stack

- **Python 3.12**
- **scikit-learn** — model training (RandomForestRegressor)
- **pandas** — data handling
- **FastAPI** — REST API framework
- **joblib** — model serialization
- **uvicorn** — ASGI server
- **Streamlit** — web frontend

## Notes

- The model is trained once via `train.py` and loaded at API startup —
  retrain and restart the server if the underlying data changes.
- Average error (~$39,000) is used to build a simple confidence range
  around each prediction.
