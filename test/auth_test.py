import pytest


@pytest.mark.asyncio
async def test_register_and_login(ac):
    reg_response = await ac.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com"
    })
    assert reg_response.status_code == 200
    assert reg_response.json()["username"] == "testuser"

    login_response = await ac.post("/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    
    return login_response.json()["access_token"]

@pytest.mark.asyncio
async def test_protected_weather(ac):
    login_data = {"username": "testuser", "password": "testpassword"}
    login_res = await ac.post("/auth/login", data=login_data)
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = await ac.get("/weather?city=Bishkek", headers=headers)
    
    assert response.status_code == 200
    assert "data" in response.json()