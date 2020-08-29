import os

MONGO_DB_CONNECTION = os.environ['MONGO_DB_CONNECTION']
SECRET_KEY = os.environ['SECRET_KEY']
SEND_GRID_API_LINK = os.environ['SEND_GRID_API_LINK']
SEND_GRID_API_KEY  = os.environ['SEND_GRID_API_KEY']
SEND_GRID_API_HEADERS={'Content-Type':'application/json', 'Authorization':'Bearer '+SEND_GRID_API_KEY}
MEMC_SERVERS = os.environ['MEMC_SERVERS']
MEMC_USERNAME = os.environ['MEMC_USERNAME']
MEMC_PASSWORD = os.environ['MEMC_PASSWORD']