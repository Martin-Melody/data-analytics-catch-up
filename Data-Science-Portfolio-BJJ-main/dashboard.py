import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px

uri = ""

# Create a new client and connect to the server
client = MongoClient(uri)  # replace with your MongoDB host and port
db = client['Bjj_data']
collection = db['bjj_data']


data = pd.DataFrame(list(collection.find({})))
data = data[data['Year'] != 0]
# Set the title of the app
st.title('Jiu Jitsu Matches Dashboard')

# Show the entire DataFrame
#st.write(data)

# Sidebar filters
year = st.sidebar.slider('Year', int(data['Year'].min()), int(data['Year'].max()))
team = st.sidebar.selectbox('Team', options=['All'] + list(data['Team'].unique()))
stage = st.sidebar.selectbox('Stage', options=['All'] + list(data['Stage'].unique()))
competition = st.sidebar.selectbox('Competition', options=['All'] + list(data['Competition'].unique()))
weight = st.sidebar.selectbox('Weight', options=['All'] + list(data['Weight'].unique()))
method = st.sidebar.selectbox('Method', options=['All'] + list(data['Method'].unique()))

filtered_data = data.copy()
# Filter data based on sidebar inputs
if team != 'All':
    filtered_data = filtered_data[filtered_data['Team'] == team]
if stage != 'All':
    filtered_data = filtered_data[filtered_data['Stage'] == stage]
if competition != 'All':
    filtered_data = filtered_data[filtered_data['Competition'] == competition]
if weight != 'All':
    filtered_data = filtered_data[filtered_data['Weight'] == weight]
if method != 'All':
    filtered_data = filtered_data[filtered_data['Method'] == method]
filtered_data = filtered_data[filtered_data['Year'] >= year]
st.write(filtered_data)


# Visualizations
st.subheader('Number of matches per year')
st.bar_chart(filtered_data['Year'].value_counts())

st.subheader('Team')
if team == 'All':
    st.bar_chart(filtered_data['Team'].value_counts().nlargest(10))
else:
    st.markdown(f"## {team}", unsafe_allow_html=True)
    st.subheader('Top 10 People with the Most Winnings')
    winners = filtered_data[filtered_data['W/L'] == 'W']
    winners_count = winners['Full Name'].value_counts().nlargest(10)
    st.bar_chart(winners_count)


st.subheader('Distribution of victories and losses')
fig = px.pie(filtered_data, names='W/L', title='Distribution of victories and losses')
st.plotly_chart(fig)

st.subheader('Most common methods of victory')
st.bar_chart(filtered_data['Method'].value_counts().nlargest(10))