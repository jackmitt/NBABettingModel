from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from helpers.classes import Database

## Scrapes regular season closing betting lines from oddsportal (consensus average) for all seasons since 2008/2009 and saves them to a csv - Make sure you have chromedriver.exe for the correct version of Chrome
## Take out the covid bubble games yourself manually

seasons = []
for i in range(2008, 2021):
    seasons.append(str(i) + "-" + str(i+1))

A = Database(["Season","Date","Home","Away","Home ML","Away ML","Favorite","Spread","Home Spread Odds","Away Spread Odds","O/U","Over Odds","Under Odds","Home Score","Away Score"])


gameUrls = []
browser = webdriver.Chrome(executable_path='chromedriver.exe')
for season in seasons:
    browser.get("https://www.oddsportal.com/basketball/usa/nba-" + season + "/results/")
    browser.maximize_window()
    for i in range(30):
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        main = soup.find(class_=" table-main")
        regSeason = False
        for row in main.find_all("tr"):
            if ("nob-border" in row["class"]):
                if ("Offs" in row.find("th").text or "Pre" in row.find("th").text):
                    regSeason = False
                else:
                    regSeason = True
            if (regSeason and "deactivate" in row["class"]):
                gameUrls.append("https://www.oddsportal.com/" + row.find(class_="name table-participant").find("a")["href"])
        browser.find_element_by_xpath("//*[@id='pagination']/a[13]/span").click()
        time.sleep(3)

for game in gameUrls:
    browser.get(game)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    #season
    A.addCellToRow(game.split("nba-")[1].split("-")[0] + '/' + game.split("nba-")[1].split("-")[1].split("/")[0])
    #date
    A.addCellToRow(soup.find(id="col-content").find("p").text)
    #home
    A.addCellToRow(soup.find(id="col-content").find("h1").text.split(" - ")[0])
    #away
    A.addCellToRow(soup.find(id="col-content").find("h1").text.split(" - ")[1])
    #moneylines
    for row in soup.find(class_="table-container").find_all("tr"):
        try:
            sportsbook = row.find(class_="name").text
        except:
            continue
        if (sportsbook == "Pinnacle"):
            #home
            A.addCellToRow(row.find_all("td")[1].text)
            #away
            A.addCellToRow(row.find_all("td")[2].text)
    #spread stuff
    browser.find_element_by_xpath("//*[@id='bettype-tabs']/ul/li[4]/a/span").click()
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    bestPayout = -1
    for option in soup.find(id="odds-data-table").find_all("div"):
        try:
            payout = float(option.find(class_="avg chunk-odd-payout").text.split("%")[0])
        except:
            continue
        if (payout > bestPayout):
            bestSpread = option
            bestPayout = payout
    #favorite
    if ("+" in bestSpread.find("a").text):
        A.addCellToRow(soup.find(id="col-content").find("h1").text.split(" - ")[1])
    else:
        A.addCellToRow(soup.find(id="col-content").find("h1").text.split(" - ")[0])
    #spread
    if ("+" in bestSpread.find("a").text):
        A.addCellToRow(bestSpread.find("a").text.split("+")[1])
    else:
        A.addCellToRow(bestSpread.find("a").text.split("-")[1])
    #home spread odds
    A.addCellToRow(bestSpread.find_all("a")[1].text)
    #away spread odds
    A.addCellToRow(bestSpread.find_all("a")[2].text)
    #O/U stuff
    browser.find_element_by_xpath("//*[@id='bettype-tabs']/ul/li[5]/a/span").click()
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    bestPayout = -1
    for option in soup.find(id="odds-data-table").find_all("div"):
        try:
            payout = float(option.find(class_="avg chunk-odd-payout").text.split("%")[0])
        except:
            continue
        if (payout > bestPayout):
            bestTotal = option
            bestPayout = payout
    #O/U
    A.addCellToRow(bestSpread.find("a").text.split("+")[1])
    #over odds
    A.addCellToRow(bestSpread.find_all("a")[1].text)
    #under odds
    A.addCellToRow(bestSpread.find_all("a")[2].text)
    #home score
    A.addCellToRow(soup.find(class_="result").find("strong").text.split(":")[0])
    #away score
    A.addCellToRow(soup.find(class_="result").find("strong").text.split(":")[1])
    A.appendRow()

A.dictToCsv("./csv_data/bettingLines.csv")
broswer.close()
