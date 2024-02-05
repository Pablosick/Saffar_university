import re
import uuid
from pydantic import BaseModel, validator, EmailStr
from fastapi import HTTPException


# Блок с API моделями (Обработка запросов, который пришли от пользователя)

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    """Промежуточный класс для настроек всех остальных моделей"""
    class Config:
        orm_mode = True  # Конвертировать все объекты (dict и другие) в json


class ShowUser(TunedModel):
    """Модель ответа для пользователя"""
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    """Модель входящего запроса на создание пользователя"""
    name: str
    surname: str
    email: EmailStr

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Имя должно содержать только буквы")
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Фамилия должно содержать только буквы")
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


# class UpdatedUserResponse(BaseModel):
#     deleted_user_id: uuid.UUID
