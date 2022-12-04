import re
from os import environ
id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = "Media_search"
API_ID = int(7106507)
API_HASH = "a9b398c45fea9da11440d3ae19bb3c1c"
BOT_TOKEN = "5031402526:AAHXhvq2LLU9jJkr6n6SUdb5Cp27ckXI0Xc"

# Bot settings
CACHE_TIME = int(300)
USE_CAPTION_FILTER = True 
PICS = ["https://graph.org/file/275d838334b8d2090782a.jpg", "https://graph.org/file/1c8e5c7ea88895e227903.jpg", "https://graph.org/file/68a45208c26df7b1be41a.jpg", "https://graph.org/file/c55260e596bf9b3541857.jpg", "https://graph.org/file/be3401ade619bbca9269b.jpg", "https://graph.org/file/2183b2a5224e6ee800571.jpg", "https://graph.org/file/66981394b7a60ed4650fc.jpg", "https://graph.org/file/b1bd6ce54fa5107f800dd.jpg", "https://graph.org/file/7c3f0aeb0d03dd80388e5.jpg", "https://graph.org/file/5a052ab936ce1190a5ead.jpg"]

# Admins, Channels & Users
ADMINS = [1872853375, 1993953092]
CHANNELS = int(-1001771962158)
AUTH_USERS = ADMINS
AUTH_CHANNEL = int(-1001870323556)
AUTH_GROUPS = None

# MongoDB information
DATABASE_URI = "mongodb+srv://tinson:tinson@cluster0.dbhxm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
DATABASE_NAME = "IMDBTINSONSIR"
COLLECTION_NAME = "Telegram_files"

DATABASE_URI_2 = ""
DATABASE_NAME_2 = ""
COLLECTION_NAME_2 = ""

# Others
LOG_CHANNEL = int(-1001679384751)
SUPPORT_CHAT = "TinsonTs"

CUSTOM_FILE_CAPTION = """<code>{file_name}</code>

Join ⚡️
<a href=https://t.me/TinsonTs>[CINEMAPRANTHAN]</a>
<a href=https://t.me/TinsonTs>[OTT MOVIES]</a>
<a href=https://t.me/TinsonTs>[CONFERENCE HALL]</a>"""


P_TTI_SHOW_OFF = True 
SINGLE_BUTTON = True 
SPELL_CHECK_REPLY = False
MELCOW_NEW_USERS = True 
PROTECT_CONTENT = False 
PUBLIC_FILE_STORE = False






