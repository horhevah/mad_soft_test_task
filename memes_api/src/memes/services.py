

import requests

from config import MINIO_API_HOST, MINIO_API_PORT
from fastapi import UploadFile, HTTPException


def post_image_to_minio(filename: str, file: UploadFile):
    try:
        res = requests.post(f'http://{MINIO_API_HOST}:{MINIO_API_PORT}/image?filename={filename}',
                            files={'file': (filename, file.file), })
        if res.status_code != 200:
            print(res.text)
            raise HTTPException(status_code=res.status_code, detail=res.text)
    except Exception:
        raise HTTPException(status_code=507, detail='request_error')
