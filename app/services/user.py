from app.models import UserBase, UserDisplay
from typing import List
from app.database import MyDatabase
from app.services.hashing import Hash
from fastapi import HTTPException, status


def create_user(payload: UserBase) -> UserDisplay:
    with MyDatabase() as db:
        db.cursor.execute(f"""
            insert into users (username, email, password)
            values(
                '{payload.username}',
                '{payload.email}',
                '{Hash.bcrypt(payload.password)}'
            )
            returning id;
        """)
        db.connection.commit()
        user_id = db.cursor.fetchone()[0]
        obj = get_user_by_userid(user_id)

    return obj


def get_user_by_userid(user_id: int) -> UserDisplay:
    with MyDatabase() as db:
        db.cursor.execute(f"""
            select username, email
              from users
             where id = '{user_id}';
        """)

        data = db.cursor.fetchone()

    return UserDisplay(
        username=data[0],
        email=data[1]
    )


def get_all_user() -> List[UserDisplay]:
    with MyDatabase() as db:
        db.cursor.execute(f"""
            select username, email
              from users
             order by id;
        """)

        obj = []
        for data in db.cursor.fetchall():
            users = UserDisplay(
                username=data[0],
                email=data[1]
            )
            obj.append(users)

    return obj


def get_user_by_username(username: str):
    with MyDatabase() as db:
        db.cursor.execute(f"""
            select username, email
              from users
              where username = {username}
        """)

        user = db.cursor.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username {username} not found")
    return user
