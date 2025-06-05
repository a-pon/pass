import pytest

from src.models import Status
from src.services import create_coords, create_pereval, get_or_create_user


@pytest.mark.asyncio
async def test_create_user(db_session):
    user = await get_or_create_user(db_session, 'Test User', 'test@example.com', '123456789')
    assert user.id is not None
    assert user.email == 'test@example.com'


@pytest.mark.asyncio
async def test_create_coords(db_session):
    coords = await create_coords(db_session, 55.5, 37.5, 500)
    assert coords.id is not None
    assert coords.height == 500


@pytest.mark.asyncio
async def test_create_pereval(db_session):
    user = await get_or_create_user(db_session, 'Test User', 'user@example.com', '000')
    coords = await create_coords(db_session, 10.0, 20.0, 1500)
    pereval = await create_pereval(
        db_session, user, coords,
        title='Test Pass',
        other_titles='Test',
        connect='No',
        level_winter='1А',
        level_summer='2А'
    )
    assert pereval.id is not None
    assert pereval.status == Status.new
