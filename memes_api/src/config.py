import os

# from dotenv import load_dotenv
#
# load_dotenv()

DB_HOST = os.environ.get("DB_HOST", '127.0.0.1')
DB_PORT = os.environ.get("DB_PORT", 5488)
DB_NAME = os.environ.get("DB_NAME", 'postgres')
DB_USER = os.environ.get("DB_USER", 'postgres')
DB_PASS = os.environ.get("DB_PASS", 'mad127')

MINIO_API_HOST = os.environ.get("MINIO_API_HOST", 'minio_api')
MINIO_API_PORT = os.environ.get("MINIO_API_PORT", 8127)

SECRET_AUTH = os.environ.get("SECRET_AUTH")

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
