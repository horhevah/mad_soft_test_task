import os

BUCKET_NAME = os.environ.get("BUCKET_NAME", 'memes-bucket')
MINIO_HOST = os.environ.get("MINIO_HOST", 'minio')
MINIO_PORT = os.environ.get("MINIO_PORT", 8127)
MINIO_USER = os.environ.get("MINIO_USER", 'memes_user')
MINIO_PASS = os.environ.get("MINIO_PASS", 'memes_pass')
