from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

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
