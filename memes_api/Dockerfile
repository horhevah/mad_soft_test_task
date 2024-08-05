FROM python:3.10

#
WORKDIR /memes_api

#
COPY requirements .

#
RUN pip install --no-cache-dir --upgrade -r requirements

#
COPY . /memes_api

#
CMD alembic upgrade head && cd src && uvicorn main:app --host 0.0.0.0 --port 8000 --reload