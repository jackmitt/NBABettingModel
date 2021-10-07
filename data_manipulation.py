import pandas as pd
import numpy as np
from classes import Database

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
def getPreMatchAverages(read_path = './csv_data/mid_manipulation/merged_matches.csv', write_path, writeToCsv = True):
    stats = pd.read_csv(read_path, encoding = "ISO-8859-1")
    A = Database(["Date","Home","Away","H_GP","A_GP","H_OffRtg","A_OffRtg","H_DefRtg","A_DefRtg","H_OREB%","A_OREB%","H_DREB%","A_DREB%","H_TOV%","A_TOV%","H_STL%","A_STL%","H_TS%","A_TS%","H_dTS%","A_dTS%","PACE","H_REST","A_REST"])
    for index, row in stats.iterrows():
        if (index == 0 or int(row["Game Date"].split("/")[0]) - 3 > int(stats.at[index-1,"Game Date"].split("/")[0])):
            #new season
