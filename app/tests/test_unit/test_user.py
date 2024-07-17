from httpx import AsyncClient


# async def test_registration(
#         ac: AsyncClient
# ):
#     response = await ac.post(
#         "/api/users/registration",
#         json={
#             'name': 'Slava',
#             'number': '79994998531',
#             'telegram_id': 'sls212',
#             'password': '12345678',
#             'address': 'address',
#             'housing_complex_id': 1
#         }
#     )
#
#     assert response.status_code == 200


async def test_login(ac: AsyncClient):
    response = await ac.post(
        '/api/users/login',
        json={
            'number': '79994998531',
            'password': '12345678'
        }
    )
    assert response.status_code == 200


# async def test_update(ac: AsyncClient):
#     response = await ac.patch(
#         '/api/users/me/update?id=30',
#         json={
#             'number': '79994998534',
#             'name': 'Slava',
#             'telegram_id': 'sl2',
#             'password': 'passw',
#             'address': 'asdasdasd',
#             'housing_complex_id': 1,
#         }
#     )
#     assert response.status_code == 200
#
#
# async def test_delete(ac: AsyncClient):
#     response = await ac.delete(
#         '/api/users/me/delete?id=31'
#     )
#     assert response.status_code == 200