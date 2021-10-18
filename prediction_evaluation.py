import pandas as pd
import numpy as np
from helpers import Database
import datetime
from helpers import monthToInt

def americanToDecimal(odds):
    if (odds < 0):
        return (1 - (100 / odds))
    else:
        return (odds/100 + 1)

def kellyStake(p, decOdds):
    return (p - (1 - p)/(decOdds - 1))

def simulateTestBets(bankroll, kellyDiv = 1, pred_path = "./csv_data/mid_manipulation/predictions_validation.csv", spread = True, ou = True):
    pred = pd.read_csv(pred_path, encoding = "ISO-8859-1")
    tempBR = bankroll
    for index, row in pred.iterrows():
        print (index)
        if (index == 0 or datetime.date(int(row["Date"].split(", ")[1].split()[2]), monthToInt(row["Date"].split(", ")[1].split()[1]), int(row["Date"].split(", ")[1].split()[0])) != datetime.date(int(pred.at[index-1,"Date"].split(", ")[1].split()[2]), monthToInt(pred.at[index-1,"Date"].split(", ")[1].split()[1]), int(pred.at[index-1,"Date"].split(", ")[1].split()[0]))):
            bankroll = tempBR
            print (bankroll)
        if (spread):
            if (row["Spread PFITS"] > 1 / americanToDecimal(row["Fav Odds"])):
                if (row["binSpread"] == 1):
                    tempBR += bankroll * kellyStake(row["Spread PFITS"], americanToDecimal(row["Fav Odds"])) * (americanToDecimal(row["Fav Odds"]) - 1) / kellyDiv
                elif (row["binSpread"] == 0):
                    tempBR -= bankroll * kellyStake(row["Spread PFITS"], americanToDecimal(row["Fav Odds"])) / kellyDiv
            elif (1 - row["Spread PFITS"] > 1 / americanToDecimal(row["Dog Odds"])):
                if (row["binSpread"] == 0):
                    tempBR += bankroll * kellyStake(1 - row["Spread PFITS"], americanToDecimal(row["Dog Odds"])) * (americanToDecimal(row["Dog Odds"]) - 1) / kellyDiv
                elif (row["binSpread"] == 1):
                    tempBR -= bankroll * kellyStake(1 - row["Spread PFITS"], americanToDecimal(row["Dog Odds"])) / kellyDiv
        if (ou):
            if (row["Total PFITS"] > 1 / americanToDecimal(row["Over Odds"])):
                if (row["binTotal"] == 1):
                    tempBR += bankroll * kellyStake(row["Total PFITS"], americanToDecimal(row["Over Odds"])) * (americanToDecimal(row["Over Odds"]) - 1) / kellyDiv
                elif (row["binTotal"] == 0):
                    tempBR -= bankroll * kellyStake(row["Total PFITS"], americanToDecimal(row["Over Odds"])) / kellyDiv
            elif (1 - row["Total PFITS"] > 1 / americanToDecimal(row["Under Odds"])):
                if (row["binTotal"] == 0):
                    tempBR += bankroll * kellyStake(1 - row["Total PFITS"], americanToDecimal(row["Under Odds"])) * (americanToDecimal(row["Under Odds"]) - 1) / kellyDiv
                elif (row["binTotal"] == 1):
                    tempBR -= bankroll * kellyStake(1 - row["Total PFITS"], americanToDecimal(row["Under Odds"])) / kellyDiv
    print (bankroll)
