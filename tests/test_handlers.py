import json


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