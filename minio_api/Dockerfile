FROM python:3.10

#
WORKDIR /minio_api

#
COPY requirements .

#
RUN pip install --no-cache-dir --upgrade -r requirements

#
COPY . /minio_api

#
CMD uvicorn main:app --host 0.0.0.0 --port 8000 --reload