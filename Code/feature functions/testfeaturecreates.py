from __future__ import print_function

import os
import pandas as pd

def get_foot_data():
    """Get the E0 data, from local csv or pandas repo."""
    if os.path.exists("bigdata.csv"):
        print("-- bigdata.csv found locally")
        df = pd.read_csv("bigdata.csv", index_col=0)
    else:
        print("-- trying to download from github")
        fn = "http://www.football-data.co.uk/mmz4281/1415/E0.csv"
        try:
            df = pd.read_csv(fn)
        except:
            exit("-- Unable to download E0.csv")

        with open("E0.csv", 'w') as f:
            print("-- writing to local E0.csv file")
            df.to_csv(f)

    return df
    
def get_team_data(df, team):
    """Return DataFrame with Team's Data"""
    Home = df.loc[df['HomeTeam'] == team]
    Away = df.loc[df['AwayTeam'] == team]
    team_data = pd.concat([Home, Away])
    print("-- Team DataFrame Constructed --")
  
    return team_data
    



if __name__ == "__main__":
    print("\n-- get data:")
    df = get_foot_data()
    print("")
    
    team1 = 'Liverpool'
    team1_df = get_team_data(df, team1)
    
    team2 = 'Everton'
    team2_df = get_team_data(df, team2)
    
    
    city = df['HomeTeam'] == "Man City"
    stoke = df['AwayTeam'] == "Stoke"
    CityStoke = df[city & stoke]
    

    
    
    
    