import pandas as pd
import numpy as np
from helpers import Database
import datetime
from helpers import standardizeTeamName
from helpers import monthToInt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

#merges the entire match onto one row with stats denoted home and away
def mergeMatches(read_path = './csv_data/raw/advanced_stats.csv', write_path = "./csv_data/mid_manipulation/merged_matches.csv", writeToCsv = True):
    stats = pd.read_csv(read_path, encoding = "ISO-8859-1")
    A = Database(["Date","Home","Away","H_OffRtg","A_OffRtg","H_OREB%","A_OREB%","H_TOV%","A_TOV%","H_TS%","A_TS%","PACE"])
    indexesVisited = []
    for i in range(len(stats.index)):
        if (i in indexesVisited):
            continue
        indexesVisited.append(i)
        A.addCellToRow(stats.at[i,"Game Date"])
        for j in range(i+1, len(stats.index)):
            if ("vs." in stats.at[i,"Match Up"] and stats.at[j,"Team"] == stats.at[i,"Match Up"].split(" vs. ")[1] and stats.at[j,"Game Date"] == stats.at[i,"Game Date"]):
                indexesVisited.append(j)
                A.addCellToRow(stats.at[i,"Team"])
                A.addCellToRow(stats.at[j,"Team"])
                A.addCellToRow(stats.at[i,"OffRtg"])
                A.addCellToRow(stats.at[j,"OffRtg"])
                A.addCellToRow(stats.at[i,"OREB%"])
                A.addCellToRow(stats.at[j,"OREB%"])
                A.addCellToRow(stats.at[i,"TOV%"])
                A.addCellToRow(stats.at[j,"TOV%"])
                A.addCellToRow(stats.at[i,"TS%"])
                A.addCellToRow(stats.at[j,"TS%"])
                A.addCellToRow(stats.at[i,"PACE"])
                A.appendRow()
                break
            elif ("@" in stats.at[i,"Match Up"] and stats.at[j,"Team"] == stats.at[i,"Match Up"].split(" @ ")[1] and stats.at[j,"Game Date"] == stats.at[i,"Game Date"]):
                indexesVisited.append(j)
                A.addCellToRow(stats.at[j,"Team"])
                A.addCellToRow(stats.at[i,"Team"])
                A.addCellToRow(stats.at[j,"OffRtg"])
                A.addCellToRow(stats.at[i,"OffRtg"])
                A.addCellToRow(stats.at[j,"OREB%"])
                A.addCellToRow(stats.at[i,"OREB%"])
                A.addCellToRow(stats.at[j,"TOV%"])
                A.addCellToRow(stats.at[i,"TOV%"])
                A.addCellToRow(stats.at[j,"TS%"])
                A.addCellToRow(stats.at[i,"TS%"])
                A.addCellToRow(stats.at[i,"PACE"])
                A.appendRow()
                break
    if (writeToCsv):
        A.dictToCsv(write_path)
    return (A)

