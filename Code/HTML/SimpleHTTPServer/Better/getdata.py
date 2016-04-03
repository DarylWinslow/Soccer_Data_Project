from __future__ import print_function

import os
import datetime
import pandas as pd

#Open file or download data for last 6 years of PL Football
def get_foot_data():
    """Get the E0 data, from local csv or download."""
    if os.path.exists("bigdata.csv"):
        #print("-- bigdata.csv found locally")
        df = pd.read_csv("bigdata.csv", index_col=0)
    else:
        print("-- can't find bigdata.csv, downloading latest data")
        fn = "http://www.football-data.co.uk/mmz4281/1516/E0.csv"
        fn1 = "http://www.football-data.co.uk/mmz4281/1415/E0.csv"
        fn2 = "http://www.football-data.co.uk/mmz4281/1314/E0.csv"
        fn3 = "http://www.football-data.co.uk/mmz4281/1213/E0.csv"
        fn4 = "http://www.football-data.co.uk/mmz4281/1112/E0.csv"
        fn5 = "http://www.football-data.co.uk/mmz4281/1011/E0.csv"
        fn6 = "http://www.football-data.co.uk/mmz4281/0910/E0.csv"
        fn7 = "http://www.football-data.co.uk/mmz4281/0809/E0.csv"
        fn8 = "http://www.football-data.co.uk/mmz4281/0708/E0.csv"
        fn9 = "http://www.football-data.co.uk/mmz4281/0607/E0.csv"
        
        try:
            df = pd.read_csv(fn)
            df1 = pd.read_csv(fn1)
            df2 = pd.read_csv(fn2)
            df3 = pd.read_csv(fn3)
            df4 = pd.read_csv(fn4)
            df5 = pd.read_csv(fn5)
            df6 = pd.read_csv(fn6)
            df7 = pd.read_csv(fn7)
            df8 = pd.read_csv(fn8)
            df9 = pd.read_csv(fn9)
                
            df = pd.concat([df, df1, df2, df3, df4, df5, df6, df7, df8, df9])
        except:
            exit("-- Unable to download csv files")

        with open("bigdata.csv", 'w') as f:
            print("-- writing to local bigdata.csv file")
            df.to_csv(f)
            
    df = select_columns(df)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    return df
    
#Refine DataFrame. Default value for columns strips away all the betting odds
def select_columns(df, columns=['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR',
                               'HTHG','HTAG','HTR','Referee','HS','AS','HST',
                               'AST','HF','AF','HC','AC','HY','AY','HR','AR']):
    df = df[columns]
    #print("-- New DataFrame Constructed --")
    return(df)
    
def graph_data(df, column):
    df.set_index(['Date'],inplace=True)
    plot = df[column].plot()
    return(plot)
    
#Returns Team Data for all seasons    
def get_team_data(team, df=get_foot_data()):
    """Return DataFrame with Team's Data"""
    Home = df.loc[df['HomeTeam'] == team]
    Away = df.loc[df['AwayTeam'] == team]
    team_data = pd.concat([Home, Away])
    #print("-- Team DataFrame Constructed --")
    return team_data
    

def head_to_head(team1, team2, df=get_foot_data()):
    t1df=get_team_data(team1, df)
    t2df=get_team_data(team2, df)
    Home = t1df.loc[t1df['AwayTeam'] == team2]
    Away = t2df.loc[t2df['AwayTeam'] == team1]
    return(pd.concat([Home, Away]))
    
def home_stats(team, df):
    home = df.loc[df['HomeTeam'] == team]
    return(home)
    
def away_stats(team, df):
    away = df.loc[df['AwayTeam'] == team]
    return(away)
    
def date_search(df, date1, befaft='b'):
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    if befaft == 'a':
        df = df.loc[df['Date'] > date1]
    if befaft == 'b':
        df = df.loc[df['Date'] < date1]
    
    df = df.sort_values('Date')
    return(df)
    
def last_month():
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)
    thisDay = today.day
    thisDayLastMonth = lastMonth.replace(day=thisDay)
    return(thisDayLastMonth)
    

def last_six(team, df=get_foot_data(), ha=' ', h2h='n'):
    tdf = get_team_data(team, df)   
    tdf = select_columns(tdf, ['Date', 'HomeTeam', 'AwayTeam', 'FTR', 'FTHG', 'FTAG', 'HR', 'AR'])
    tdf['Date'] = pd.to_datetime(tdf['Date'], dayfirst=True)
    tdf = tdf.sort_values('Date')
    last6 = tdf.tail(6)
    home = home_stats(team, last6)
    away = away_stats(team, last6)
    i = 0
    wdl=0
    while i < 6:
        if home[i:i+1].FTR.any() == 'H':
            #print(home[i:i+1])
            #print("HOME AND WON \n")
            wdl = wdl + 1
        elif home[i:i+1].FTR.any() == 'A':
            #print(home[i:i+1])
            #print("HOME AND LOST \n")
            wdl = wdl - 1
        #elif home[i:i+1].FTR.any() == 'D':
            #print(home[i:i+1])
            #print("HOME DRAW \n")  
            
        if away[i:i+1].FTR.any() == 'H':
            #print(away[i:i+1])
            #print("AWAY AND LOST \n")
            wdl = wdl - 1
        elif away[i:i+1].FTR.any() == 'A':
            #print(away[i:i+1])
            #print("AWAY AND WON \n")
            wdl = wdl + 1
        #elif away[i:i+1].FTR.any() == 'D':
            #print(away[i:i+1])
            #print("AWAY DRAW \n")
        i = i+1
    
    #print("WDL is " + str(wdl))
    gs=home.FTHG.sum() + away.FTAG.sum()
    #print("Goals scored is " + str(gs))
    ga=home.FTAG.sum() + away.FTHG.sum()
    #print("Goals conceded is " +str(ga))
    rc=home.HR.sum()+away.AR.sum()
    #print("Red cards = "+ str(rc))
    
    if(h2h=='y'): 
        d = {'H2hWDL': [wdl], 'H2hGS': [gs], 'H2hGA': [ga], 'H2hRC': [rc]}
        l6 = pd.DataFrame(d, columns=['H2hWDL', 'H2hGS', 'H2hGA', 'H2hRC'])
    elif(ha=='h'): 
        d = {'HWDL': [wdl], 'HGS': [gs], 'HGA': [ga], 'HRC': [rc]}
        l6 = pd.DataFrame(d, columns=['HWDL', 'HGS', 'HGA', 'HRC'])
    elif(ha=='a'): 
        d = {'AWDL': [wdl], 'AGS': [gs], 'AGA': [ga], 'ARC': [rc]}
        l6 = pd.DataFrame(d, columns=['AWDL', 'AGS', 'AGA', 'ARC'])
    else: 
        d = {'WDL': [wdl], 'Scored': [gs], 'Conceded': [ga], 'Red Cards': [rc]}
        l6 = pd.DataFrame(d, columns=['WDL', 'Scored', 'Conceded', 'Red Cards'])
    
    return(l6)
    

