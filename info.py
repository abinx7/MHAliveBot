import re
from os import environ

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

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

# Others
LOG_CHANNEL = int(-1001679384751)
SUPPORT_CHAT = "TinsonTs"

CUSTOM_FILE_CAPTION = """<code>{file_name}</code>

Join ⚡️
<a href=https://t.me/TinsonTs>[CINEMAPRANTHAN]</a>
<a href=https://t.me/TinsonTs>[OTT MOVIES]</a>
<a href=https://t.me/TinsonTs>[CONFERENCE HALL]</a>"""

BATCH_FILE_CAPTION = None
IMDB_TEMPLATE = """<b>🏷 Title</b>: <a href={url}>{title}</a>
🎭 Genres: {genres}
📆 Year: <a href={url}/releaseinfo>{year}</a>
🌟 Rating: <a href={url}/ratings>{rating}</a> / 10 


Requested by : {message.from_user.mention}"""


P_TTI_SHOW_OFF = is_enabled(("True"), True)
IMDB = is_enabled(("False"), False)
SINGLE_BUTTON = is_enabled(("True"), True)
LONG_IMDB_DESCRIPTION = is_enabled(("False"), False)
SPELL_CHECK_REPLY = is_enabled(("False"), False)
MAX_LIST_ELM = None
INDEX_REQ_CHANNEL = LOG_CHANNEL
FILE_STORE_CHANNEL = None
MELCOW_NEW_USERS = is_enabled(("True"), True)
PROTECT_CONTENT = is_enabled(("False"), False)
PUBLIC_FILE_STORE = is_enabled(("False"), False)

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"
