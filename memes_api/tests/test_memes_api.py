import os.path
from pathlib import Path

import pytest

from memes.models import Memes
from memes.router import add_mem
from .conftest import client, async_session_maker_test

from sqlalchemy import select, func


BASE_DIR = Path(__file__).resolve().parent.parent

print('AAAAAAAAAAAAAAAA', BASE_DIR)


class TestAPI:
    def test_get_memes(self):
        response = client.get("/api/v1/memes")
        assert response.status_code == 200

    @pytest.mark.usefixtures('send_post')
    @pytest.mark.usefixtures('minio_mock')
    async def test_add_memes_status_code(self, send_post):
        assert send_post.status_code == 201

    @pytest.mark.usefixtures('send_post')
    @pytest.mark.usefixtures('minio_mock')
    async def test_add_memes_count(self, send_post):
        async with async_session_maker_test() as session:
            res = await session.execute(select(func.count("*")).select_from(Memes))
            assert res.scalar() == 1

    @pytest.mark.usefixtures('send_post')
    @pytest.mark.usefixtures('minio_mock')
    async def test_add_memes_attributes(self, send_post):
        async with async_session_maker_test() as session:
            res = await session.execute(select(Memes))
            mem = res.scalar()
            assert mem.title == 'title'
            assert mem.category == 'category'
            assert mem.image == f"/api/v1/images?filename=1_test_img.jpg"


