def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('Country').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                   ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def year_country_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = df['Country'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if (year == "Overall" and country == "Overall"):
        temp_df = medal_df

    if (year == "Overall" and country != "Overall"):
        temp_df = medal_df[medal_df['Country'] == country]
        flag = 1

    if (year != "Overall" and country == "Overall"):
        temp_df = medal_df[medal_df['Year'] == year]

    if (year != "Overall" and country != "Overall"):
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['Country'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('Country').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                       ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    nations_over_time = nations_over_time.sort_values('Year')
    nations_over_time.rename(columns={'count': col, 'Year': 'Edition'}, inplace=True)

    return nations_over_time

def most_successful(df, sport):
    temp_df = df[df['Medal'] != 'No medal']
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, on='Name')[['Name', 'count', 'Sport', 'Country']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'}, inplace=True)

    return x

def year_wise_medal_tally(df, country):
    temp_df = df[df['Medal'] != 'No medal']
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['Country'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_sport_heatmap(df, country):
    temp_df = df[df['Medal'] != 'No medal']
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['Country'] == country]
    y = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')

    return y

def most_successful_countrywise(df, country):
    temp_df = df[df['Medal'] != 'No medal']
    temp_df = temp_df[temp_df['Country'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, on='Name')[['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'}, inplace=True)

    return x

def men_vs_women_participation(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'Country'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final_df = men.merge(women, on='Year', how='left')
    final_df.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final = final_df.fillna(0).astype('int')

    return final