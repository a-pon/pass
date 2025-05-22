from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Coords, PerevalAdded, PerevalImage, Status, User


async def get_or_create_user(session: AsyncSession, name: str, email: str, phone: str) -> User:
    user_query = select(User).where(User.email == email)
    result = await session.execute(user_query)
    user = result.scalar_one_or_none()
    if user:
        return user

    user = User(name=name, email=email, phone=phone)
    session.add(user)
    await session.flush()
    return user


async def create_coords(session: AsyncSession, latitude: float, longitude: float, height: int) -> Coords:
    coords = Coords(latitude=latitude, longitude=longitude, height=height)
    session.add(coords)
    await session.flush()
    return coords


async def create_pereval(
        session: AsyncSession,
        user: User,
        coords: Coords,
        title: str,
        other_titles: str,
        connect: str,
        level_winter: str = None,
        level_spring: str = None,
        level_summer: str = None,
        level_autumn: str = None
) -> PerevalAdded:
    pereval = PerevalAdded(
        user_id=user.id,
        coord_id=coords.id,
        title=title,
        other_titles=other_titles,
        connect=connect,
        status=Status.new,
        level_winter=level_winter,
        level_spring=level_spring,
        level_summer=level_summer,
        level_autumn=level_autumn
    )
    session.add(pereval)
    await session.flush()
    return pereval


async def add_images_to_pereval(
        session: AsyncSession,
        pereval: PerevalAdded,
        image_urls: List[str]
) -> None:
    for url in image_urls:
        image = PerevalImage(pereval_id=pereval.id, image_url=url)
        session.add(image)
