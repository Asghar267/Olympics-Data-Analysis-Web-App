import time
import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import streamlit as st
import plotly.express as px
import helper  # Assuming you have a helper module with your functions
from dask import dataframe as dd
import plotly.express as px

# Set page configurations
st.set_page_config(
    page_title="Gender Participation Trends",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed",)

df = pd.read_csv('athlete_events.csv',index_col=None)
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("🏅 Olympics Analysis")
# st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

user_menu = st.sidebar.radio(
    'Select an Option',
    ("EDA Report",'Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

# Add some space for better separation
st.sidebar.markdown('---')

if user_menu == "EDA Report":
    st.title("Automated Exploratory Data Analysis Report")
    st.dataframe(df) 
            
    print("Profiling...")
    # profile_report = df.profile_report()
    profile_report = ProfileReport(df, explorative=True)
 
    st_profile_report(profile_report)

    # # Assuming df is your DataFrame
    # profile_report = ProfileReport(df, explorative=True)

    # # Convert the pandas profiling report to an HTML report
    # profile_html = profile_report.to_widgets()

    # # Display the HTML report in Streamlit
    # st.components.v1.html(profile_html, height=1000, scrolling=True)
    # # profile_html = profile_report.to_widgets()
    
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")

    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance") 
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    # st.title("No. of Events over time(Every Sport)")
    # fig,ax = plt.subplots(figsize=(20,20))
    # x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    # ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
    #             annot=True)
    # st.pyplot(fig)

    st.title("No. of Events over time(Every Sport)")

    # Create a heatmap with custom figure size and annotations
    fig, ax = plt.subplots(figsize=(30, 25))

    # sns.heatmap(pt, annot=True, annot_kws={"size": 20}, linewidths=1, cmap="YlGnBu", ax=ax)

    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    heatmap_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')

    sns.set(font_scale=1.5)  # Adjust the font scale for better readability

    # Customize heatmap appearance
    sns.heatmap(heatmap_data, annot=True, linewidths=1, cmap="YlGnBu", ax=ax, fmt='g', cbar=True)

    # Customize axis labels and plot title (optional)
    ax.set_xticklabels(heatmap_data.columns, rotation=45, ha='right', fontsize=18)
    ax.set_yticklabels(heatmap_data.index, fontsize=18)
    ax.set_xlabel("Year", fontsize=25)  # Customize X-axis label
    ax.set_ylabel("Sports", fontsize=25)  # Customize Y-axis label
    st.pyplot(fig)
 
    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)

    
    if not pt.empty and not pt.isnull().values.any():
        # fig, ax = plt.subplots(figsize=(20, 20))
        # ax = sns.heatmap(pt, annot=True)
        # st.pyplot(fig)
        # Set the font scale for better readability
        sns.set(font_scale=3.1)
        # Create a heatmap with custom figure size and annotations
        fig, ax = plt.subplots(figsize=(35, 25))
        sns.heatmap(pt, annot=True, annot_kws={"size": 20}, linewidths=1, cmap="YlGnBu", ax=ax)

        # Customize axis labels and plot title (optional)
        ax.set_xticklabels(pt.columns, rotation=45, ha='right', fontsize=20)
        ax.set_yticklabels(pt.index, fontsize=22)

        ax.set_xlabel("Year", fontsize=36)  # Customize X-axis label
        ax.set_ylabel("Sports", fontsize=36)  # Customize Y-axis label
        # plt.title("Your Heatmap Title", fontsize=18)  # Customize heatmap title

        # Display the heatmap with customized settings
        st.pyplot(fig)

    else:
        st.warning("No data available for creating the heatmap.")



    # fig, ax = plt.subplots(figsize=(20, 20))
    # ax = sns.heatmap(pt,annot=True)
    # st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
