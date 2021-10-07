from classes import Database
from scrapers import historicOdds
from scrapers import nbaBoxScores


#A = Database(["Season","Date","Home","Away","Home ML","Away ML","Favorite","Spread","Home Spread Odds","Away Spread Odds","O/U","Over Odds","Under Odds","Home Score","Away Score","url"])
#historicOdds(A, 2008, 2020)

bst = ["misc","scoring"]
for a in bst:
    A = Database()
    nbaBoxScores(A,a)
