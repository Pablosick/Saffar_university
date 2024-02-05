import json
from uuid import uuid4


async def test_create_user(client, get_user_from_database):
    """Тест на создание пользователя"""
    user_data = {
        "name": "Pavel",
        "surname": "Bochkarev",
        "email": "bo04@gmail.com"
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_database = await get_user_from_database(data_from_resp["user_id"])  # Что вернется по user_id из ответа
    assert len(users_from_database) == 1
    users_from_database = dict(users_from_database[0])
    assert users_from_database["name"] == user_data["name"]
    assert users_from_database["surname"] == user_data["surname"]
    assert users_from_database["email"] == user_data["email"]
    assert users_from_database["is_active"] is True
    assert str(users_from_database["user_id"]) == data_from_resp["user_id"]


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Pavel",
        "surname": "Bochkarev2",
        "email": "bo018@gmail.com",
        "is_active": True
    }
    await create_user_in_database(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_database = await get_user_from_database(user_data["user_id"])
    user_from_database = dict(users_from_database[0])
    assert user_from_database["name"] == user_data["name"]
    assert user_from_database["surname"] == user_data["surname"]
    assert user_from_database["email"] == user_data["email"]
    assert user_from_database["is_active"] is False
    assert user_from_database["user_id"] == user_data["user_id"]