#gets the pre match averages for the stats so far in the season
def preMatchAverages(read_path = './csv_data/mid_manipulation/merged_matches.csv', write_path = './csv_data/mid_manipulation/pre_match_averages.csv', writeToCsv = True):
    stats = pd.read_csv(read_path, encoding = "ISO-8859-1")
    A = Database(["Date","Home","Away","H_GP","A_GP","H_OffRtg","A_OffRtg","H_DefRtg","A_DefRtg","H_OREB%","A_OREB%","H_DREB%","A_DREB%","H_TOV%","A_TOV%","H_STL%","A_STL%","H_TS%","A_TS%","H_dTS%","A_dTS%","H_PACE","A_PACE","H_REST","A_REST"])
    for index, row in stats.iterrows():
        if (index == 0 or int(row["Date"].split("/")[0]) - 3 > int(stats.at[index-1,"Date"].split("/")[0])):
            seasonDict = {}
        if (row["Home"] not in seasonDict):
            seasonDict[row["Home"]] = {"OffRtg":[],"DefRtg":[],"OREB%":[],"DREB%":[],"TOV%":[],"STL%":[],"TS%":[],"dTS%":[],"PACE":[],"LastG":datetime.date(1999,5,7),"GP":0}
        if (row["Away"] not in seasonDict):
            seasonDict[row["Away"]] = {"OffRtg":[],"DefRtg":[],"OREB%":[],"DREB%":[],"TOV%":[],"STL%":[],"TS%":[],"dTS%":[],"PACE":[],"LastG":datetime.date(1999,5,7),"GP":0}
        #more than 5 games played AND exclude covid bubble
        if (seasonDict[row["Away"]]["GP"] >= 5 and seasonDict[row["Home"]]["GP"] >= 5 and (not datetime.date(int(row["Date"].split("/")[2]), int(row["Date"].split("/")[0]), int(row["Date"].split("/")[1])).month == 8)):
            A.addCellToRow(row["Date"])
            A.addCellToRow(row["Home"])
            A.addCellToRow(row["Away"])
            A.addCellToRow(seasonDict[row["Home"]]["GP"])
            A.addCellToRow(seasonDict[row["Away"]]["GP"])
            A.addCellToRow(np.average(seasonDict[row["Home"]]["OffRtg"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["OffRtg"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DefRtg"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DefRtg"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["OREB%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["OREB%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DREB%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DREB%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["TOV%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["TOV%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["STL%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["STL%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["TS%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["TS%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["dTS%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["dTS%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["PACE"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["PACE"]))
            A.addCellToRow(abs(seasonDict[row["Home"]]["LastG"] - datetime.date(int(row["Date"].split("/")[2]), int(row["Date"].split("/")[0]), int(row["Date"].split("/")[1]))).days)
            A.addCellToRow(abs(seasonDict[row["Away"]]["LastG"] - datetime.date(int(row["Date"].split("/")[2]), int(row["Date"].split("/")[0]), int(row["Date"].split("/")[1]))).days)
            A.appendRow()
        seasonDict[row["Home"]]["OffRtg"].append(row["H_OffRtg"])
        seasonDict[row["Away"]]["OffRtg"].append(row["A_OffRtg"])
        seasonDict[row["Home"]]["DefRtg"].append(row["A_OffRtg"])
        seasonDict[row["Away"]]["DefRtg"].append(row["H_OffRtg"])
        seasonDict[row["Home"]]["OREB%"].append(row["H_OREB%"])
        seasonDict[row["Away"]]["OREB%"].append(row["A_OREB%"])
        seasonDict[row["Home"]]["DREB%"].append(100 - int(row["A_OREB%"]))
        seasonDict[row["Away"]]["DREB%"].append(100 - int(row["H_OREB%"]))
        seasonDict[row["Home"]]["TOV%"].append(row["H_TOV%"])
        seasonDict[row["Away"]]["TOV%"].append(row["A_TOV%"])
        seasonDict[row["Home"]]["STL%"].append(row["A_TOV%"])
        seasonDict[row["Away"]]["STL%"].append(row["H_TOV%"])
        seasonDict[row["Home"]]["TS%"].append(row["H_TS%"])
        seasonDict[row["Away"]]["TS%"].append(row["A_TS%"])
        seasonDict[row["Home"]]["dTS%"].append(row["A_TS%"])
        seasonDict[row["Away"]]["dTS%"].append(row["H_TS%"])
        seasonDict[row["Home"]]["PACE"].append(row["PACE"])
        seasonDict[row["Away"]]["PACE"].append(row["PACE"])
        seasonDict[row["Home"]]["LastG"] = datetime.date(int(row["Date"].split("/")[2]), int(row["Date"].split("/")[0]), int(row["Date"].split("/")[1]))
        seasonDict[row["Away"]]["LastG"] = datetime.date(int(row["Date"].split("/")[2]), int(row["Date"].split("/")[0]), int(row["Date"].split("/")[1]))
        seasonDict[row["Away"]]["GP"] += 1
        seasonDict[row["Home"]]["GP"] += 1

    if (writeToCsv):
        A.dictToCsv(write_path)
    return (A)

#matches the betting data with the pre match averages
def combineStatsAndBettingData(stats_path = './csv_data/mid_manipulation/pre_match_averages.csv', bets_path = './csv_data/raw/bettingLines.csv', write_path = './csv_data/mid_manipulation/combined_data.csv', writeToCsv = True):
    bets = pd.read_csv(bets_path, encoding = "ISO-8859-1")
    stats = pd.read_csv(stats_path, encoding = "ISO-8859-1")

    A = Database(["Date","Home","Away","Home ML","Away ML","Favorite","Spread","Home Spread Odds","Away Spread Odds","O/U","Over Odds","Under Odds","Home Score","Away Score","H_GP","A_GP","H_OffRtg","A_OffRtg","H_DefRtg","A_DefRtg","H_OREB%","A_OREB%","H_DREB%","A_DREB%","H_TOV%","A_TOV%","H_STL%","A_STL%","H_TS%","A_TS%","H_dTS%","A_dTS%","H_PACE","A_PACE","H_REST","A_REST"])

    for index, row in bets.iterrows():
        print (str(index) + "/" + str(len(bets.index)) + " games")
        if (index == 0 or abs(datetime.date(int(row["Date"].split(", ")[1].split()[2]), monthToInt(row["Date"].split(", ")[1].split()[1]), int(row["Date"].split(", ")[1].split()[0])) - datetime.date(int(bets.at[index-1,"Date"].split(", ")[1].split()[2]), monthToInt(bets.at[index-1,"Date"].split(", ")[1].split()[1]), int(bets.at[index-1,"Date"].split(", ")[1].split()[0]))).days > 100):
            if (index == 0):
                startIndex = 0
            else:
                startIndex = endIndex
            for i in range(startIndex, len(stats.index)):
                if (i == startIndex):
                    continue
                if (abs(datetime.date(int(stats.at[i,"Date"].split("/")[2]), int(stats.at[i,"Date"].split("/")[0]), int(stats.at[i,"Date"].split("/")[1])) - datetime.date(int(stats.at[i-1,"Date"].split("/")[2]), int(stats.at[i-1,"Date"].split("/")[0]), int(stats.at[i-1,"Date"].split("/")[1]))).days > 100):
                    endIndex = i
                    break

        for i in range(startIndex, endIndex):
            if (abs(datetime.date(int(row["Date"].split(", ")[1].split()[2]), monthToInt(row["Date"].split(", ")[1].split()[1]), int(row["Date"].split(", ")[1].split()[0])) - datetime.date(int(stats.at[i,"Date"].split("/")[2]), int(stats.at[i,"Date"].split("/")[0]), int(stats.at[i,"Date"].split("/")[1]))).days <= 1 and standardizeTeamName(row["Home"]) == standardizeTeamName(stats.at[i,"Home"]) and standardizeTeamName(row["Away"]) == standardizeTeamName(stats.at[i,"Away"])):
                for col in bets.columns:
                    if (col == "Home" or col == "Away"):
                        A.addCellToRow(standardizeTeamName(row[col]))
                    elif (col not in ["Season","url"]):
                        A.addCellToRow(row[col])
                for col in stats.columns:
                    if (col not in ["Date","Home","Away"]):
                        A.addCellToRow(stats.at[i,col])
                A.appendRow()
                break
    if (writeToCsv):
        A.dictToCsv(write_path)
    return (A)

#give it the first test season in the form of 2007/2008
def trainTestSplit(season = "2016/2017", data_path = "./csv_data/mid_manipulation/combined_data.csv"):
    data = pd.read_csv(data_path, encoding = "ISO-8859-1")
    split = False
    trainRows = []
    testRows = []
    for index, row in data.iterrows():
        if (int(row["Date"].split(", ")[1].split()[2]) == int(season.split("/")[1])):
            split = True
        if (split):
            testRows.append(index)
        else:
            trainRows.append(index)
    data.iloc[trainRows].to_csv(data_path.split(".csv")[0] + "_train.csv", index = False)
    data.iloc[testRows].to_csv(data_path.split(".csv")[0] + "_test.csv", index = False)

#formats the data for binary response model
def binClassificationTransform(train_path = "./csv_data/mid_manipulation/combined_data_train.csv", test_path = "./csv_data/mid_manipulation/combined_data_test.csv"):
    cols = ["Spread","O/U",]
    for x in ["Fav_","Dog_"]:
        cols.append(x + "Rtg")
        cols.append(x + "OREB%")
        cols.append(x + "TOV%")
        cols.append(x + "TS%")
        cols.append(x + "REST")
        cols.append(x + "PACE*Rtg")
        cols.append(x + "PACE*OREB%")
        cols.append(x + "PACE*TOV%")
        cols.append(x + "PACE*TS%")
    A = Database(cols)
    train = pd.read_csv(train_path, encoding = "ISO-8859-1")
    a = train["H_OffRtg"].to_list()
    a.extend(train["A_OffRtg"].to_list())
    rtgAvg = np.average(a)
    a = train["H_OREB%"].to_list()
    a.extend(train["A_OREB%"].to_list())
    orebAvg = np.average(a)
    a = train["H_TOV%"].to_list()
    a.extend(train["A_TOV%"].to_list())
    tovAvg = np.average(a)
    a = train["H_TS%"].to_list()
    a.extend(train["A_TS%"].to_list())
    tsAvg = np.average(a)
    a = train["H_PACE"].to_list()
    a.extend(train["A_PACE"].to_list())
    paceAvg = np.average(a)
    for index, row in train.iterrows():
        A.addCellToRow(row["Spread"])
        A.addCellToRow(row["O/U"])
        if (standardizeTeamName(row["Favorite"]) == row["Home"]):
            A.addCellToRow(float(row["H_OffRtg"]) + float(row["A_DefRtg"]) - rtgAvg)
            A.addCellToRow(float(row["H_OREB%"]) + 100 - float(row["A_DREB%"]) - orebAvg)
            A.addCellToRow(float(row["H_TOV%"]) + float(row["A_STL%"]) - tovAvg)
            A.addCellToRow(float(row["H_TS%"]) + float(row["A_dTS%"]) - tsAvg)
            A.addCellToRow(row["H_REST"])
            A.addCellToRow((float(row["H_OffRtg"]) + float(row["A_DefRtg"]) - rtgAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_OREB%"]) + 100 - float(row["A_DREB%"]) - orebAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_TOV%"]) + float(row["A_STL%"]) - tovAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_TS%"]) + float(row["A_dTS%"]) - tsAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow(float(row["A_OffRtg"]) + float(row["H_DefRtg"]) - rtgAvg)
            A.addCellToRow(float(row["A_OREB%"]) + 100 - float(row["H_DREB%"]) - orebAvg)
            A.addCellToRow(float(row["A_TOV%"]) + float(row["H_STL%"]) - tovAvg)
            A.addCellToRow(float(row["A_TS%"]) + float(row["H_dTS%"]) - tsAvg)
            A.addCellToRow(row["A_REST"])
            A.addCellToRow((float(row["A_OffRtg"]) + float(row["H_DefRtg"]) - rtgAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_OREB%"]) + 100 - float(row["H_DREB%"]) - orebAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_TOV%"]) + float(row["H_STL%"]) - tovAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_TS%"]) + float(row["H_dTS%"]) - tsAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
        else:
            A.addCellToRow(float(row["A_OffRtg"]) + float(row["H_DefRtg"]) - rtgAvg)
            A.addCellToRow(float(row["A_OREB%"]) + 100 - float(row["H_DREB%"]) - orebAvg)
            A.addCellToRow(float(row["A_TOV%"]) + float(row["H_STL%"]) - tovAvg)
            A.addCellToRow(float(row["A_TS%"]) + float(row["H_dTS%"]) - tsAvg)
            A.addCellToRow(row["A_REST"])
            A.addCellToRow((float(row["A_OffRtg"]) + float(row["H_DefRtg"]) - rtgAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_OREB%"]) + 100 - float(row["H_DREB%"]) - orebAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_TOV%"]) + float(row["H_STL%"]) - tovAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_TS%"]) + float(row["H_dTS%"]) - tsAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow(float(row["H_OffRtg"]) + float(row["A_DefRtg"]) - rtgAvg)
            A.addCellToRow(float(row["H_OREB%"]) + 100 - float(row["A_DREB%"]) - orebAvg)
            A.addCellToRow(float(row["H_TOV%"]) + float(row["A_STL%"]) - tovAvg)
            A.addCellToRow(float(row["H_TS%"]) + float(row["A_dTS%"]) - tsAvg)
            A.addCellToRow(row["H_REST"])
            A.addCellToRow((float(row["H_OffRtg"]) + float(row["A_DefRtg"]) - rtgAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_OREB%"]) + 100 - float(row["A_DREB%"]) - orebAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_TOV%"]) + float(row["A_STL%"]) - tovAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_TS%"]) + float(row["A_dTS%"]) - tsAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
        A.appendRow()
    df = A.getDataFrame()
    statCols = []
    #just diffs rn, the _aboveAvg part only is true after the regression, easier to just name it this now
    statCols.append("Rtg_diff_aboveAvg")
    statCols.append("OREB%_diff_aboveAvg")
    statCols.append("TOV%_diff_aboveAvg")
    statCols.append("TS%_diff_aboveAvg")
    statCols.append("REST_diff_aboveAvg")
    statCols.append("PACE*Rtg_total_aboveAvg")
    statCols.append("PACE*OREB%_total_aboveAvg")
    statCols.append("PACE*TOV%_total_aboveAvg")
    statCols.append("PACE*TS%_total_aboveAvg")
    interDict = {}
    for col in statCols:
        interDict[col] = []
    for index, row in df.iterrows():
        interDict["Rtg_diff_aboveAvg"].append(row["Fav_Rtg"] - row["Dog_Rtg"])
        interDict["OREB%_diff_aboveAvg"].append(row["Fav_OREB%"] - row["Dog_OREB%"])
        interDict["TOV%_diff_aboveAvg"].append(row["Fav_TOV%"] - row["Dog_TOV%"])
        interDict["TS%_diff_aboveAvg"].append(row["Fav_TS%"] - row["Dog_TS%"])
        interDict["REST_diff_aboveAvg"].append(row["Fav_REST"] - row["Dog_REST"])
        interDict["PACE*Rtg_total_aboveAvg"].append(row["Fav_PACE*Rtg"] + row["Dog_PACE*Rtg"])
        interDict["PACE*OREB%_total_aboveAvg"].append(row["Fav_PACE*OREB%"] + row["Dog_PACE*OREB%"])
        interDict["PACE*TOV%_total_aboveAvg"].append(row["Fav_PACE*TOV%"] + row["Dog_PACE*TOV%"])
        interDict["PACE*TS%_total_aboveAvg"].append(row["Fav_PACE*TS%"] + row["Dog_PACE*TS%"])
    modelDict = {}
    for col in statCols:
        if ("PACE" not in col):
            modelDict[col] = LinearRegression(fit_intercept = False).fit(X = df["Spread"].to_numpy().reshape(-1,1), y = np.array(interDict[col]).reshape(-1,1))
        else:
            modelDict[col] = LinearRegression(fit_intercept = False).fit(X = df["O/U"].to_numpy().reshape(-1,1), y = np.array(interDict[col]).reshape(-1,1))
    cols = ["Date","Favorite","Dog","FavHF","Spread","Fav Odds","Dog Odds","O/U","Over Odds","Under Odds","Fav Score","Dog Score","binSpread","binTotal"]
    cols.extend(statCols)
    B = Database(cols)
    for index, row in train.iterrows():
        B.addCellToRow(row["Date"])
        if ("OT" in row["Away Score"]):
            awayScore = int(row["Away Score"].split(" OT")[0])
        else:
            awayScore = int(row["Away Score"])
        if (row["Home"] == standardizeTeamName(row["Favorite"])):
            B.addCellToRow(row["Home"])
            B.addCellToRow(row["Away"])
            B.addCellToRow(1)
            B.addCellToRow(row["Spread"])
            B.addCellToRow(row["Home Spread Odds"])
            B.addCellToRow(row["Away Spread Odds"])
            B.addCellToRow(row["O/U"])
            B.addCellToRow(row["Over Odds"])
            B.addCellToRow(row["Under Odds"])
            B.addCellToRow(row["Home Score"])
            B.addCellToRow(row["Away Score"])
            if (int(row["Home Score"]) - float(row["Spread"]) > awayScore):
                B.addCellToRow(1)
            elif (int(row["Home Score"]) - float(row["Spread"]) < awayScore):
                B.addCellToRow(0)
            else:
                B.addCellToRow(np.nan)
            if (int(row["Home Score"]) + awayScore > float(row["O/U"])):
                B.addCellToRow(1)
            elif (int(row["Home Score"]) + awayScore < float(row["O/U"])):
                B.addCellToRow(0)
            else:
                B.addCellToRow(np.nan)
        else:
            B.addCellToRow(row["Away"])
            B.addCellToRow(row["Home"])
            B.addCellToRow(0)
            B.addCellToRow(row["Spread"])
            B.addCellToRow(row["Away Spread Odds"])
            B.addCellToRow(row["Home Spread Odds"])
            B.addCellToRow(row["O/U"])
            B.addCellToRow(row["Over Odds"])
            B.addCellToRow(row["Under Odds"])
            B.addCellToRow(row["Away Score"])
            B.addCellToRow(row["Home Score"])
            if (awayScore - float(row["Spread"]) > int(row["Home Score"])):
                B.addCellToRow(1)
            elif (awayScore - float(row["Spread"]) < int(row["Home Score"])):
                B.addCellToRow(0)
            else:
                B.addCellToRow(np.nan)
            if (int(row["Home Score"]) + awayScore > float(row["O/U"])):
                B.addCellToRow(1)
            elif (int(row["Home Score"]) + awayScore < float(row["O/U"])):
                B.addCellToRow(0)
            else:
                B.addCellToRow(np.nan)
        for col in statCols:
            if ("PACE" not in col):
                tempArray = np.array(row["Spread"])
                B.addCellToRow(interDict[col][index] - modelDict[col].predict(tempArray.reshape(1,-1))[0][0])
            else:
                tempArray = np.array(row["O/U"])
                B.addCellToRow(interDict[col][index] - modelDict[col].predict(tempArray.reshape(1,-1))[0][0])
        B.appendRow()
    B.dictToCsv("./csv_data/mid_manipulation/logistic_regression_ready_train.csv")


    test = pd.read_csv(test_path, encoding = "ISO-8859-1")
    cols = ["Spread","O/U",]
    for x in ["Fav_","Dog_"]:
        cols.append(x + "Rtg")
        cols.append(x + "OREB%")
        cols.append(x + "TOV%")
        cols.append(x + "TS%")
        cols.append(x + "REST")
        cols.append(x + "PACE*Rtg")
        cols.append(x + "PACE*OREB%")
        cols.append(x + "PACE*TOV%")
        cols.append(x + "PACE*TS%")
    A = Database(cols)
    for index, row in test.iterrows():
        A.addCellToRow(row["Spread"])
        A.addCellToRow(row["O/U"])
        if (standardizeTeamName(row["Favorite"]) == row["Home"]):
            A.addCellToRow(float(row["H_OffRtg"]) + float(row["A_DefRtg"]) - rtgAvg)
            A.addCellToRow(float(row["H_OREB%"]) + 100 - float(row["A_DREB%"]) - orebAvg)
            A.addCellToRow(float(row["H_TOV%"]) + float(row["A_STL%"]) - tovAvg)
            A.addCellToRow(float(row["H_TS%"]) + float(row["A_dTS%"]) - tsAvg)
            A.addCellToRow(row["H_REST"])
            A.addCellToRow((float(row["H_OffRtg"]) + float(row["A_DefRtg"]) - rtgAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_OREB%"]) + 100 - float(row["A_DREB%"]) - orebAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_TOV%"]) + float(row["A_STL%"]) - tovAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_TS%"]) + float(row["A_dTS%"]) - tsAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow(float(row["A_OffRtg"]) + float(row["H_DefRtg"]) - rtgAvg)
            A.addCellToRow(float(row["A_OREB%"]) + 100 - float(row["H_DREB%"]) - orebAvg)
            A.addCellToRow(float(row["A_TOV%"]) + float(row["H_STL%"]) - tovAvg)
            A.addCellToRow(float(row["A_TS%"]) + float(row["H_dTS%"]) - tsAvg)
            A.addCellToRow(row["A_REST"])
            A.addCellToRow((float(row["A_OffRtg"]) + float(row["H_DefRtg"]) - rtgAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_OREB%"]) + 100 - float(row["H_DREB%"]) - orebAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_TOV%"]) + float(row["H_STL%"]) - tovAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_TS%"]) + float(row["H_dTS%"]) - tsAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
        else:
            A.addCellToRow(float(row["A_OffRtg"]) + float(row["H_DefRtg"]) - rtgAvg)
            A.addCellToRow(float(row["A_OREB%"]) + 100 - float(row["H_DREB%"]) - orebAvg)
            A.addCellToRow(float(row["A_TOV%"]) + float(row["H_STL%"]) - tovAvg)
            A.addCellToRow(float(row["A_TS%"]) + float(row["H_dTS%"]) - tsAvg)
            A.addCellToRow(row["A_REST"])
            A.addCellToRow((float(row["A_OffRtg"]) + float(row["H_DefRtg"]) - rtgAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_OREB%"]) + 100 - float(row["H_DREB%"]) - orebAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_TOV%"]) + float(row["H_STL%"]) - tovAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow((float(row["A_TS%"]) + float(row["H_dTS%"]) - tsAvg) * (float(row["A_PACE"]) + float(row["H_PACE"]) - paceAvg))
            A.addCellToRow(float(row["H_OffRtg"]) + float(row["A_DefRtg"]) - rtgAvg)
            A.addCellToRow(float(row["H_OREB%"]) + 100 - float(row["A_DREB%"]) - orebAvg)
            A.addCellToRow(float(row["H_TOV%"]) + float(row["A_STL%"]) - tovAvg)
            A.addCellToRow(float(row["H_TS%"]) + float(row["A_dTS%"]) - tsAvg)
            A.addCellToRow(row["H_REST"])
            A.addCellToRow((float(row["H_OffRtg"]) + float(row["A_DefRtg"]) - rtgAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_OREB%"]) + 100 - float(row["A_DREB%"]) - orebAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_TOV%"]) + float(row["A_STL%"]) - tovAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
            A.addCellToRow((float(row["H_TS%"]) + float(row["A_dTS%"]) - tsAvg) * (float(row["H_PACE"]) + float(row["A_PACE"]) - paceAvg))
        A.appendRow()
    df = A.getDataFrame()
    statCols = []
    #just diffs rn, the _aboveAvg part only is true after the regression, easier to just name it this now
    statCols.append("Rtg_diff_aboveAvg")
    statCols.append("OREB%_diff_aboveAvg")
    statCols.append("TOV%_diff_aboveAvg")
    statCols.append("TS%_diff_aboveAvg")
    statCols.append("REST_diff_aboveAvg")
    statCols.append("PACE*Rtg_total_aboveAvg")
    statCols.append("PACE*OREB%_total_aboveAvg")
    statCols.append("PACE*TOV%_total_aboveAvg")
    statCols.append("PACE*TS%_total_aboveAvg")
    interDict = {}
    for col in statCols:
        interDict[col] = []
    for index, row in df.iterrows():
        interDict["Rtg_diff_aboveAvg"].append(row["Fav_Rtg"] - row["Dog_Rtg"])
        interDict["OREB%_diff_aboveAvg"].append(row["Fav_OREB%"] - row["Dog_OREB%"])
        interDict["TOV%_diff_aboveAvg"].append(row["Fav_TOV%"] - row["Dog_TOV%"])
        interDict["TS%_diff_aboveAvg"].append(row["Fav_TS%"] - row["Dog_TS%"])
        interDict["REST_diff_aboveAvg"].append(row["Fav_REST"] - row["Dog_REST"])
        interDict["PACE*Rtg_total_aboveAvg"].append(row["Fav_PACE*Rtg"] + row["Dog_PACE*Rtg"])
        interDict["PACE*OREB%_total_aboveAvg"].append(row["Fav_PACE*OREB%"] + row["Dog_PACE*OREB%"])
        interDict["PACE*TOV%_total_aboveAvg"].append(row["Fav_PACE*TOV%"] + row["Dog_PACE*TOV%"])
        interDict["PACE*TS%_total_aboveAvg"].append(row["Fav_PACE*TS%"] + row["Dog_PACE*TS%"])
    cols = ["Date","Favorite","Dog","FavHF","Spread","Fav Odds","Dog Odds","O/U","Over Odds","Under Odds","Fav Score","Dog Score","binSpread","binTotal"]
    cols.extend(statCols)
    B = Database(cols)
    for index, row in test.iterrows():
        B.addCellToRow(row["Date"])
        if ("OT" in row["Away Score"]):
            awayScore = int(row["Away Score"].split(" OT")[0])
        else:
            awayScore = int(row["Away Score"])
        if (row["Home"] == standardizeTeamName(row["Favorite"])):
            B.addCellToRow(row["Home"])
            B.addCellToRow(row["Away"])
            B.addCellToRow(1)
            B.addCellToRow(row["Spread"])
            B.addCellToRow(row["Home Spread Odds"])
            B.addCellToRow(row["Away Spread Odds"])
            B.addCellToRow(row["O/U"])
            B.addCellToRow(row["Over Odds"])
            B.addCellToRow(row["Under Odds"])
            B.addCellToRow(row["Home Score"])
            B.addCellToRow(row["Away Score"])
            if (int(row["Home Score"]) - float(row["Spread"]) > awayScore):
                B.addCellToRow(1)
            elif (int(row["Home Score"]) - float(row["Spread"]) < awayScore):
                B.addCellToRow(0)
            else:
                B.addCellToRow(np.nan)
            if (int(row["Home Score"]) + awayScore > float(row["O/U"])):
                B.addCellToRow(1)
            elif (int(row["Home Score"]) + awayScore < float(row["O/U"])):
                B.addCellToRow(0)
            else:
                B.addCellToRow(np.nan)
        else:
            B.addCellToRow(row["Away"])
            B.addCellToRow(row["Home"])
            B.addCellToRow(0)
            B.addCellToRow(row["Spread"])
            B.addCellToRow(row["Away Spread Odds"])
            B.addCellToRow(row["Home Spread Odds"])
            B.addCellToRow(row["O/U"])
            B.addCellToRow(row["Over Odds"])
            B.addCellToRow(row["Under Odds"])
            B.addCellToRow(row["Away Score"])
            B.addCellToRow(row["Home Score"])
            if (awayScore - float(row["Spread"]) > int(row["Home Score"])):
                B.addCellToRow(1)
            elif (awayScore - float(row["Spread"]) < int(row["Home Score"])):
                B.addCellToRow(0)
            else:
                B.addCellToRow(np.nan)
            if (int(row["Home Score"]) + awayScore > float(row["O/U"])):
                B.addCellToRow(1)
            elif (int(row["Home Score"]) + awayScore < float(row["O/U"])):
                B.addCellToRow(0)
            else:
                B.addCellToRow(np.nan)
        for col in statCols:
            if ("PACE" not in col):
                tempArray = np.array(row["Spread"])
                B.addCellToRow(interDict[col][index] - modelDict[col].predict(tempArray.reshape(1,-1))[0][0])
            else:
                tempArray = np.array(row["O/U"])
                B.addCellToRow(interDict[col][index] - modelDict[col].predict(tempArray.reshape(1,-1))[0][0])
        B.appendRow()
    B.dictToCsv("./csv_data/mid_manipulation/logistic_regression_ready_test.csv")

#does logistic regression
def logisticRegression(train_path = "./csv_data/mid_manipulation/logistic_regression_ready_train.csv", test_path = "./csv_data/mid_manipulation/logistic_regression_ready_test.csv"):
    train = pd.read_csv(train_path, encoding = "ISO-8859-1")
    test = pd.read_csv(test_path, encoding = "ISO-8859-1")

    predictions = []
    spreadTrain = train[train["binSpread"].notna()]
    y_train = spreadTrain["binSpread"]
    xCols = ["FavHF","Rtg_diff_aboveAvg","OREB%_diff_aboveAvg","TOV%_diff_aboveAvg","TS%_diff_aboveAvg","REST_diff_aboveAvg"]
    scaler = StandardScaler()
    X_train = pd.DataFrame(spreadTrain, columns = xCols)
    X_train[xCols] = scaler.fit_transform(X_train[xCols])
    X_test = pd.DataFrame(test, columns = xCols)
    X_test[xCols] = scaler.transform(X_test[xCols])
    model = LogisticRegression(max_iter = 100000, C = 999999999)
    model.fit(X = X_train, y = y_train)
    for p in model.predict_proba(X_test):
        if (model.classes_[1] == 1):
            predictions.append(p[1])
        else:
            predictions.append(p[0])
    test["Spread PFITS"] = predictions

    predictions = []
    totalTrain = train[train["binTotal"].notna()]
    y_train = totalTrain["binTotal"]
    xCols = ["PACE*Rtg_total_aboveAvg","PACE*OREB%_total_aboveAvg","PACE*TOV%_total_aboveAvg","PACE*TS%_total_aboveAvg"]
    scaler = StandardScaler()
    X_train = pd.DataFrame(totalTrain, columns = xCols)
    X_train[xCols] = scaler.fit_transform(X_train[xCols])
    X_test = pd.DataFrame(test, columns = xCols)
    X_test[xCols] = scaler.transform(X_test[xCols])
    model = LogisticRegression(max_iter = 100000, C = 999999999)
    model.fit(X = X_train, y = y_train)
    for p in model.predict_proba(X_test):
        if (model.classes_[1] == 1):
            predictions.append(p[1])
        else:
            predictions.append(p[0])
    test["Total PFITS"] = predictions

    test.to_csv("./csv_data/mid_manipulation/predictions.csv", index = False)
