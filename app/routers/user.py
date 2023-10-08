from fastapi import APIRouter, HTTPException, status, Path
from app.models import UserDisplay, UserBase
from app.services import user
from typing import List

router = APIRouter(
    prefix="/user",
    tags=["사용자"]
)


@router.post("/", response_model=UserDisplay)
def create_user(request: UserBase):
    return user.create_user(request)


@router.get("/", response_model=List[UserDisplay])
def get_all_user():
    result = user.get_all_user()
    print(result)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Users not found')
    return result

