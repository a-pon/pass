from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.db import db_dependency
from src.schemas import PerevalCreateSchema, PerevalResponseSchema
from src.services import (add_images_to_pereval,
                          create_coords,
                          create_pereval,
                          get_or_create_user)

app = FastAPI()


@app.post('/submitData', response_model=PerevalResponseSchema)
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
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=500, detail='Unexpected server error')
