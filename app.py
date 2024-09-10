import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('olympics_dataset.csv')
noc_country = pd.read_csv('noc_country.csv')

df = preprocessor.preprocess(df,noc_country)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRh2BFlPvu_og03soxqXUu5aYQv6dITAvqe6SfOTPNLU5E1-LOab00_f7IUkQoRRRBw0i0&usqp=CAU')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, countries = helper.year_country_list(df)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', countries)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall Performance")

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['Country'].unique().shape[0]

    st.title('Top Statistics')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader('Editions')
        st.title(editions)

    with col2:
        st.subheader('Hosts')
        st.title(cities)

    with col3:
        st.subheader('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader('Events')
        st.title(events)

    with col2:
        st.subheader('Athletes')
        st.title(athletes)

    with col3:
        st.subheader('Nations')
        st.title(nations)

    nations_over_time = helper.data_over_time(df, 'Country')
    fig = px.line(nations_over_time, x='Edition', y='Country', width=800, height=500)
    st.title('Participating Nations Over the Years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event', width=800, height=500)
    st.title('Events Over the Years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name', width=800, height=500)
    st.title('Athletes Over the Years')
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    x = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    ax = sns.heatmap(x, annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')

    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    selected_sport = st.selectbox("Select a Sport", sports_list)

    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Country wise Analysis':
    st.sidebar.title('Country wise Analysis')

    country_list = df['Country'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox("Select a Country", country_list)

    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal', width=800, height=500)
    st.title(selected_country + ' Medal Tally Over the Years')
    st.plotly_chart(fig)

    st.title(selected_country + ' excels in following sports')

    pt = helper.country_sport_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(15, 15))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title('Top 10 Athletes of ' + selected_country)
    top_ten = helper.most_successful_countrywise(df, selected_country)
    st.table(top_ten)

if user_menu == 'Athlete wise Analysis':
    st.subheader('Men vs Women Participation over the Years')
    final = helper.men_vs_women_participation(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'], width=800, height=400)
    st.plotly_chart(fig)