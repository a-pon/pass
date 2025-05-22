from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class CoordsSchema(BaseModel):
    latitude: float
    longitude: float
    height: int


class LevelSchema(BaseModel):
    winter: Optional[str] = None
    spring: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None


class ImageSchema(BaseModel):
    image_url: str


class PerevalCreateSchema(BaseModel):
    user: UserSchema
    beauty_title: Optional[str] = None
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    coords: CoordsSchema
    level: Optional[LevelSchema] = None
    images: Optional[List[ImageSchema]] = []

    # class Config:
    #     from_attributes = True


class PerevalResponseSchema(BaseModel):
    status: int = Field(..., example=200)
    message: str
    id: Optional[int] = None
