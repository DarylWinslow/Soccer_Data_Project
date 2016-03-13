from __future__ import print_function

import getdata

df = getdata.get_foot_data()

team1="Liverpool"
team2="Everton"
team3="Watford"

team1_df = getdata.get_team_data(df, team1)   
team2_df = getdata.get_team_data(df, team2)
team3_df = getdata.get_team_data(df, team3)


with open("live.csv", 'w') as f:
    print("-- writing to local liv.csv file")
    team1_df.to_csv(f)