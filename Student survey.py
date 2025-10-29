import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np # Added for creating dummy data

st.set_page_config(
  page_title="Scientific Visualization"
)
st.header("Scientific Visualization", divider="gray")

# Define the URL for the data
URL = 'https://raw.githubusercontent.com/aisyah2521/EC2024/refs/heads/main/arts_faculty_data.csv'

col1, col2, col3, col4 = st.columns(4)
    
col1.metric(label="PLO 2", value=f"3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric(label="PLO 3", value=f"3.5", help="PLO 3: Digital Skill", border=True)
col3.metric(label="PLO 4", value=f"4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value=f"4.3", help="PLO 5: Communication Skill", border=True)

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


# --- Dummy DataFrame Creation ---
# In a real application, you would load your DataFrame like this:
# df_onlines = pd.read_csv('your_data.csv')
# Since 'df_onlines' is not defined, we'll create a dummy one for the example to be runnable.

# Function to create a dummy DataFrame matching the required columns
def create_dummy_df():
    np.random.seed(42)
    data = {
        'Faculty': np.random.choice(['Arts', 'Science', 'Commerce'], 100),
        'Bachelor Academic Year in EU': np.random.randint(2018, 2024, 100),
        '1st Year Semester 1': np.random.uniform(2.5, 4.0, 100).round(2),
        'Average_Semester_GPA': np.random.uniform(2.8, 3.8, 100).round(2),
        'H.S.C (GPA)': np.random.uniform(4.0, 5.0, 100).round(2)
    }
    df = pd.DataFrame(data)
    # Introduce some NaNs to mimic real-world data and test dropna
    df.loc[::10, 'Bachelor Academic Year in EU'] = np.nan
    df.loc[::5, 'H.S.C (GPA)'] = np.nan
    return df

df_onlines = create_dummy_df()
# --- End of Dummy DataFrame Creation ---

st.set_page_config(layout="wide")
st.title("Data Visualization for Arts Faculty")

# --- 1. Distribution of Bachelor Academic Year in EU (Histogram) ---
st.header("1. Bachelor Academic Year Distribution (Arts Faculty)")
st.write("This histogram shows the frequency distribution of the academic year students from the Arts faculty were in the EU Bachelor program.")

# Filter the DataFrame for 'Arts' faculty
arts_bachelor_years = df_onlines[df_onlines['Faculty'] == 'Arts']['Bachelor Academic Year in EU'].dropna()

if not arts_bachelor_years.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(arts_bachelor_years, bins=20, edgecolor='black')
    ax.set_title('Distribution of Bachelor Academic Year in EU for Arts Faculty')
    ax.set_xlabel('Bachelor Academic Year in EU')
    ax.set_ylabel('Frequency')
    ax.grid(axis='y', alpha=0.75)
    st.pyplot(fig)
else:
    st.warning("No data available for 'Bachelor Academic Year in EU' in the Arts Faculty.")
plt.close(fig) # Important to explicitly close the plot

# --- 2. 1st Year Semester 1 GPA vs. Average Semester GPA (Scatter Plot) ---
st.header("2. GPA Correlation: 1st Year Semester 1 vs. Average (All Faculties)")
st.write("A scatter plot comparing students' GPA in their first semester with their overall average semester GPA.")

# The original code did not filter this plot for 'Arts' despite the title, 
# so the Streamlit title is adjusted, and the plot uses the full DataFrame.
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df_onlines['1st Year Semester 1'], df_onlines['Average_Semester_GPA'])
ax.set_title('1st Year Semester 1 GPA vs. Average Semester GPA')
ax.set_xlabel('1st Year Semester 1 GPA')
ax.set_ylabel('Average Semester GPA')
ax.grid(True)
st.pyplot(fig)
plt.close(fig)

# --- 3. Distribution of H.S.C (GPA) (Violin Plot) ---
st.header("3. H.S.C (GPA) Distribution (Arts Faculty)")
st.write("A violin plot illustrating the distribution and density of H.S.C (GPA) scores for students in the Arts faculty.")

# Filter the DataFrame for 'Arts' faculty and drop NaN values in 'H.S.C (GPA)'
arts_hsc_gpa = df_onlines[df_onlines['Faculty'] == 'Arts']['H.S.C (GPA)'].dropna()

if not arts_hsc_gpa.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(x=arts_hsc_gpa, ax=ax)
    ax.set_title('Distribution of H.S.C (GPA) for Arts Faculty')
    ax.set_xlabel('H.S.C (GPA)')
    st.pyplot(fig)
else:
    st.warning("No data available for 'H.S.C (GPA)' in the Arts Faculty.")
plt.close(fig)
