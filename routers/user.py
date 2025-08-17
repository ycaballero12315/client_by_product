from fastapi import APIRouter, HTTPException
from db.models.users_model import User, list_users

router = APIRouter( prefix="/user", tags=["user"], responses={404: {"description": "Not found"}})

@router.get("/")
async def read_root():
    return {"Hello": "World"}   

@router.get("/users/{id}")
async def read_users(id: int):
    return search_user(id) 

@router.post("/users/", status_code=201)
async def create_user(user: User):
    if search_user(user.id):
        return {"error": "User with this ID already exists"}    
    list_users.append(user)
    return user

@router.get("/users/")
async def read_all_users():
    return list_users   

def search_user(id: int):
    users = filter(lambda user: user.id == id, list_users)
    try:
        return list(users)[0]
    except:
        return None
    
@router.put("/users/{id}")
async def update_user(id: int, password: str | None = None):
    existing_user = search_user(id)
    if not existing_user:
        return {"error": "User not found"}
    
    existing_user.password = password if password else existing_user.password
    
    
    return existing_user

@router.put("/users")
async def update_user(user: User) -> str:
    existing_user = search_user(user.id)
    if not existing_user:
        return {"error": "User not found"}
    else:
        for index, user in enumerate(list_users):
            if user.id == existing_user.id:
                list_users[index] = user
                return {"message": "User updated successfully"}
            
    return {"error": "User not found"}

@router.delete("/users/{id}")
async def delete_user(id: int):
    existing_user = search_user(id)
    if not existing_user:
        return {"error": "User not found"}
    else:
        del_user = existing_user
        list_users.remove(existing_user)
        return del_user

@router.delete("/users/by_username/{username}")
async def delete_user_for_index(username:str):
    if not list_users:
        raise HTTPException(status_code=404, detail="No users found")
    
    else:
        for index, user in enumerate(list_users):
            if user.username == username:
                del_user = user
                del list_users[index]
                return del_user
            
    raise HTTPException(status_code=404, detail="User not found")