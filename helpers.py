import pandas as pd
import numpy as np

class Database:
    def __init__(self, keys = []):
        self.df = pd.DataFrame()
        self.dict = {}
        for key in keys:
            self.dict[key] = []
        self.tempRow = []

    def getKeys(self):
        return (list(self.dict.keys()))

    def getCol(self, colName):
        return (self.dict[colName])

    def getLength(self):
        return (len(list(self.dict.keys())[0]))

    def initDictFromCsv(self, path):
        self.dict = pd.read_csv(path, encoding = "ISO-8859-1").to_dict(orient="list")

    def addColumn(self, colName):
        self.dict[colName] = []

    def addCellToRow(self, datum):
        if (len(self.tempRow) + 1 > len(self.dict)):
            raise ValueError("The row is already full")
        else:
            self.tempRow.append(datum)

    def appendRow(self):
        if (len(self.tempRow) != len(self.dict)):
            raise ValueError("The row is not fully populated")
        else:
            for i in range(len(self.dict.keys())):
                self.dict[list(self.dict.keys())[i]].append(self.tempRow[i])
            self.tempRow = []

    def trashRow(self):
        self.tempRow = []

    def dictToCsv(self, pathName):
        self.df = pd.DataFrame.from_dict(self.dict)
        self.df = self.df.drop_duplicates()
        self.df.to_csv(pathName, index = False)

    def printRow(self):
        print(self.tempRow)

    def reset(self):
        self.tempRow = []
        self.dict = {}
        for key in list(self.dict.keys()):
            self.dict[key] = []

    def merge(self, B):
        for key in B.getKeys():
            if (key not in list(self.dict.keys())):
                self.dict[key] = B.getCol(key)

def standardizeTeamName(name):
    name = name.lower()
    if ("golden" in name or name == 'gsw'):
        return ('GSW')
    if ("memphis" in name or name == 'mem'):
        return ('MEM')
    if ("chicago" in name or name == 'chi'):
        return ('CHI')
    if ("phoenix" in name or name == 'phx'):
        return ('PHX')
    if ("boston" in name or name == 'bos'):
        return ('BOS')
    if ("milwaukee" in name or name == 'mil'):
        return ('MIL')
    if ("clipper" in name or name == 'lac'):
        return ('LAC')
    if ("laker" in name or name == 'lal'):
        return ('LAL')
    if ("houston" in name or name == 'hou'):
        return ('HOU')
    if ("cleveland" in name or name == 'cle'):
        return ('CLE')
    if ("new orleans" in name or name == "noh" or name == 'nop'):
        return ('NOP')
    if ("miami" in name or name == 'mia'):
        return ('MIA')
    if ("portland" in name or name == 'por'):
        return ('POR')
    if ("minnesota" in name or name == 'min'):
        return ('MIN')
    if ("detroit" in name or name == 'det'):
        return ('DET')
    if ("knick" in name or name == 'nyk'):
        return ('NYK')
    if ("utah" in name or name == 'uta'):
        return ('UTA')
    if ("sacramento" in name or name == 'sac'):
        return ('SAC')
    if ("dallas" in name or name == 'dal'):
        return ('DAL')
    if ("charlotte" in name or name == 'cha'):
        return ('CHA')
    if ("toronto" in name or name == 'tor'):
        return ('TOR')
    if ("denver" in name or name == 'den'):
        return ('DEN')
    if ("indiana" in name or name == 'ind'):
        return ('IND')
    if ("oklahoma" in name or name == 'okc'):
        return ('OKC')
    if ("orlando" in name or name == 'orl'):
        return ('ORL')
    if ("nets" in name or name == 'njn' or name == 'bkn'):
        return ('BKN')
    if ("washington" in name or name == 'was'):
        return ('WAS')
    if ("76" in name or name == 'phi'):
        return ('PHI')
    if ("san antonio" in name or name == 'sas'):
        return ('SAS')
    if ("atlanta" in name or name == 'atl'):
        return ('ATL')
    else:
        return ('---------------------------------------------------------------------------' + name)

def monthToInt(month):
    month = month.lower()
    if ('jan' in month):
        return (1)
    if ('feb' in month):
        return (2)
    if ('mar' in month):
        return (3)
    if ('apr' in month):
        return (4)
    if ('may' in month):
        return (5)
    if ('oct' in month):
        return (10)
    if ('nov' in month):
        return (11)
    if ('dec' in month):
        return (12)
    else:
        return (-1)
