from pydantic import BaseModel
from fastapi import APIRouter, status


router = APIRouter(prefix='/query', tags=['analitical'], responses={status.HTTP_400_BAD_REQUEST: {"description": "Not found"}})

class Query(BaseModel):
    select: str
    where: str | None = None
    orderby: str | None = None
    sortby: str | None = None

@router.post('/analitical')
async def respon(q: Query):
    return q

