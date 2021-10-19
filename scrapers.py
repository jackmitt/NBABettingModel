from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from os.path import exists
from prediction_evaluation import americanToDecimal
from helpers import Database
import datetime

## Scrapes regular season closing betting lines from oddsportal (consensus average) for all seasons since 2008/2009 and saves them to a csv - Make sure you have chromedriver.exe for the correct version of Chrome
## Take out the covid bubble games yourself manually
def oddsportal(yearStart, yearEnd):
    A = Database(["Season","Date","Home","Away","Home ML","Away ML","Favorite","Spread","Home Spread Odds","Away Spread Odds","O/U","Over Odds","Under Odds","Home Score","Away Score","url"])
    seasons = []
    for i in range(yearStart, yearEnd+1):
        seasons.append(str(i) + "-" + str(i+1))
    browser = webdriver.Chrome(executable_path='chromedriver.exe')
    if (not exists("./gameUrls.csv")):
        gameUrls = []
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
        save = {}
        save["urls"] = gameUrls
        dfFinal = pd.DataFrame.from_dict(save)
        dfFinal = dfFinal.drop_duplicates()
        dfFinal.to_csv("./gameUrls.csv", index = False)
    else:
        gameUrls = pd.read_csv('./gameUrls.csv', encoding = "ISO-8859-1")["urls"].tolist()

    counter = 0
    if (exists("./csv_data/bettingLines.csv")):
        A.initDictFromCsv("./csv_data/bettingLines.csv")
        scrapedGames = pd.read_csv('./csv_data/bettingLines.csv', encoding = "ISO-8859-1")["url"].tolist()
        for game in scrapedGames:
            gameUrls.remove(game)
    try:
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
            pinnacleFound = False
            for row in soup.find(class_="table-container").find_all("tr"):
                try:
                    sportsbook = row.find(class_="name").text
                except:
                    continue
                if (sportsbook == "Pinnacle"):
                    pinnacleFound = True
                    #home
                    A.addCellToRow(row.find_all("td")[1].text)
                    #away
                    A.addCellToRow(row.find_all("td")[2].text)
            if (not pinnacleFound):
                A.addCellToRow(np.nan)
                A.addCellToRow(np.nan)
            #spread stuff
            try:
                browser.find_element_by_xpath("//*[@id='bettype-tabs']/ul/li[4]/a/span").click()
            except:
                A.trashRow()
                continue
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            minDiff = 99999
            for option in soup.find(id="odds-data-table").find_all("div"):
                try:
                    diff = abs(americanToDecimal(float(option.find_all("a")[1].text)) - americanToDecimal(float(option.find_all("a")[2].text)))
                    sp1 = americanToDecimal(float(option.find_all("a")[1].text))
                    sp2 = americanToDecimal(float(option.find_all("a")[2].text))
                except:
                    continue
                if (diff < minDiff and sp1 > 1.87 and sp2 > 1.87):
                    bestSpread = option
                    minDiff = diff
            #favorite
            try:
                if ("+" in bestSpread.find("a").text):
                    A.addCellToRow(soup.find(id="col-content").find("h1").text.split(" - ")[1])
                elif ("-" in bestSpread.find("a").text):
                    A.addCellToRow(soup.find(id="col-content").find("h1").text.split(" - ")[0])
                else:
                    A.addCellToRow("Even")
            except:
                A.trashRow()
                continue
            #spread
            if ("+" in bestSpread.find("a").text):
                A.addCellToRow(bestSpread.find("a").text.split("+")[1])
            elif ("-" in bestSpread.find("a").text):
                A.addCellToRow(bestSpread.find("a").text.split("-")[1])
            else:
                A.addCellToRow(0)
            #home spread odds
            A.addCellToRow(bestSpread.find_all("a")[1].text)
            #away spread odds
            A.addCellToRow(bestSpread.find_all("a")[2].text)
            #O/U stuff
            browser.find_element_by_xpath("//*[@id='bettype-tabs']/ul/li[5]/a/span").click()
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            minDiff = 99999
            for option in soup.find(id="odds-data-table").find_all("div"):
                try:
                    diff = abs(americanToDecimal(float(option.find_all("a")[1].text)) - americanToDecimal(float(option.find_all("a")[2].text)))
                    sp1 = americanToDecimal(float(option.find_all("a")[1].text))
                    sp2 = americanToDecimal(float(option.find_all("a")[2].text))
                except:
                    continue
                if (diff < minDiff and sp1 > 1.85 and sp2 > 1.85):
                    bestTotal = option
                    minDiff = diff
            #O/U
            try:
                A.addCellToRow(bestTotal.find("a").text.split("+")[1])
            except:
                A.trashRow()
                continue
            #over odds
            try:
                A.addCellToRow(bestTotal.find_all("a")[1].text)
                #under odds
                A.addCellToRow(bestTotal.find_all("a")[2].text)
            except:
                A.trashRow()
                continue
            #home score
            try:
                A.addCellToRow(soup.find(class_="result").find("strong").text.split(":")[0])
            except:
                A.trashRow()
                continue
            #away score
            A.addCellToRow(soup.find(class_="result").find("strong").text.split(":")[1])
            A.addCellToRow(game)
            A.appendRow()
            counter += 1
            if (counter % 3 == 1):
                A.dictToCsv("./csv_data/bettingLines.csv")
    except:
        browser.close()
        print ("SCRAPER FAILED. RESTARTING...")
        historicOdds(yearStart, yearEnd)

    A.dictToCsv("./csv_data/bettingLines.csv")
    browser.close()

