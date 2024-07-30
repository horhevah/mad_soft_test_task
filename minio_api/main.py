import uuid

import fastapi.responses
from fastapi.openapi.models import Response
from minio import Minio
from minio.error import S3Error

from fastapi import HTTPException, FastAPI, UploadFile
# from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse

from config import BUCKET_NAME

app = FastAPI(
    title="Memes App"
)

client = Minio("192.168.17.105:9009",
                   secure=False,
                   access_key='memes_user',
                   secret_key='memes_pass'
        # access_key="Q3AM3UQ867SPQQA43P2F",
        # secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
    )

print('BBBBBBBBBBBBB', BUCKET_NAME)

found = client.bucket_exists(BUCKET_NAME)
if not found:
    client.make_bucket(BUCKET_NAME)
    print("Created bucket", BUCKET_NAME)
else:
    print("Bucket", BUCKET_NAME, "already exists")


@app.get('/image')
def get_file(filename: str):
    try:
        image_file = client.get_object(BUCKET_NAME, filename)
        return StreamingResponse(content=image_file)
    except S3Error as exc:
        return HTTPException(status_code=500, detail=f'S3 error, {exc}')


@app.post('/image')
def post_file(file: UploadFile):
    try:
        client.put_object(
            BUCKET_NAME, file.filename, file.file, file.size
        )
    except S3Error as exc:
        return HTTPException(status_code=500, detail=f'S3 error, {exc}')

# def main():
#     # Create a client with the MinIO server playground, its access key
#     # and secret key.
#
#
#     # The file to upload, change this path if needed
#     source_file = "main.py"
#
#     # The destination bucket and filename on the MinIO server
#     bucket_name = "memes-bucket"
#     destination_file = "main.py"
#
#     # Make the bucket if it doesn't exist.
#     found = client.bucket_exists(bucket_name)
#     if not found:
#         client.make_bucket(bucket_name)
#         print("Created bucket", bucket_name)
#     else:
#         print("Bucket", bucket_name, "already exists")
#
#     # Upload the file, renaming it in the process
#     client.fput_object(
#         bucket_name, destination_file, source_file,
#     )
#     print(
#         source_file, "successfully uploaded as object",
#         destination_file, "to bucket", bucket_name,
#     )
#

if __name__ == "__main__":
    pass
