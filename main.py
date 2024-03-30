import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

###################################### DATA ORGANIZATION ######################################################

laliga_data = pd.read_csv("/content/LaLiga_Matches.csv")

# Desired filter settings
considered_games = 380 # 380 games in a season
year = '2010'

filtered_df = laliga_data[laliga_data['Season'].str.startswith(year)]

# Extract teams
home_teams = filtered_df['HomeTeam'].values
away_teams = filtered_df['AwayTeam'].values

participating_teams = np.union1d(home_teams, away_teams)

# Extract goals
home_goals = filtered_df['FTHG'].values[:considered_games]
away_goals = filtered_df['FTAG'].values[:considered_games]



# Construct Adjaceny Matrix for targeted data
n_teams = len(participating_teams)
n_games = considered_games

A = np.zeros((n_teams, n_teams))
for i in range(n_teams):
    for j in range(n_teams):
        for k in range(n_games):
            # Check for the played games between i and j sides
            if (participating_teams[i] == home_teams[k] and participating_teams[j] == away_teams[k]):
                # apply for both home or away
                if (home_goals[k] > away_goals[k]):
                    A[i,j] += home_goals[k] - away_goals[k]
                else:
                    A[j,i] += away_goals[k] - home_goals[k]


# Construct Markov Matrix

M = np.zeros(A.shape)
for i in range(len(A)):
  col_sums = sum(A[:,i])

  if (col_sums != 0):
    # Markov Part
    M[:,i] = A[:,i] / col_sums
  else:
    # Account for zero matchups (Should not be enetered
    # since teams all play against each other in a season)
    M[:,i] = np.ones(len(A)).T / len(A)
    

# Power iteration to find steady state vector

x0 = np.ones(len(A)) / len(A)
x1 = M @ x0

while ((x0 != x1).all()):
  x0 = M @ x0
  x1 = M @ x1


# Get rankings (Best -> Worst)
prob_idxs = np.argsort(-x0)

ranked_probs = x0[prob_idxs]
ranked_teams = participating_teams[prob_idxs]

print(ranked_probs)
print(ranked_teams)
