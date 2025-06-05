from typing import List

from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from src.db import db_dependency
from src.models import PerevalAdded, PerevalImage, Status, User
from src.schemas import PerevalCreateSchema, PerevalDetailSchema, PerevalResponseSchema
from src.services import (add_images_to_pereval,
                          create_coords,
                          create_pereval,
                          get_or_create_user)

app = FastAPI(
    title='Mountain-pass-REST_API-App',
    description='An app for creating a database of mountain passes.',
    version='1.0.0'
)


@app.post('/submitData',
          response_model=PerevalResponseSchema,
          summary='Add new mountain pass')
async def submit_data(data: PerevalCreateSchema, session: db_dependency):
    try:
        user_data = data.user
        coords_data = data.coords
        level_data = data.level or {}
        user = await get_or_create_user(session, user_data.name, user_data.email, user_data.phone)
        coords = await create_coords(session, coords_data.latitude, coords_data.longitude, coords_data.height)
        pereval = await create_pereval(
            session=session,
            user=user,
            coords=coords,
            title=data.title,
            other_titles=data.other_titles,
            connect=data.connect,
            level_winter=level_data.winter,
            level_spring=level_data.spring,
            level_summer=level_data.summer,
            level_autumn=level_data.autumn
        )
        image_urls = [img.image_url for img in data.images]
        await add_images_to_pereval(session, pereval, image_urls)
        await session.commit()
        return PerevalResponseSchema(
            status=200,
            message='Pereval submitted successfully',
            id=pereval.id
        )
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail='Database error')
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{str(e)}')


@app.get('/submitData/{pereval_id}',
         response_model=PerevalDetailSchema,
         summary='Get mountain pass by id')
async def get_pereval_by_id(pereval_id: int, session: db_dependency):
    query = select(PerevalAdded).where(PerevalAdded.id == pereval_id).options(
        joinedload(PerevalAdded.user),
        joinedload(PerevalAdded.coords),
        joinedload(PerevalAdded.images)
    )
    result = await session.execute(query)
    pereval = result.scalar_one_or_none()
    if not pereval:
        raise HTTPException(status_code=404, detail='Pereval not found')
    return pereval


@app.patch('/submitData/{pereval_id}',
           summary='Update mountain pass info')
async def update_pereval(pereval_id: int, data: PerevalCreateSchema, session: db_dependency):
    try:
        query = select(PerevalAdded).where(PerevalAdded.id == pereval_id).options(
            joinedload(PerevalAdded.user),
            joinedload(PerevalAdded.coords),
            joinedload(PerevalAdded.images)
        )
        result = await session.execute(query)
        pereval = result.scalar_one_or_none()
        if not pereval:
            return {'state': 0, 'message': 'Pereval not found'}
        if pereval.status != Status.new:
            return {'state': 0, 'message': 'Update failed: Status is not "new"'}

        pereval.title = data.title
        pereval.other_titles = data.other_titles
        pereval.connect = data.connect
        pereval.level_winter = data.level.winter if data.level else None
        pereval.level_spring = data.level.spring if data.level else None
        pereval.level_summer = data.level.summer if data.level else None
        pereval.level_autumn = data.level.autumn if data.level else None
        pereval.coords.latitude = data.coords.latitude
        pereval.coords.longitude = data.coords.longitude
        pereval.coords.height = data.coords.height
        await session.execute(
            PerevalImage.__table__.delete().where(PerevalImage.pereval_id == pereval.id)
        )
        for img in data.images or []:
            session.add(PerevalImage(pereval_id=pereval.id, image_url=img.image_url))
        await session.commit()
        return {'state': 1, 'message': 'Updated successfully'}
    except Exception as e:
        await session.rollback()
        return {'state': 0, 'message': f'Update failed: {str(e)}'}


@app.get('/submitData',
         response_model=List[PerevalDetailSchema],
         summary='Get mountain passes by user email')
async def get_perevals_by_user(email: str, session: db_dependency):
    query = select(PerevalAdded).join(PerevalAdded.user).where(User.email == email).options(
        joinedload(PerevalAdded.user),
        joinedload(PerevalAdded.coords),
        joinedload(PerevalAdded.images)
    )
    result = await session.execute(query)
    perevals = result.scalars().all()
    return perevals
