from typing import List
from fastapi import APIRouter, HTTPException, status, Path  # new
# from psycopg2.errors import DatetimeFieldOverflow, OperationalError
#  internals
from app.services.news import (insert_t_news, select_t_news, select_t_news_by_id, update_t_news_by_id, delete_t_news_by_id)  # new
from app.models import NewsDB, NewsSchema

router = APIRouter(
    prefix='/news',
    tags=['news']
)


@router.post('/', response_model=NewsDB, status_code=status.HTTP_201_CREATED)
async def create_news(payload: NewsSchema):
    try:
        res = insert_t_news(payload)
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )
    # except Error as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"{e}"
    #     )


@router.get('/', response_model=List[NewsDB], status_code=status.HTTP_200_OK)
async def read_news():
    try:
        return select_t_news()
    # except OperationalError:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="""Check if the database exists, connection is successful or tables exist. To create tables use '/initdb' endpoint"""
    #     )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"""Error {e}"""
        )


@router.get('/{id}/', response_model=NewsDB, status_code=status.HTTP_200_OK)
async def read_news_by_id(id: int = Path(..., gt=0)):
    result = select_t_news_by_id(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='News not found')
    return result


@router.put('/{id}/', response_model=NewsDB, status_code=status.HTTP_200_OK)
async def update_news_by_id(payload: NewsSchema, id: int = Path(..., gt=0)):
    result = update_t_news_by_id(id, payload)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='News not found')
    return result


@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_news_by_id(id: int = Path(..., gt=0)):
    result = delete_t_news_by_id(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='News not found')
    return result
