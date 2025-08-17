from fastapi import APIRouter, HTTPException, status
from db.models.user_model_for_db import User
from db.client import db
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter( prefix="/userdb", tags=["userdb"], responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

@router.get("/id/{id}")
async def read_users(id: str):
    return search_user_by("_id", id)

@router.get("/username/{username}")
async def read_user_by_username(username: str):
    if not username.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Username is required")
    return search_user_by("username", username)

@router.get("/email/{email}")
async def read_user_by_email(email: str):
    if not email.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email is required")
    return search_user_by("email", email)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    if type(search_user_by("username", user.username)) == User:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    if type(search_user_by("email", user.email)) == User:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already exists")
      
    user_dict = user.model_dump()
    user_dict.pop("id", None) 
    inserted =  db.users.insert_one(user_dict)
    
    new_user = user_schema(db.users.find_one({"_id": inserted.inserted_id}))
  
    return User(**new_user)

@router.get("/", response_model=list[User])
async def read_all_users(skip: int = 0, limit: int = 10) -> list[User]:
    user_cursor = db.users.find().skip(skip).limit(limit) #Esto es como una paginacion en la base de datos
    if  not user_cursor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No users found")

    return users_schema(user_cursor) 

def search_user_by(field: str, value: str):
    if field not in FIELD_VALIDATORS:
        raise HTTPException(status_code=400, detail=f"Invalid field: {field}")
    
    try:
        validated_value = FIELD_VALIDATORS[field](value)
        validated_value = str(validated_value)  

        if field in ["username", "email"]:
            query = {field: {"$regex": f"^{validated_value}$", "$options": "i"}}
        else:
            query = {field: validated_value}
        user = db.users.find_one(query)
        return User(**user_schema(user))
    except:
        return None

def validate_id(id_str: str) -> ObjectId:
    if not ObjectId.is_valid(id_str):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    return ObjectId(id_str)

def identity(value: str) -> str:
    return value

FIELD_VALIDATORS = {
    "_id": validate_id,
    "username": identity,
    "email": identity
}
    
@router.put("/{id}")
async def update_user(id: str, username:str) -> User:
    try:
        validate_value = validate_id(id)
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

    user = db.users.find_one({"_id": validate_value})
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    update_fields = {}
    if username:
        update_fields["username"] = username

    if update_fields:
        result = db.users.update_one(
            {"_id": validate_value},
            {"$set": update_fields}
        )
        if result.modified_count != 1:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No changes made to the user")

    updated_user = db.users.find_one({"_id": validate_value})
    return User(**user_schema(updated_user))
        

@router.put("/", response_model=dict)
async def update_user(user: User) -> dict:
    try:
        validate_value = validate_id(user.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    _by(user.id)

    user_dict = user.model_dump()
    user_dict.pop("id", None) 

    updated_user = db.users.update_one(
        {"_id": validate_value},
        {"$set": user_dict}
    )
    
    if updated_user.modified_count == 1:
        return {"message": "User updated successfully"}
    else:
        return {"message": "No changes made to the user"}
    

@router.delete("/{id}", response_model=dict)
async def delete_user(id: str) ->dict:

    try:
        validate_value = validate_id(id)
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

    user = db.users.find_one({"_id": validate_value})
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    result = db.users.delete_one({"_id": validate_value})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Failed to delete user")
    
@router.delete("/{username}", response_model=dict)
async def delete_user_for_index(username:str):
    if not username.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Username is required")
    else:
        user = db.users.find_one({"username": username})
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    result = db.users.delete_one({"username": username})
    if result.deleted_count == 1:
        return {f"message": f"User {username} deleted successfully"}
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to server delete user")