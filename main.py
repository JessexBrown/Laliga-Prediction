import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

###################################### DATA ORGANIZATION ######################################################

# https://www.kaggle.com/datasets/kishan305/la-liga-results-19952020/data
laliga_data = pd.read_csv("/content/Data/LaLiga_Matches.csv")

# Desired filter year 
year = '2010'
filtered_df = laliga_data[laliga_data['Season'].str.startswith(year)]

# Extract  column
home_teams = filtered_df['HomeTeam'].unique()
away_teams = filtered_df['AwayTeam'].unique()

participating_teams = set(np.concatenate((home_teams, away_teams)))
home_goals = filtered_df['FTHG'].values
away_goals = filtered_df['FTAG'].values

