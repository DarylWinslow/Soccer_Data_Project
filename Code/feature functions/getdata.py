from __future__ import print_function

import os
import pandas as pd

def get_foot_data():
    """Get the E0 data, from local csv or pandas repo."""
    if os.path.exists("bigdata.csv"):
        print("-- bigdata.csv found locally")
        df = pd.read_csv("bigdata.csv", index_col=0)
    else:
        print("-- can't find bigdata.csv, downloading latest data")
        fn = "http://www.football-data.co.uk/mmz4281/1516/E0.csv"
        fn1 = "http://www.football-data.co.uk/mmz4281/1415/E0.csv"
        fn2 = "http://www.football-data.co.uk/mmz4281/1314/E0.csv"
        fn3 = "http://www.football-data.co.uk/mmz4281/1213/E0.csv"
        fn4 = "http://www.football-data.co.uk/mmz4281/1112/E0.csv"
        fn5 = "http://www.football-data.co.uk/mmz4281/1011/E0.csv"
        try:
            df = pd.read_csv(fn)
            df1 = pd.read_csv(fn1)
            df2 = pd.read_csv(fn2)
            df3 = pd.read_csv(fn3)
            df4 = pd.read_csv(fn4)
            df5 = pd.read_csv(fn5)
            df = pd.concat([df, df1, df2, df3, df4, df5])
        except:
            exit("-- Unable to download E0.csv")

        with open("bigdata.csv", 'w') as f:
            print("-- writing to local bigdata.csv file")
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
    print("Number of rows in bigdata is " + str(len(df)))
    
 
    """ 
    with open("describe.csv", 'w') as f:
            print("-- writing to local describe.csv file")
            des=df.describe()
            des.to_csv(f)
            
       
    #Example Opponents DataFrame
    team1 = 'Liverpool'
    team1_df = get_team_data(df, team1)
    
    team2 = 'Everton'
    team2_df = get_team_data(df, team2)
    
    
    city = df['HomeTeam'] == "Man City"
    stoke = df['AwayTeam'] == "Stoke"
    CityStoke = df[city & stoke]
    
    print(CityStoke)
    
    AC
AF
AR
AS
AST
AY
AwayTeam
B365A
B365D
B365H
BSA
BSD
BSH
BWA
BWD
BWH
Bb1X2
BbAH
BbAHh
BbAv<2.5
BbAv>2.5
BbAvA
BbAvAHA
BbAvAHH
BbAvD
BbAvH
BbMx<2.5
BbMx>2.5
BbMxA
BbMxAHA
BbMxAHH
BbMxD
BbMxH
BbOU
Date
Div
FTAG
FTHG
FTR
GBA
GBD
GBH
HC
HF
HR
HS
HST
HTAG
HTHG
HTR
HY
HomeTeam
IWA
IWD
IWH
LBA
LBD
LBH
PSA
PSD
PSH
Referee
SBA
SBD
SBH
SJA
SJD
SJH
VCA
VCD
VCH
WHA
WHD
WHH
"""
 

    
    
    
    