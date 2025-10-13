import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
  page_title="Genetic Algorithm"
)
st.header("Genetic Algorithm", divider="gray")

# Define the URL for the data
URL = 'https://raw.githubusercontent.com/aisyah2521/EC2024/refs/heads/main/arts_faculty_data.csv'

# Set the title of the Streamlit application
st.title('📊 Arts Faculty Gender Distribution')

# --- Data Loading and Processing ---

@st.cache_data
def load_data(url):
    """Loads the data from the URL and returns the DataFrame."""
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data(URL)

# Check if data loaded successfully and contains the 'Gender' column
if not df.empty and 'Gender' in df.columns:
    # Calculate the counts for each gender
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    st.header('Visualizations')

    # 1. Plotly Pie Chart (Interactive)
    st.subheader('Gender Distribution (Pie Chart)')
    fig_pie = px.pie(
        gender_counts,
        values='Count',
        names='Gender',
        title='Proportional Gender Distribution in Arts Faculty',
        hole=.3  # Creates a donut chart effect
    )
    # Customize the layout for better appearance
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # 2. Plotly Bar Chart (Interactive)
    st.subheader('Gender Distribution (Bar Chart)')
    fig_bar = px.bar(
        gender_counts,
        x='Gender',
        y='Count',
        title='Count of Students by Gender in Arts Faculty',
        color='Gender',
        template='plotly_white'
    )
    # Customize the layout
    fig_bar.update_layout(xaxis_title='Gender', yaxis_title='Number of Students')
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.subheader('Raw Data Preview')
    st.dataframe(df.head())

else:
    st.error("Data could not be loaded or the 'Gender' column is missing. Please verify the CSV file structure.")
