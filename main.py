from helpers.classes import Database
from scraping.historicOdds import historicOdds
from scraping.nbaBoxScores import nbaBoxScores


#A = Database(["Season","Date","Home","Away","Home ML","Away ML","Favorite","Spread","Home Spread Odds","Away Spread Odds","O/U","Over Odds","Under Odds","Home Score","Away Score","url"])
#historicOdds(A, 2008, 2020)

A = Database()
bst = ["traditional","advanced","four-factors","misc","scoring"]
for a in bst:
    nbaBoxScores(A,a)
