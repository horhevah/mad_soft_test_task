import datetime
from typing import Any

import fastapi
import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
        return MemesOut(**mem.__dict__)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Mem not found")


@router.post('/memes')
async def add_mem(mem_data: MemesIn, session: AsyncSession = Depends(get_async_session)) -> Any:
    session.add(Memes(created_at=datetime.datetime.now(), **mem_data.model_dump()))
    await session.commit()


@router.put('/memes/{mem_id}')
async def change_mem_by_id(mem_id: int, mem_data: MemesPut, session: AsyncSession = Depends(get_async_session)) -> MemesOut:
    try:
        mem = await session.get_one(Memes, mem_id)
        for key, value in mem_data:
            setattr(mem, key, value) if value else None
        session.add(mem)
        await session.commit()
        return MemesOut(**mem.__dict__)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Mem not found")


@router.delete('/memes/{mem_id}')
async def delete_mem_by_id(mem_id: int, session: AsyncSession = Depends(get_async_session)) -> MemesOut:
    try:
        mem = await session.get_one(Memes, mem_id)
        await session.delete(mem)
        await session.commit()
        return MemesOut(**mem.__dict__)

    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Mem not found")
