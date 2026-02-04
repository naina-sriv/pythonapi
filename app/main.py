"""FastAPI CRUD Application with ORM SQLAlchemy and PostgreSQL Database Integration"""


from .database import engine, SessionLocal, get_db
from .routers import posts,user
from . import models
from fastapi import FastAPI


models.Base.metadata.create_all(bind=engine)

app=FastAPI()
 
    
app.include_router(posts.router) 
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get("/sqlalchemy")
# def test_posts(db:Session=Depends(get_db)):
# #     posts=db.query(models.Post)
# #     SELECT posts_ver_2.id AS posts_ver_2_id, posts_ver_2.title AS posts_ver_2_title, posts_ver_2.content AS posts_ver_2_content, posts_ver_2.published AS posts_ver_2_published, posts_ver_2.created_at AS posts_ver_2_created_at
# # FROM posts_ver_2
# #     print(posts)
#     posts=db.query(models.Post).all()
#     return {"message":posts}




    

