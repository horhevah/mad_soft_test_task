service for storing memes, consists of:
- public API for managing memes
- postgresql for storing data about memes
- private API for working with s3 storage
- mino s3 storage for storing meme files

use docker compose to run
sudo docker compose up --build

for test memes_api:
- go to directory memes_api
- create virtual environment with requirements from file requirements
- run pytest -s -v