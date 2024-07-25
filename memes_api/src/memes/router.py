import datetime
from typing import Any, Annotated

import fastapi
import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from minio import Minio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.users import current_active_user
from memes.models import Memes
from database import get_async_session
from memes.schemas import MemesOut, MemesIn, MemesPut

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter(
    prefix="/api/v1",
    tags=["/api/v1"]
)


@router.get('/memes')
async def get_memes(session: AsyncSession = Depends(get_async_session)) -> Page[MemesOut]:
    return await paginate(session, select(Memes))


@router.get('/memes/{mem_id}')
async def get_mem_by_id(mem_id: int, session: AsyncSession = Depends(get_async_session)) -> MemesOut:
    try:
        mem = await session.get_one(Memes, mem_id)
        return MemesOut.model_validate(mem, from_attributes=True)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Mem not found")


@router.post('/memes', status_code=201)
async def add_mem(
        title: Annotated[str, Form()],
        category: Annotated[str, Form()],
        file: UploadFile,
        # mem_data: MemesIn,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)) -> int:
    # new_mem = Memes(created_at=datetime.datetime.now(), **mem_data.model_dump())
    print(type(file), file)
    client = Minio("192.168.17.105:9009",
                   secure=False,
                   access_key='memes_user',
                   secret_key='memes_pass'
                   )

    source_file = file.file
    bucket_name = "memes-bucket"
    destination_file = "screenshot.py"

    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the file, renaming it in the process
    client.put_object(
        bucket_name, destination_file, file.file, file.size
    )
    print(
        source_file, "successfully uploaded as object",
        destination_file, "to bucket", bucket_name,
    )


    # new_mem = Memes(created_at=datetime.datetime.now(),
    #                 title=title,
    #                 category=category,
    #                 )
    # session.add(new_mem)
    # await session.commit()
    # return new_mem.id
    return 1


@router.put('/memes/{mem_id}')
async def change_mem_by_id(mem_id: int, mem_data: MemesPut, user: User = Depends(current_active_user), session: AsyncSession = Depends(get_async_session)) -> MemesOut:
    try:
        mem = await session.get_one(Memes, mem_id)
        for key, value in mem_data:
            setattr(mem, key, value) if value else None
        session.add(mem)
        await session.commit()
        return MemesOut.model_validate(mem, from_attributes=True)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Mem not found")


@router.delete('/memes/{mem_id}')
async def delete_mem_by_id(mem_id: int, user: User = Depends(current_active_user), session: AsyncSession = Depends(get_async_session)) -> MemesOut:
    try:
        mem = await session.get_one(Memes, mem_id)
        await session.delete(mem)
        await session.commit()
        return MemesOut.model_validate(mem, from_attributes=True)

    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Mem not found")
