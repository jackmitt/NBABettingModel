from classes import Database
from scrapers import historicOdds
from scrapers import nbaBoxScores
import data_manipulation as dm

dm.mergeMatches("./csv_data/raw/advanced_stats.csv", "./csv_data/mid_manipulation/merged_matches.csv")
