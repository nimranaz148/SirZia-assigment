# 

import streamlit as st
import pandas as pd
import os
import time
from matplotlib import pyplot as plt
import numpy as np
from io import BytesIO

# Page Config
st.set_page_config(page_title="🚀 Data Sweeper", layout='wide')

# Custom CSS for animations
st.markdown(
    """
    <style>
    @keyframes blink {
        0% {opacity: 1;}
        50% {opacity: 0.5;}
        100% {opacity: 1;}
    }
    .blinking-text {
        animation: blink 1s infinite;
        color: red;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.title("🚀 Data Sweeper")
st.markdown(
    """
    <h1 style='text-align: center; color: #FF5733; font-size: 36px;'>🚀 Hello! My name is <span style="color:#4CAF50;">Nimra Naz</span></h1>
    <h2 style='text-align: center; color: #3498db; font-size: 28px;'>This is my <span style="color:#e74c3c;">Awesome Streamlit App</span> for Cleaning and Transforming Data! 🛠️✨</h2>
    <p style='text-align: center; font-size: 22px; color: #8e44ad; font-weight: bold;'>💡 Growth Mindset Challenge: "Every challenge is an opportunity to grow and improve!" 🚀</p>
    """,
    unsafe_allow_html=True
)


# Sidebar for settings
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("<style>body{background-color: #333; color: white;}</style>", unsafe_allow_html=True)

# File Upload Section
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[1]
        with st.spinner("⏳ Processing your file... Please wait!"):
            time.sleep(2)

        # Read file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue
        
        # File Info
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")
        
        # Show dataframe
        st.write("📊 **Preview of Data**")
        st.dataframe(df.head())
        
        # Data Cleaning Options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🗑 Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")
            
            with col2:
                if st.button(f"📉 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled!")
        
        # Data Visualization
        st.subheader("📈 Data Visualization")
        chart_type = st.radio("Choose chart type:", ["Line Chart", "Bar Chart", "None"], key=file.name)
        
        if chart_type != "None":
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 1:
                x_col = st.selectbox("Select X-axis column:", numeric_cols, key=f"x_{file.name}")
                y_col = st.selectbox("Select Y-axis column:", numeric_cols, key=f"y_{file.name}")
                fig, ax = plt.subplots()
                if chart_type == "Line Chart":
                    ax.plot(df[x_col], df[y_col], label=f"{y_col} vs {x_col}")
                else:
                    ax.bar(df[x_col], df[y_col])
                ax.legend()
                st.pyplot(fig)
            else:
                st.warning("Not enough numeric columns for visualization!")
        
        # File Conversion
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"{file.name}_{time.time()}")

        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            # Download button
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.write("✨ **Enjoy using Data Sweeper! 🚀**")
