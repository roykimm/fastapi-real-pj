from ..database import MyDatabase
from ..models import NewsSchema, NewsDB
from typing import List

t_news = "t_news"


def create_tables():
    with MyDatabase() as db:
        db.cursor.execute(f"""CREATE TABLE {t_news} (
            id integer(10) PRIMARY KEY AUTO_INCREMENT,
            published_date timestamp DEFAULT NOW(),
            created_date timestamp DEFAULT NOW(),
            created_by varchar(140),
            context TEXT NOT NULL
            );
        """)
        db.connection.commit()
        print("Tables are created successfully...")


def drop_tables():
    with MyDatabase() as db:
        db.cursor.execute(f"DROP TABLE IF EXISTS {t_news} CASCADE;")
        db.connection.commit()
        print("Tables are dropped...")


def select_t_news() -> List[NewsDB]:
    with MyDatabase() as db:
        db.cursor.execute(f"""SELECT id, created_by, context, published_date 
                         FROM {t_news};""")
        obj = []
        for data in db.cursor.fetchall():
            news = NewsDB(
                id=data[0],
                created_by=data[1],
                context=data[2],
                published_date=str(data[3])
            )
            obj.append(news)

        # objects = [
        #     {
        #         "id": data[0],
        #         "created_by": data[1],
        #         "context": data[2],
        #         "published_date": str(data[3])
        #     }
        #     for data in db.cursor.fetchall()
        # ]
    return obj


def select_t_news_by_id(id: int) -> NewsDB:
    with MyDatabase() as db:
        db.cursor.execute(f"""
        SELECT id, created_by, context, published_date FROM {t_news}
        WHERE id={id};
                        """)
        # newsdb = NewsDB(id=2, created_by="123", context="dsad", published_date="dfdf")
        # print(newsdb)
        data = db.cursor.fetchone()
        if data is None:
            return None

    return NewsDB(
        id=data[0],
        created_by=data[1],
        context=data[2],
        published_date=str(data[3])
    )
    # return {
    #     "id": data[0],
    #     "created_by": data[1],
    #     "context": data[2],
    #     "published_date": str(data[3])
    # }


def insert_t_news(payload: NewsSchema, *args, **kwargs) -> NewsDB:
    with MyDatabase() as db:
        db.cursor.execute(f"""
        INSERT INTO {t_news}(created_by, context, published_date) 
        VALUES('{payload.created_by}', 
                '{payload.context}', 
                '{payload.published_date}'
                ) 
        RETURNING id;
                    """)

        db.connection.commit()
        inserted_id = db.cursor.fetchone()[0]
        obj = select_t_news_by_id(inserted_id)
    return obj


def update_t_news_by_id(id: int, payload: NewsSchema) -> NewsDB:
    with MyDatabase() as db:
        db.cursor.execute(f"""
        UPDATE {t_news}
        SET created_by='{payload.created_by}', 
            context='{payload.context}', 
            published_date='{payload.published_date}'
        WHERE id='{id}';
        """)
        db.connection.commit()
        # result = db.cursor.fetchone()
        # if not result:
        #     return None
        # updated_id = result[0]
        # obj = select_t_news_by_id(updated_id)
        obj = select_t_news_by_id(id)
    return obj


def delete_t_news_by_id(id: int) -> bool:
    with MyDatabase() as db:
        db.cursor.execute(f"""
        DELETE FROM {t_news}
        WHERE id={id};
                        """)
        db.connection.commit()
    return True
