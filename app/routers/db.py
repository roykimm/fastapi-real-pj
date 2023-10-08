from typing import List
from fastapi import APIRouter, HTTPException, status, Path  # new
# from psycopg2.errors import DatetimeFieldOverflow, OperationalError
#  internals
from app.db_script import create_table
from app.models import NewsDB, NewsSchema

router = APIRouter(
    prefix='/db',
    tags=['db 생성']
)


@router.get('/', status_code=status.HTTP_201_CREATED)
async def execute_db_script():
    try:
        res = create_table()
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )