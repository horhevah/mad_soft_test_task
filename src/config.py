import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = '127.0.0.1' # os.environ.get("DB_HOST", '127.0.0.1')
DB_PORT = "5488" #os.environ.get("DB_PORT", 5488)
DB_NAME = 'postgres' #os.environ.get("DB_NAME", 'postgres')
DB_USER = 'postgres' # os.environ.get("DB_USER", 'postgres')
DB_PASS = 'mad127' # os.environ.get("DB_PASS", 'mad127')

print('DB_PASS', DB_PASS, DB_PORT)

DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")

SECRET_AUTH = os.environ.get("SECRET_AUTH")

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
