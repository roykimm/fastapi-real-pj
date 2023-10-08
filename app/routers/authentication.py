from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.services.authentication import get_user, create_access_token
from app.services.hashing import Hash

router = APIRouter(
    tags=["authentication"]
)


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = get_user(request.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")

    if not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="incorrect password")

    access_token = create_access_token(data={"username": user["username"]})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user["id"],
        "username": user["username"]
    }
