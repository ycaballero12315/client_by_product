from fastapi import HTTPException, Depends, APIRouter, status
from db.models.users_model import User, DBUser
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 

router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

# Aquí debes poner la URL correcta de obtención del token
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

user_db = {
    'yoeny': {
        'id': 1,
        'username': 'yoeny',
        'full_name': 'Yoeny Caballero',
        'email': 'ycaballero12315@gmail.com',
        'password': '12345678',
        'disable': False
    },
    'yoedev': {
        'id': 2,
        'username': 'yoedev',
        'full_name': 'Yoeny Caballero Gonzalez',    
        'email': 'yoenycaballerogonzalez@gmail.com',
        'password': '123456789',
        'disable': True
    }
}

def get_user_db(username: str):
    if username in user_db:
        return DBUser(**user_db[username])
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
def get_user(username: str):
    if username in user_db:
        return User(**user_db[username])
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
async def current_user(token: str = Depends(oath2_scheme)):
    user = get_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized access", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User is disabled"
        )
    return user

# Ruta explícita con "/"
@router.post("/token", summary="Login and get token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Buscar usuario en la "base de datos"
    user_entry = user_db.get(form_data.username)
    if not user_entry or user_entry["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    # Convertir a modelo
    user = get_user_db(form_data.username)

    # En un caso real deberías devolver un JWT o token similar
    return {
        "access_token": user.username,
        "token_type": "bearer"
    }

@router.get("/users/me", response_model=User, summary="Get current logged user")
async def read_users_me(user: User = Depends(current_user)):
    return user
