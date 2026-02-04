from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random



app=FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int]=None
    

    
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
    return {"Here are the posts:":my_posts}

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
    post_dict=post.dict()
    post_dict["id"]=random.randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

def find_post(id):
    for post in my_posts:
        if post['id']==id:
            return post
    return False

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
    index = find_post_index(id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exists.")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
    index=find_post_index(id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exists.")
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"message":post_dict}
    