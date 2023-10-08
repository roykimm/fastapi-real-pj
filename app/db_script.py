from app.database import MyDatabase

def create_table():
    with MyDatabase() as db:
        # t_news
        db.cursor.execute(f"""CREATE TABLE users (
            id integer(10) PRIMARY KEY AUTO_INCREMENT,
            username varchar(255) not null,
            email varchar(255) not null,
            password varchar(255) not null,
            created_date timestamp default now()
            );
        """)
        # db.cursor.execute(f"DROP TABLE IF EXISTS t_news CASCADE;")

        # # t_news
        # db.cursor.execute(f"""CREATE TABLE t_news (
        #     id integer(10) PRIMARY KEY AUTO_INCREMENT,
        #     published_date timestamp DEFAULT NOW(),
        #     created_date timestamp DEFAULT NOW(),
        #     created_by varchar(140),
        #     context TEXT NOT NULL
        #     );
        # """)
        # db.cursor.execute(f"DROP TABLE IF EXISTS t_news CASCADE;")
        db.connection.commit()
        print("Tables are created successfully...")
