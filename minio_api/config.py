import os

BUCKET_NAME = os.environ.get("BUCKET_NAME", 'memes-bucket')
MINIO_HOST = os.environ.get("MINIO_HOST", 'minio')
MINIO_PORT = os.environ.get("MINIO_PORT", 8127)