## Scrapes traditional and advanced box scores from nba.com since 2005/06 season
def nbaBoxScores(A, boxScoreType = "traditional"):
    browser = webdriver.Chrome(executable_path='chromedriver.exe')
    for i in reversed(range(16)):
        browser.get("https://www.nba.com/stats/teams/boxscores-" + boxScoreType + "/?Season=2005-06&SeasonType=Regular%20Season")
        browser.maximize_window()
        browser.find_element_by_xpath("/html/body/main/div/div/div[2]/div/div/div[1]/div[1]/div/div/label/select").click()
        browser.find_element_by_xpath("/html/body/main/div/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[" + str(i+2) + "]").click()
        time.sleep(10)
        browser.find_element_by_xpath("/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select").click()
        browser.find_element_by_xpath("/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select/option[1]").click()
        time.sleep(45)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        if (i == 15):
            for col in soup.find(class_="nba-stat-table").find("tr").find_all("th"):
                name = ""
                for x in col.get_text().split():
                    if (name == ""):
                        name = x
                    else:
                        name = name + " " + x
                A.addColumn(name)
        for row in soup.find(class_="nba-stat-table").find("tbody").find_all("tr"):
            for cell in row.find_all("td"):
                # if (cell.has_attr("class") and "hidden" in cell["class"]):
                #     continue
                if (len(cell.get_text().split()) == 1):
                    A.addCellToRow(cell.get_text().split()[0])
                else:
                    mu = ""
                    for x in cell.get_text().split():
                        if (mu == ""):
                            mu = x
                        else:
                            mu = mu + " " + x
                    A.addCellToRow(mu)
            A.appendRow()
    A.dictToCsv("./csv_data/" + boxScoreType + "_stats.csv")
    browser.close()

##Using this site since oddsportal gives faulty numbers sometimes and I am fed up
def sbrOdds():
    date = datetime.date(2006, 10, 31)
    A = Database(["Date","Home","Away","Favorite","Spread","Home Spread Odds","Away Spread Odds","O/U","Over Odds","Under Odds","Home Score","Away Score"])
    browser = webdriver.Chrome(executable_path='chromedriver.exe')
    counter = 0
    browser.get(date.strftime("https://www.sportsbookreview.com/betting-odds/nba-basketball/merged/?date=20061031"))
    browser.maximize_window()
    browser.find_element_by_xpath("//*[@id='bettingOddsGridContainer']/div[3]/div[1]/div[2]/div/div/div").click()
    while (date < datetime.date(2021, 10, 1)):
        browser.get(date.strftime("https://www.sportsbookreview.com/betting-odds/nba-basketball/merged/?date=%Y%m%d"))
        time.sleep(3)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        if (date.year < 2020 and date.month == 6):
            date = date + datetime.timedelta(days=120)
            continue
        if (len(soup.find_all(class_="noEvents-1qOEP")) > 0):
            date = date + datetime.timedelta(days=1)
            continue
        table = soup.find(class_="eventsByLeague-2wGLV")
        for i in range(len(table.find_all(class_="compactBettingOptionContainer-VVPjh"))):
            row = table.find_all(class_="compactBettingOptionContainer-VVPjh")[i]
            A.addCellToRow(date)
            A.addCellToRow(row.find_all(class_="participantBox-3ar9Y")[1].text)
            A.addCellToRow(row.find_all(class_="participantBox-3ar9Y")[0].text)
            odds = table.find_all(class_="container-341kQ")[1+i]
            top = odds.find_all(class_="pointer-2j4Dk margin-2SxKQ")[0]
            bot = odds.find_all(class_="pointer-2j4Dk margin-2SxKQ")[1]
            if ("-" in top.find("span").text):
                try:
                    A.addCellToRow(row.find_all(class_="participantBox-3ar9Y")[0].text)
                    if ("½" in top.find("span").text.split("-")[1]):
                        A.addCellToRow(top.find("span").text.split("-")[1].split("½")[0] + ".5")
                    else:
                        A.addCellToRow(top.find("span").text.split("-")[1])
                    A.addCellToRow(top.find_all("span")[1].text)
                    A.addCellToRow(-220 - int(top.find_all("span")[1].text))
                    if ("½" in bot.find("span").text):
                        A.addCellToRow(bot.find("span").text.split("½")[0] + ".5")
                    else:
                        A.addCellToRow(bot.find("span").text)
                    A.addCellToRow(bot.find_all("span")[1].text)
                    A.addCellToRow(-220 - int(bot.find_all("span")[1].text))
                except:
                    A.trashRow()
                    continue
            else:
                try:
                    A.addCellToRow(row.find_all(class_="participantBox-3ar9Y")[1].text)
                    if ("½" in bot.find("span").text.split("-")[1]):
                        A.addCellToRow(bot.find("span").text.split("-")[1].split("½")[0] + ".5")
                    else:
                        A.addCellToRow(bot.find("span").text.split("-")[1])
                    A.addCellToRow(bot.find_all("span")[1].text)
                    A.addCellToRow(-220 - int(bot.find_all("span")[1].text))
                    if ("½" in top.find("span").text):
                        A.addCellToRow(top.find("span").text.split("½")[0] + ".5")
                    else:
                        A.addCellToRow(top.find("span").text)
                    A.addCellToRow(top.find_all("span")[1].text)
                    A.addCellToRow(-220 - int(top.find_all("span")[1].text))
                except:
                    A.trashRow()
                    continue
            A.addCellToRow(row.find_all(class_="scores-1-KV5 undefined")[1].text)
            A.addCellToRow(row.find_all(class_="scores-1-KV5 undefined")[0].text)
            A.appendRow()
            counter += 1
            if (counter % 10 == 1):
                A.dictToCsv("./csv_data/raw/sbrOdds.csv")
        date = date + datetime.timedelta(days=1)
