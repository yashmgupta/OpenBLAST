# Import required libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from Bio import SeqIO
from Bio.Blast import NCBIXML

# Set page configuration
st.set_page_config(page_title="BLAST Result Dashboard", layout="wide")

# Sidebar - File uploader
with st.sidebar:
    st.title("BLAST Dashboard")
    uploaded_file = st.file_uploader("Upload BLAST Result CSV", type=['csv'])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.DataFrame()  # Empty DataFrame if no file is uploaded

# Main page setup
st.title("BLAST Result Visualization")

# Check if data is loaded
if not data.empty:
    st.write("### Summary")
    st.write(data.describe())  # Display a summary of the data
    
    # Visualization of Identity Scores
    st.write("### Identity Score Distribution")
    fig = px.histogram(data, x="identity", nbins=50, title="Identity Score Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    # Visualization of E-values
    st.write("### E-value Distribution")
    fig2 = px.histogram(data, x="evalue", nbins=50, title="E-value Distribution", log_y=True)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Detailed Data Table
    st.write("### Detailed Results")
    st.dataframe(data)
    
else:
    st.write("Please upload a BLAST result CSV file to start.")
