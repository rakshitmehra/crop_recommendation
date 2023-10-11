import joblib
import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu
from twilio.rest import Client

# Load the model
try:
    model = joblib.load('./SavedModels/fruits1.joblib')
except Exception as e:
    st.error(f"Error loading the model: {e}")

# Create the Streamlit app
with st.sidebar:
    # selected = st.selectbox('Crop Prediction System', ['Crops Prediction'])
    selected = option_menu('Crop Recommendation System',
                                ['Crops Recommendation'],
                                icons = ['activity'],
                                default_index=0)

if selected == 'Crops Recommendation':
    st.title('Crop Prediction By Using Machine Learning')
    st.write("**Note: N, P & K are in grams per Hectare, Temperature is in Degree Celsius, Humidity in Percentage (%) & Rainfall in Millimeter(mm).**")
    
    # Create input fields for user to enter features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        N = st.text_input('Nitrogen')
    with col2:
        P = st.text_input('Phosphorus')
    with col3:
        K = st.text_input('Potassium')
    with col1:
        temperature = st.text_input('Temperature')
    with col2:
        humidity = st.text_input('Humidity')
    with col3:
        ph = st.text_input('Ph')
    with col1:
        rainfall = st.text_input('Rainfall')
            
    crop = ''

    if st.button('Submit'):
        try:
            input_features = [
                float(N), float(P), float(K), float(temperature),
                float(humidity), float(ph), float(rainfall)
            ]
            
            # Use the loaded model to make predictions
            crop_prediction = model.predict([input_features])
            
            # Map prediction to crop name (as you've done before)
            crop_names = [
                'Apple', 'Banana', 'Coconut', 'Dates', 'Grapes', 'Guava', 'Litchi', 'Mango', 'Musk Melon', 'Orange', 'Papaya', 'Pomegranate', 'Strawberry', 'Sugar Cane', 'Water Melon',
            ]
            if 0 <= crop_prediction[0] < len(crop_names):
                crop = crop_names[crop_prediction[0]]
            else:
                crop = 'Soil is not fit for growing crops'

            if crop != 'Soil is not fit for growing crops':
                if float(humidity) <= 40:
                    st.write(
                        '<div style="background-color: Grey; padding: 15px; margin-bottom: 20px; border-radius: 5px; font-size: 20px; color: white;">'
                        '<strong>⚠️⚠️LOW WATER LEVEL IN YOUR SOIL⚠️⚠️</strong>'
                        '</div>',
                        unsafe_allow_html=True
                    )
                st.write(
                    f'<div style="background-color: Grey; padding: 15px; margin-bottom: 20px; border-radius: 5px; font-size: 22px; color: white;">'
                    f'<strong>Soil is fit to grow {crop}</strong>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        except ValueError:
            st.error("Invalid input. Please provide valid numeric values for all features.")