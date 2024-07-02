import datetime
from typing import Any

import fastapi
import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.users import current_active_user
from src.memes.models import Memes
from src.database import get_async_session
from src.memes.schemas import MemesOut, MemesIn, MemesPut

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
async def add_mem(mem_data: MemesIn, user: User = Depends(current_active_user),  session: AsyncSession = Depends(get_async_session)) -> int:
    new_mem = Memes(created_at=datetime.datetime.now(), **mem_data.model_dump())
    session.add(new_mem)
    await session.commit()
    return new_mem.id


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
