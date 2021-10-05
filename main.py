from helpers.classes import Database
from scraping.historicOdds import historicOdds


A = Database(["Season","Date","Home","Away","Home ML","Away ML","Favorite","Spread","Home Spread Odds","Away Spread Odds","O/U","Over Odds","Under Odds","Home Score","Away Score","url"])

historicOdds(A, 2008, 2020)
