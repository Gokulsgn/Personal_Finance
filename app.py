import streamlit as st
import pandas as pd
import os
from streamlit_option_menu import option_menu

# Set a custom theme using Streamlit's built-in feature
st.set_page_config(page_title="Personal Finance Manager", page_icon="💰", layout="centered")

# Add custom CSS to enhance styling and responsiveness
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f2f6;
        margin: 0;
        padding: 0;
    }
    .stButton button {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: background 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #45a049, #4CAF50);
    }
    .stTextInput input, .stDateInput input, .stSelectbox select {
        border-radius: 8px;
        padding: 12px;
        border: 2px solid #ddd;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: border-color 0.3s, box-shadow 0.3s;
        width: 100%;
    }
    .stTextInput input:focus, .stDateInput input:focus, .stSelectbox select:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 8px rgba(76, 175, 80, 0.2);
        outline: none;
    }
    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin: 10px;
    }
    .css-1d391kg {
        background-color: #FF6347;
        color: white;
        border-radius: 12px;
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stDataFrame {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
    }
    /* Styling for the option menu */
    .nav-link {
        font-size: 16px;
        font-weight: bold;
        color: black;
        border-radius: 8px;
        padding: 12px;
        transition: background-color 0.3s, color 0.3s;
    }
    .nav-link-selected {
        background-color: #FF6347;
        color: white;
        font-weight: bold;
    }
    .nav-link:hover {
        background-color: #FF6347;
        color: white;
    }
    .stOptionMenu .stMenu {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 10px;
    }
    /* Responsive design */
    @media (max-width: 768px) {
        .stButton button {
            padding: 10px 20px;
            font-size: 14px;
        }
        .stTextInput input, .stDateInput input, .stSelectbox select {
            padding: 10px;
            font-size: 14px;
        }
        .nav-link {
            font-size: 14px;
        }
    }
    @media (max-width: 480px) {
        .stButton button {
            padding: 8px 16px;
            font-size: 12px;
        }
        .stTextInput input, .stDateInput input, .stSelectbox select {
            padding: 8px;
            font-size: 12px;
        }
        .nav-link {
            font-size: 12px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 Personal Finance Manager")

# Navigation menu using streamlit-option-menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Add Expense", "View Data"],
    icons=["house", "plus-circle", "table"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ffffff", "border-radius": "12px", "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"},
        "icon": {"color": "orange", "font-size": "20px"},
        "nav-link": {
            "font-size": "18px",
            "font-weight": "bold",
            "text-align": "center",
            "margin": "0px",
            "color": "black",
            "border-radius": "12px",
            "padding": "12px",
            "transition": "background-color 0.3s, color 0.3s"
        },
        "nav-link-selected": {"background-color": "#FF6347", "color": "white", "font-weight": "bold"},
        "nav-link:hover": {"background-color": "#FF6347", "color": "white"},
    }
)

if selected == "Home":
    st.subheader("Welcome to your Personal Finance Manager! 🎉")
    st.write("Track your expenses, set budgets, and gain insights into your financial habits.")
    st.write("Use the menu above to navigate through the app.")

if selected == "Add Expense":
    user_id = st.text_input("Enter your username:")

    if user_id:
        filename = f"{user_id}_data.csv"

        if os.path.exists(filename):
            df = pd.read_csv(filename)
        else:
            df = pd.DataFrame(columns=["Date", "Description", "Category", "Amount"])

        st.subheader("Add New Expense")

        with st.form(key='input_form'):
            date = st.date_input("Date")
            description = st.text_input("Description")
            category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Others"])
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
            submit_button = st.form_submit_button("Submit")

        if submit_button:
            new_data = pd.DataFrame({"Date": [date], "Description": [description], "Category": [category], "Amount": [amount]})
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(filename, index=False)
            st.success("Data saved successfully!")

    else:
        st.warning("Please enter your username to proceed.")

if selected == "View Data":
    user_id = st.text_input("Enter your username:")

    if user_id:
        filename = f"{user_id}_data.csv"

        if os.path.exists(filename):
            df = pd.read_csv(filename)
            st.subheader("Your Data")
            st.dataframe(df, use_container_width=True)

            # Calculate and display the sum of expenses
            total_expense = df["Amount"].sum()
            st.write(f"### Total Expense: ₹{total_expense:.2f}")

        else:
            st.write("No data available. Please add your expenses.")

    else:
        st.warning("Please enter your username to view your data.")
