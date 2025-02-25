# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO


# Set up our app

st.set_page_config(page_title = "📀Advanced Data Sweeper", layout = "wide")

st.markdown(
    """
    <style>
    .main {
        background-color: #121212;
    }

    .block-container {
        padding: 3rem 2rem;
        border-radius: 12px;
        background-color:rgb(197, 196, 196);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    h1, h2, h3, h4, h5, h6 {
        color: #66c2ff;
    }

    .stButton>button {
        border: none;
        border-radius: 8px;
        background-color: #0078D7;
        color: white;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    }

    .stButton>button:hover {
        background-color: #005a9e;
        cursor: pointer;
    }

    .stDataFrame, .stTable {
        border-radius: 10px;
        overflow: hidden;
    }

    .css-1aumxik, .css-18e3th9 {
        text-align: left;
        color: white;
    }

    .stRadio>label {
        font-weight: bold;
        color: white;
    }

    .stCheckbox>label {
        color: white;
    }

    .stDownloadButton>button {
        background-color: #28a745;
        color: white;
    }

    .stDownloadButton>button:hover {
        background-color: #218838;
    }
    </style>
    """,
    unsafe_allow_html = True
)
st.title("📀 Advanced Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type = ["csv", "xlsx"], accept_multiple_files = True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1]


        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type: {file_ext}")
            continue

        # Display info about the file
        st.write(f"**📄File Name:** {file.name}")
        st.write(f"**📏File Size:** {file.size/1024}")

        #Show 5 rows of our df
        st.write("🔍Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("🛠️Data Cleaning Otions")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace = True)
                    st.write("Duplicates Removes!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled!")

        
        # Choose Specific Columns to Keep or Convert
        st.subheader("🎯Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default = df.columns)
        df = df[columns]


        # Create Some Visualizations
        st.subheader("📊Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


        # Convert the File => CSV to Excel
        st.subheader("🔄Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:",["CSV", "Excel"], key = file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index = False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index = False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)


            # Download Button
            st.download_button(
                label = f"⬇️ Download {file.name} as {conversion_type}",
                data = buffer,
                file_name = file_name,
                mime = mime_type
            )

st.success("🎉 All files processed successfully!")