from httpx import AsyncClient


async def test_jobs(
        ac: AsyncClient
):
    response = await ac.post(
        "/api/jobs",
        json={
            'title': 'Сходить в магазин',
            'description': 'Купить молоко',
            'user_executor': None,
            'user_customer': 32,
            'jobs_access': False,
            'jobs_active': False
        }
    )

    assert response.status_code == 200


async def test_get_jobs(
        ac: AsyncClient
):
    response = await ac.get(
        "/api/jobs"
    )
    assert response.status_code == 200


async def test_get_job_by_id(
        ac: AsyncClient
):
    response = await ac.get(
        "/api/jobs/1"
    )
    assert response.status_code == 200


async def test_my_access_job(
        ac: AsyncClient
):
    response = await ac.get(
        "/api/jobs/my/32/access",

    )
    assert response.status_code == 200


async def test_my_active_job(
        ac: AsyncClient
):
    response = await ac.get(
        "/api/jobs/my/32/active",

    )
    assert response.status_code == 200


async def test_take_job(
        ac: AsyncClient
):
    response = await ac.post(
        "/api/jobs/3/take?my_id=32",
    )
    assert response.status_code == 200


async def test_access_job(
        ac: AsyncClient
):
    response = await ac.post(
        "/api/jobs/3/access?my_id=32",
    )
    assert response.status_code == 200
