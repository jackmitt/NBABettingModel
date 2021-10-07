import pandas as pd
import numpy as np
from classes import Database
import datetime

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
        if (seasonDict[row["Away"]]["GP"] != 0 and seasonDict[row["Home"]]["GP"] != 0):
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
