from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from helpers.classes import Database

## Scrapes regular season closing betting lines from oddsportal (Pinnacle where possible) for all seasons since 2008/2009 and saves them to a csv - Make sure you have chromedriver.exe for the correct version of Chrome
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

broswer.close()
