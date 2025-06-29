import streamlit as st
import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pickle


# Load the trained model
model = tf.keras.models.load_model('model.h5')

# Load the scaler and encoders
with open('label_encoder_gender.pkl', 'rb') as f:
    label_encoder_gender = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('onehot_encoder.pkl', 'rb') as f:
    onehot_encoder_geo = pickle.load(f)


# streamlit app
st.title("Customer Churn Prediction")

# User Input
geography = st.selectbox("Geography", onehot_encoder_geo.categories_[0])
gender = st.selectbox("Gender", label_encoder_gender.classes_)
age = st.slider("Age", 18, 92)
balance = st.numer_input('Credit SCore')
credit_score = st.number_input('Credit Salary')
estimated_salary = st.number_input('Estimated Salary')
num_of_products = st.slider('Number of products', 1, 4)
tenture = st.slider("Tenure", 0, 10)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox("Is Active Number", [0, 1])

# Prepare input as a DataFrame
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenture],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

# One-hot encode 'Geography'
geo_encoded = onehot_encoder_geo.tranform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=onehot_encoder_geo.get_features_names_out(["Geography"]))

# Combine one-hot encoded columns with input data
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], asix=1)

# Scale the input data
input_data_scaled = scaler.transform(input_data)

## Predict churn
prediction = model.predict(input_data_scaled)
prediction_proba = prediction[0][0]

st.write()

if prediction_proba > 0.5:
    st.write("The customer is likely to churn with a probability of {:.2f}%".format(prediction_proba * 100))
else:
    st.write("The customer is unlikely to churn with a probability of {:.2f}%".format((1 - prediction_proba) * 100))
