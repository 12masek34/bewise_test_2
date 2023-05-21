

from pydantic import (
    BaseModel,
    PositiveInt,
)


class UserSchema(BaseModel):

    name: str


class UserUploadFileSchema(BaseModel):

    id: PositiveInt
    token: str

    class Config:
        orm_mode = True


class UserResponseSchema(UserUploadFileSchema, UserSchema):
    """All filds user."""
