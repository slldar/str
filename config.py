from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID","15575514"))
API_HASH = getenv("API_HASH","0152346497bdf77eb9698994d0205a3a")

BOT_TOKEN = getenv("BOT_TOKEN")
OWNER_ID = int(getenv("OWNER_ID"))

MONGO_DB_URI = ("MONGO_DB_URI","mongodb+srv://SlliDaaR:SlliDaaR@cluster0.rwmk3kf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
MUST_JOIN = getenv("MUST_JOIN", None)
