from fastapi import HTTPException, Depends, APIRouter, status
from db.models.users_model import User, DBUser
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from routers.simple_autentication import get_user, get_user_db
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone


router = APIRouter(prefix="/loginJWT", tags=["loginJWT"], 
                   responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

aouth2_scheme = OAuth2PasswordBearer(tokenUrl="/loginJWT/token")

ALGORITHM = "HS256"
SECRET_KEY = "e3d8518c0a7e8d1353b90229a4" \
            "133422a0351dc6139d6aea66a2c8462a590d1e73e030e3eb" \
            "88074426dc787cc49023464e5bf9a35add1a9013cd744fcc0fa8d9" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_db = {
    'yoeny': {
        'id': 1,
        'username': 'yoeny',
        'full_name': 'Yoeny Caballero',
        'email': 'ycaballero12315@gmail.com',
        'password': '$2a$12$.UCo/hMCc7gpvZweyl1r8eookfxhkEjHhzg78Tpfy7kKOIsOcVUOe',
        'disable': False
    },
    'yoedev': {
        'id': 2,
        'username': 'yoedev',
        'full_name': 'Yoeny Caballero Gonzalez',    
        'email': 'yoenycaballerogonzalez@gmail.com',
        'password': '$2a$12$27LPyJyyzdWHIh71DmJ4a.JfYAOuh.xP1sYvQJY/eFEMgcIb8qozi',
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

def auth_user(token:str = Depends(aouth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid authentication credentials", 
                headers={"WWW-Authenticate": "Bearer"}
            )
        return get_user(username)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication credentials", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    
async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User is disabled"
        )
    return user

@router.post("/", summary="Login and get token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Buscar usuario en la "base de datos"
    user_entry = user_db.get(form_data.username)
    if not user_entry or not crypt.verify(form_data.password, user_entry["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    # Convertir a modelo
    user = get_user_db(form_data.username)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": user.username, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    # Devolver el token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/users/me", response_model=User, summary="Get current logged user")
async def read_users_me(user: User = Depends(current_user)):
    try:
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))