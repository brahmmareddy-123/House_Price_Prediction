import streamlit as st
import pandas as pd
import joblib

# Load model and columns
model = joblib.load("Ame_house_price_model.pkl")
model_columns = joblib.load("Ame_house_model_columns.pkl")

st.title("🏠 House Price Prediction App")

st.write("Enter house details to predict price")

# User Inputs
overall_qual = st.slider("Overall Quality", 1, 10, 5)
gr_liv_area = st.number_input("Ground Living Area (sq ft)", 500, 5000, 1500)
garage_cars = st.number_input("Garage Capacity", 0, 5, 2)
total_bsmt = st.number_input("Basement Area (sq ft)", 0, 3000, 800)
year_built = st.number_input("Year Built", 1900, 2025, 2000)
lot_area = st.number_input("Lot Area", 1000, 50000, 8000)

neighborhood = st.selectbox(
    "Neighborhood",
    ["NAmes","CollgCr","OldTown","Edwards","Somerst"]
)

kitchen_qual = st.selectbox(
    "Kitchen Quality",
    ["Ex","Gd","TA","Fa"]
)

# Feature Engineering
current_year = 2026
house_age = current_year - year_built
total_area = total_bsmt + gr_liv_area

# Create input dataframe
input_dict = {
    "Overall Qual": overall_qual,
    "Gr Liv Area": gr_liv_area,
    "Garage Cars": garage_cars,
    "Total Bsmt SF": total_bsmt,
    "Year Built": year_built,
    "Lot Area": lot_area,
    "HouseAge": house_age,
    "TotalArea": total_area
}

input_data = pd.DataFrame([input_dict])

# Add dummy columns
for col in model_columns:
    if col not in input_data.columns:
        input_data[col] = 0

input_data = input_data[model_columns]

# Prediction
if st.button("Predict Price"):

    prediction = model.predict(input_data)

    # Convert USD to INR
    price_in_inr = prediction[0] * 83

    st.success(f"Predicted House Price: ₹{price_in_inr:,.2f}")