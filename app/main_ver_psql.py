from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random
import psycopg
from psycopg.rows import dict_row
import time



app=FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int]=None
    
#connection IS REALLY imp so we repeat until its successfully
while True:    
    try:
        conn=psycopg.connect(host='localhost',
                             dbname='fastapi',
                             user='postgres',
                             password='dancemonkey',
                             row_factory=dict_row)
        cursor=conn.cursor()
        print("Database is connected sucessfully")
        break
    #changes from psycopg2: database to dbname, RealDictCursor to dict_rows imported from psycopg.rows
    except Exception as err:
        print("Connection to database failed")
        print("Error:",err)
        #using time module so that it waits 2 secs before retrying
        time.sleep(2)
    
my_posts=[{"title": "title of post1", "content":"content of post 1", "id":1},
         {"title": "title of post2", "content":"content of post 2", "id":2}]
@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get("/posts")
# def get_posts():
#     return {"Here are the posts:":"hello"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""") ##just passing the statement
    #to commit the statement we use conn.commit
    posts=cursor.fetchall() #for multiple posts
    #cursor.fetchone() for one post
    print(posts)
    # return {"Here are the posts:":my_posts}
    return {"Here are the posts:":posts}

# @app.post("/createposts")
# def createpost(payLoad: dict= Body(...)):
#     print(payLoad)
#     return {"new post":f"title: {payLoad["title"]} content: {payLoad["content"]}"}
            
#title str, str content


    
# @app.post("/createposts")
# def createpost(post: Post):
#     print(post)
#     return {"post":f"{post}", "post dict":f"{post.dict()}"}  
#     {
#     "post": "title='top books in my library' content='check out my home library!' published=True rating=None",
#     "post dict": "{'title': 'top books in my library', 'content': 'check out my home library!', 'published': True, 'rating': None}"
# }

@app.post("/posts")
def create_post(post: Post):
    # post_dict=post.dict()
    # post_dict["id"]=random.randrange(0,1000000)
    # my_posts.append(post_dict)
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    #here we dont use f string cause that will make us vulnerable to sql injection
    new_post=cursor.fetchone()
    conn.commit()
    return {"data":new_post}  

def find_post(id):
    # for post in my_posts:
    #     if post['id']==id:
    #         return post
    # else:
    #     # return "not found"
        # return False
    cursor.execute("""SELECT * FROM posts WHERE id=%s""",(id,))
    #here just id was not expected instead (id,) as single valued tuple worked
    #no need to commit for select
    post=cursor.fetchone()
    return post

def find_post_index(id):
    index=-1
    for post in my_posts:
        index+=1
        if post['id']==id:
            return index
            
@app.get("/posts/{id}") #automatic validation
def get_post(id:int):
    print(id)
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {f"post at {id}":find_post(id)}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(id,))
    # my_posts.pop(find_post_index(id))
    del_post=cursor.fetchone()
    if not del_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exists.")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *""",(post.title,post.content,id))
    updated_post=cursor.fetchone()
    conn.commit()
    # index=find_post_index(id)
    # post_dict=post.dict()
    # post_dict['id']=id
    # my_posts[index]=post_dict
    return {"message":updated_post}
    