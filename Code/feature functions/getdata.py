from __future__ import print_function

import os
import datetime
import pandas as pd

#Open file or download data for last 6 years of PL Football
def get_foot_data():
    """Get the E0 data, from local csv or download."""
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
    
#Refine DataFrame. Default value for columns strips away all the betting odds
def select_columns(df, columns=['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR',
                               'HTHG','HTAG','HTR','Referee','HS','AS','HST',
                               'AST','HF','AF','HC','AC','HY','AY','HR','AR']):
    df = df[columns]
    print("-- New DataFrame Constructed --")
    return(df)
    
#Returns Team Data for all seasons    
def get_team_data(df, team):
    """Return DataFrame with Team's Data"""
    Home = df.loc[df['HomeTeam'] == team]
    Away = df.loc[df['AwayTeam'] == team]
    team_data = pd.concat([Home, Away])
    print("-- Team DataFrame Constructed --")
    return team_data
    

def head_to_head(team1, team2, t1df, t2df):
    Home = t1df.loc[t1df['AwayTeam'] == team2]
    Away = t2df.loc[t2df['AwayTeam'] == team1]
    return(pd.concat([Home, Away]))
    
def home_stats(team, df):
    home = df.loc[df['HomeTeam'] == team]
    return(home)
    
def away_stats(team, df):
    away = df.loc[df['AwayTeam'] == team]
    return(away)
    
def date_search(df, date1, befaft):
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    if befaft == 'a':
        df = df.loc[df['Date'] >= date1]
    if befaft == 'b':
        df = df.loc[df['Date'] <= date1]
    
    df = df.sort_values('Date')
    return(df)
    
def last_month():
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)
    thisDay = today.day
    thisDayLastMonth = lastMonth.replace(day=thisDay)
    return(thisDayLastMonth)
    

def last_six(team, df=get_foot_data()):
    tdf = get_team_data(df, team)   
    tdf = select_columns(tdf, ['Date', 'HomeTeam', 'AwayTeam', 'FTR', 'FTHG', 'FTAG'])
    tdf['Date'] = pd.to_datetime(tdf['Date'], dayfirst=True)
    tdf = tdf.sort_values('Date')
    last6 = tdf.tail(6)
    #print(last6)
    home = home_stats(team, last6)
    away = away_stats(team, last6)
    
    i = 0
    while i < 6:
        if home[i:i+1].FTR.any() == 'H':
            print(home[i:i+1])
            print("HOME AND WON \n")
        elif home[i:i+1].FTR.any() == 'A':
            print(home[i:i+1])
            print("HOME AND LOST \n")
        elif home[i:i+1].FTR.any() == 'D':
            print(home[i:i+1])
            print("HOME DRAW \n")  
        """
        else:
            print(home[i:i+1])
            print("WARNING NO DATA \n") 
        """
            
        if away[i:i+1].FTR.any() == 'H':
            print(away[i:i+1])
            print("AWAY AND WON \n")
        elif away[i:i+1].FTR.any() == 'A':
            print(away[i:i+1])
            print("AWAY AND LOST \n")
        elif away[i:i+1].FTR.any() == 'D':
            print(away[i:i+1])
            print("AWAY DRAW \n")
        """
        else:
            print(away[i:i+1])
            print("WARNING NO DATA \n")
        """
        i = i+1
    

    
    


if __name__ == "__main__":
    print("\n-- get data:")
    df = select_columns(get_foot_data())
    print("")
    print("Number of rows in bigdata is " + str(len(df)))
    
    
    ####TESTING AREA####
    
    team1 = "Liverpool"
    team2 = "Everton"
    t1df = get_team_data(df, team1)
    t2df = get_team_data(df, team2)
    t1df = select_columns(t1df, ['Date', 'HomeTeam', 'AwayTeam', 'FTR', 'FTHG', 'FTAG'])
    t2df = select_columns(t2df, ['Date', 'HomeTeam', 'AwayTeam', 'FTR', 'FTHG', 'FTAG'])
    
    LvE = head_to_head(team1, team2, t1df, t2df)
    
    
    """
    t1df = t1df.sort_values('Date')
    last6 = t1df.tail(6)
    home = home_stats(team1, last6)
    away = away_stats(team1, last6)
    i = 0
    while i < len(away):
        if away[i:i+1].FTR.any() == 'H':
            print("HOME")
        elif away[i:i+1].FTR.any() == 'A':
            print("AWAY")
        elif away[i:i+1].FTR.any() == 'D':
            print("DRAW")
        i = i+1
    """
    

    
    

 
    
    
    