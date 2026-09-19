import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="California House Price Predictor", page_icon="🏠")

st.title("California House Price Predictor")
st.caption("Enter neighborhood details to get a predicted median house price.")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        med_inc = st.number_input("Median income (10,000s USD)", min_value=0.1, value=5.0, step=0.1)
        house_age = st.number_input("House age (years)", min_value=1.0, value=25.0, step=1.0)
        ave_rooms = st.number_input("Average rooms per house", min_value=0.1, value=6.0, step=0.1)
        ave_bedrms = st.number_input("Average bedrooms per house", min_value=0.1, value=1.0, step=0.1)

    with col2:
        population = st.number_input("Population of the block", min_value=1.0, value=1200.0, step=10.0)
        ave_occup = st.number_input("Average occupants per house", min_value=0.1, value=3.0, step=0.1)
        latitude = st.number_input("Latitude", min_value=32.0, max_value=42.0, value=34.05, step=0.01)
        longitude = st.number_input("Longitude", min_value=-125.0, max_value=-114.0, value=-118.25, step=0.01)

    submitted = st.form_submit_button("Predict price")

if submitted:
    payload = {
        "MedInc": med_inc,
        "HouseAge": house_age,
        "AveRooms": ave_rooms,
        "AveBedrms": ave_bedrms,
        "Population": population,
        "AveOccup": ave_occup,
        "Latitude": latitude,
        "longitude": longitude,
    }

    try:
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        st.success(f"Predicted price: {result['predicted_price']}")
        st.write(f"Confidence range: {result['fidence_range']}")

    except requests.exceptions.ConnectionError:
        st.error("Could not reach the API. Make sure main.py (FastAPI) is running on port 8000.")
    except requests.exceptions.HTTPError as e:
        st.error(f"API returned an error: {e}")
    except Exception as e:
        st.error(f"Something went wrong: {e}")

st.divider()
st.caption("Bulk predictions from a CSV are available via the API's /predict-file endpoint.")