import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import time
from streamlit_gsheets import GSheetsConnection

# 1. Connect to the Google Sheet using streamlit_gsheets
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=600)
def load_data():
    # Read the sheet data directly (Sheet1 by default, or specify a sheet name if needed)
    df = conn.read()
    return df

def create_bar_chart(data):
    avg_price = data.groupby("cut")["price"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(avg_price["cut"], avg_price["price"], color='skyblue')
    ax.set_xlabel("Cut")
    ax.set_ylabel("Average Price")
    ax.set_title("Average Price by Diamond Cut (Bar Chart)")
    return fig

def create_box_plot(data):
    fig, ax = plt.subplots(figsize=(6,4))
    sns.boxplot(x="cut", y="price", data=data, ax=ax, palette="Set2")
    ax.set_title("Price Distribution by Diamond Cut (Box Plot)")
    return fig

def main():
    st.title("My Diamonds App with Google Sheets Data")
    st.write("**Business Question:** Which diamond cut has the highest average price?")

    # Load data from the Google Sheet
    diamonds_df = load_data()

    # 2. A/B Testing: show random chart
    if 'chart_shown' not in st.session_state:
        st.session_state.chart_shown = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None

    if not st.session_state.chart_shown:
        if st.button("Show Chart"):
            st.session_state.chart_shown = True
            st.session_state.chart_choice = random.choice(["bar", "box"])
            st.session_state.start_time = time.time()  # Record start time

    if st.session_state.chart_shown:
        if st.session_state.chart_choice == "bar":
            st.pyplot(create_bar_chart(diamonds_df))
        else:
            st.pyplot(create_box_plot(diamonds_df))

        if st.button("I answered your question"):
            end_time = time.time()
            elapsed_time = end_time - st.session_state.start_time
            st.success(f"Thank you for participating! It took you {elapsed_time:.2f} seconds to answer the question.")

if __name__ == "__main__":
    main()
