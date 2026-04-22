from pydantic import BaseModel, ConfigDict

# TODO: Validate that email address ends with @company.com
# Is this required for all users?
# TODO: Add phone_number to User. What validation rules should apply?

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