def create_model_data(olddf):
    olddf['Date'] = pd.to_datetime(olddf['Date'], dayfirst=True)
        
    newdf= pd.DataFrame(columns=['Date', 'HomeTeam', 'AwayTeam', 'FTR', 'HWDL', 'HGS', 'HGA', 'HRC',
                                'AWDL', 'AGS', 'AGA', 'ARC', 'H2hWDL', 'H2hGS', 'H2hGA', 'H2hRC'])
    
    for index, row in olddf.iterrows():
        #print(row['HomeTeam'], row['Referee'])
        date=row['Date']
        home=row['HomeTeam']
        away=row['AwayTeam']
        ftr=row['FTR']
        #datedf=date_search(olddf, date)
        hl6=last_six(home, ha='h')
        al6=last_six(away, ha='a')
        h2hdf=head_to_head(home, away)
        h2hl6=last_six(home, h2hdf, h2h='y')
        d = {'Date': [date], 'HomeTeam': [home], 'AwayTeam': [away], 'FTR':[ftr]}
        df = pd.DataFrame(d, columns=['Date', 'HomeTeam', 'AwayTeam', 'FTR'])
        newrow = pd.concat([df, hl6, al6, h2hl6], axis=1)
        #print(newrow)
        newdf = newdf.append(newrow)        
    
    return(newdf)
    
    
    
    

    
    


if __name__ == "__main__":
    print("\n-- get data:")
    #df = select_columns(get_foot_data())
    #print("")
    #print("Number of rows in bigdata is " + str(len(df)))
    
    
    ####TESTING AREA####
    """
    bigdf = get_foot_data()
    newdf = create_model_data(bigdf)    
    
    
    
    # Testing for create model data for predictions function
    bigdf = get_foot_data()
    bigdf['Date'] = pd.to_datetime(bigdf['Date'], dayfirst=True)
    testdf=pd.read_csv("testfuture.csv", index_col=0)
    testdf['Date'] = pd.to_datetime(testdf['Date'], dayfirst=True)
    testdf = testdf.sort_values('Date')
    sorteddf = bigdf.sort_values('Date')
    newdf= pd.DataFrame(columns=['Date', 'HomeTeam', 'AwayTeam', 'FTR', 'HWDL', 'HGS', 'HGA', 'HRC',
                                'AWDL', 'AGS', 'AGA', 'ARC', 'H2hWDL', 'H2hGS', 'H2hGA', 'H2hRC'])
                              
    for index, row in testdf.iterrows():
        #print(row['HomeTeam'], row['Referee'])
        date=row['Date']
        home=row['HomeTeam']
        away=row['AwayTeam']
        ftr=row['FTR']
        datedf=date_search(sorteddf, date)
        hl6=last_six(home, datedf, ha='h')
        #print(home + " " + away)
        #print(hl6)
        al6=last_six(away, datedf, ha='a')
        #print(al6)
        h2hdf=head_to_head(home, away, datedf)
        h2hl6=last_six(home, h2hdf, h2h='y')
        d = {'Date': [date], 'HomeTeam': [home], 'AwayTeam': [away], 'FTR':[ftr]}
        df = pd.DataFrame(d, columns=['Date', 'HomeTeam', 'AwayTeam', 'FTR'])
        newrow = pd.concat([df, hl6, al6, h2hl6], axis=1)
        #print(newrow)
        newdf = newdf.append(newrow)   
        
        with open("futuretestmodel.csv", 'w') as f:
            newdf.to_csv(f)
    #######################
    
    
    """
    
    """
    team1 = "Liverpool"
    team2 = "Everton"
    
    Livl6=last_six(team1, ha='h')
    Evl6=last_six(team2, ha='a')
    
    LvE = head_to_head(team1, team2)
    LvEl6 = last_six(team1, LvE, h2h='y')
    test = pd.concat([Livl6, Evl6, LvEl6], axis=1)
    
    team3 = "Arsenal"
    team4 = "Chelsea"
    
    Arsl6=last_six(team3, ha='h')
    Chell6=last_six(team4, ha='a')
    
    AvC = head_to_head(team3, team4)
    ACl6 = last_six(team3, AvC, h2h='y')
    test2 = pd.concat([Arsl6, Chell6, ACl6], axis=1)
    """
    """
    if os.path.exists("E0.csv"):
        testdf = pd.read_csv("E0.csv", index_col=0)
        testdf['Date'] = pd.to_datetime(testdf['Date'], dayfirst=True)
    """    
       
    
    

    
    

 
    
    
    