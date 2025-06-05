import pytest
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_submit_and_get_pereval():
    async with AsyncClient(app=app, base_url='http://test') as client:
        payload = {
            'user': {
                'name': 'API Tester',
                'email': 'apitest@example.com',
                'phone': '987654321'
            },
            'title': 'Test pass',
            'other_titles': 'Test alt',
            'connect': 'No',
            'coords': {
                'latitude': 50.0,
                'longitude': 60.0,
                'height': 1200
            },
            'level': {
                'winter': '1А',
                'spring': None,
                'summer': '2Б',
                'autumn': None
            },
            'images': [
                {'image_url': 'http://example.com/img1.jpg'},
                {'image_url': 'http://example.com/img2.jpg'}
            ]
        }

        # Submit
        post_response = await client.post('/submitData', json=payload)
        assert post_response.status_code == 200
        data = post_response.json()
        pereval_id = data['id']
        assert data['message'] == 'Pereval submitted successfully'

        # Get
        get_response = await client.get(f'/submitData/{pereval_id}')
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data['title'] == 'Test pass'
        assert get_data['coords']['height'] == 1200

        # Update
        payload['title'] = 'Updated title'
        patch_response = await client.patch(f'/submitData/{pereval_id}', json=payload)
        assert patch_response.status_code == 200
        assert patch_response.json()['message'] == 'Updated successfully'
