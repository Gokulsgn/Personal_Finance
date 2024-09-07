import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Personal Finance Manager", page_icon="💰")

# Add some custom styling
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
    }
    .title {
        color: #1e1e1e;
        text-align: center;
    }
    .card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .form-element {
        margin-bottom: 1rem;
    }
    .data-table {
        display: flex;
        justify-content: center;
        overflow-x: auto;
    }
    .data-frame {
        width: 100%;
        max-width: 1200px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>Personal Finance Manager</h1>", unsafe_allow_html=True)

# Container for form and results
with st.container():
    # Form for input
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("## Add New Expense")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("Date", key="date_input")
            category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Others"], key="category_select")
        
        with col2:
            description = st.text_input("Description", key="description_input")
            amount = st.number_input("Amount", min_value=0.0, step=0.01, key="amount_input")

        submit_button = st.button("Submit")
        st.markdown('</div>', unsafe_allow_html=True)

    # Load existing data from Flask API
    response = requests.get('http://127.0.0.1:5000/api/data')
    data = response.json()
    df = pd.DataFrame(data)

    if submit_button:
        # Convert date to string
        date_str = date.strftime('%Y-%m-%d')
        
        new_data = pd.DataFrame({
            "Date": [date_str],
            "Description": [description],
            "Category": [category],
            "Amount": [amount]
        })
        
        response = requests.post('http://127.0.0.1:5000/api/data', json=new_data.to_dict(orient='records'))
        if response.status_code == 201:
            st.success("Data saved successfully!")
            df = pd.concat([df, new_data], ignore_index=True)
        else:
            st.error("Failed to save data.")

    if not df.empty:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h1 class='title'>Expense Data</h1>", unsafe_allow_html=True)
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
