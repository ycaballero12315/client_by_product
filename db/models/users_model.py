from pydantic import BaseModel

class User(BaseModel):
    id: int | None = None
    username: str
    full_name: str | None = None
    email: str | None = None
    disable: bool = False

class DBUser(User):
    password: str

list_users = [User(id= 1, username="ycaballero", full_name="Yoeny Caballero Gonzalez", email= 'ycaballero12315@gmail.com', disable= False),
              User(id=2, username="yoedev", full_name="ghg Caballero Gonzalez", email= 'ycaballero123515@gmail.com', disable=False)]

