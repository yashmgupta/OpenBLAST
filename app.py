# Import required libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Function to clean percentage columns
def clean_percentage_column(dataframe, column_name):
    if column_name in dataframe.columns:
        dataframe[column_name] = dataframe[column_name].str.rstrip('%').astype('float') / 100.0
    return dataframe

# Set page configuration
st.set_page_config(page_title="BLAST Result Dashboard", layout="wide")

# Sidebar - File uploader
with st.sidebar:
    st.title("BLAST Dashboard")
    uploaded_file = st.file_uploader("Upload BLAST Result CSV", type=['csv'])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        
        # Clean and prepare data
        data.columns = data.columns.str.strip()  # Strip whitespace from column names
        data = clean_percentage_column(data, 'Query Cover')  # Clean 'Query Cover' column
        
    else:
        data = pd.DataFrame()  # Empty DataFrame if no file is uploaded

# Main page setup
st.title("BLAST Result Visualization")

# Check if data is loaded
if not data.empty:
    st.write("### Summary")
    # Total number of different species
    total_species = data['Scientific Name'].nunique()
    st.write(f"Total number of different species: {total_species}")
    
    # The sequence with the highest Percentage Identity
    top_sequence = data.loc[data['Per. ident'].idxmax()]
    st.write("Top most similar sequence details:")
    st.write(top_sequence)
    
    # Visualization of Query Coverage
    st.write("### Query Coverage Distribution")
    fig_query_cover = px.histogram(data, x="Query Cover", nbins=50, title="Query Coverage Distribution")
    st.plotly_chart(fig_query_cover, use_container_width=True)
    
    # Visualization of Percentage Identity
    st.write("### Percentage Identity Distribution")
    fig_per_ident = px.histogram(data, x="Per. ident", nbins=50, title="Percentage Identity Distribution")
    st.plotly_chart(fig_per_ident, use_container_width=True)
    
    # Summary of top species based on occurrence
    st.write("### Top Species by Occurrence")
    species_count = data['Scientific Name'].value_counts().reset_index()
    species_count.columns = ['Scientific Name', 'Count']
    fig_species_count = px.bar(species_count.head(10), x='Scientific Name', y='Count', title='Top 10 Species by Occurrence')
    st.plotly_chart(fig_species_count, use_container_width=True)
    
    # Detailed Data Table
    st.write("### Detailed Results")
    st.dataframe(data)
    
else:
    st.write("Please upload a BLAST result CSV file to start.")
