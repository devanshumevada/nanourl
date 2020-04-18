from config import MONGO_DB_CONNECTION
import pymongo
client = pymongo.MongoClient(MONGO_DB_CONNECTION)
db_links = client['url_shortener']['links']
db_user = client['url_shortener']['user']
db_log = client['url_shortener']['logs']
db_token = client['url_shortener']['tokens']