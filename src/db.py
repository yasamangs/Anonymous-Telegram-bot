import pymongo


# Initializing the database
client = pymongo.MongoClient("localhost", 27017)
db = client.anonymous_telegram_bot
col = db.users
